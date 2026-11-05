"""Simulation tests for the LoadShedding reference FMU.

Run with:
    LOAD_SHEDDING_FMU=path/to/LoadShedding.fmu pytest test_load_shedding.py -v
"""

import ctypes
import math
import os
import shutil
import xml.etree.ElementTree as ET

import numpy as np
import pytest
from fmpy import extract, read_model_description, simulate_fmu
from fmpy.fmi3 import FMU3Model

FMU = os.environ.get('LOAD_SHEDDING_FMU', 'LoadShedding.fmu')

STOP_TIME = 2.0

C, R, R_AUX, V_SHED, I_MAX = 1.0, 1.0, 2.0, 0.5, 0.2

# RShed = 10: the current drops to 0.05 A, below iMax, so tripped must stay false.
# RShed = 2:  the current only drops to 0.25 A, above iMax, so tripped must latch.
CASES = [(10.0, False), (2.0, True)]


def pointer(values):
    return values.ctypes.data_as(ctypes.POINTER(ctypes.c_double))


def crossed(z0, z1):
    """A strict sign change: at z = 0 the relation v < vShed has not switched yet."""
    return np.any(z0 * z1 < 0)


def event_time():
    return C * math.log(1.0 / V_SHED) / (1.0 / R + 1.0 / R_AUX)


def analytical_v(t, r_shed, tripped):
    """Closed-form solution, an exponential decay on each side of the event."""
    t_e = event_time()
    if t < t_e:
        return math.exp(-(1.0 / R + 1.0 / R_AUX) * t / C)
    conductance = 1.0 / r_shed + (0.0 if tripped else 1.0 / R_AUX)
    return V_SHED * math.exp(-conductance * (t - t_e) / C)


@pytest.mark.parametrize('r_shed, tripped', CASES)
def test_ode_mode(r_shed, tripped):
    """A non-DAE-aware importer reproduces the analytical solution in ODE mode."""
    result = simulate_fmu(
        FMU,
        start_time=0.0,
        stop_time=STOP_TIME,
        output_interval=0.01,
        solver='CVode',
        relative_tolerance=1e-8,
        start_values={'RShed': r_shed},
        output=['v', 'i', 'shed', 'tripped', '__residual0'],
    )

    assert result['time'][-1] >= STOP_TIME - 1e-6, \
        f"simulation stopped early at t={result['time'][-1]}"

    t = result['time']
    expected = np.array([analytical_v(ti, r_shed, tripped) for ti in t])

    assert np.allclose(result['v'], expected, atol=1e-5), \
        f"v: max deviation is {np.max(np.abs(result['v'] - expected))}"

    after = t > event_time() + 1e-3
    before = t < event_time() - 1e-3
    assert not result['shed'][before].any() and result['shed'][after].all()
    assert not result['tripped'][before].any()
    assert (result['tripped'][after] == tripped).all(), \
        f"tripped: expected {tripped} after the event"

    # i = v/R(shed) holds exactly in ODE mode, so the residual is identically zero
    assert np.all(np.abs(result['__residual0']) < 1e-14)


class DaeImporter:
    """A minimal DAE-aware importer, driven by the fmi-ls-manifest.xml of the FMU.

    It integrates the state and the algebraic variable together with the implicit
    trapezoidal rule, solves the residual itself and locates events by bisection.
    Subclasses implement the event iteration.  This base class is an importer that
    stays in DAE mode and never solves the residual during the event iteration.
    """

    def __init__(self, unzipdir, r_shed, v_start=None):
        md = read_model_description(unzipdir)
        vrs = {v.name: v.valueReference for v in md.modelVariables}
        manifest = ET.parse(
            os.path.join(unzipdir, 'extra', 'org.fmi-standard.fmi-ls-dae', 'fmi-ls-manifest.xml')
        ).getroot()
        structure = manifest.find('ModelStructure')

        self.vr_enable = int(manifest.find('EnableDAEParameter').get('valueReference'))
        self.vr_i = int(manifest.find('AlgebraicVariables/AlgebraicVariable').get('valueReference'))
        self.vr_residual = int(structure.find('Residual').get('valueReference'))
        self.vr_shed, self.vr_tripped = vrs['shed'], vrs['tripped']

        assert self.vr_i == vrs['i']
        assert self.vr_residual == vrs['__residual0']
        assert self.vr_enable == vrs['ODE_DAE_Switch']

        self.fmu = FMU3Model(
            guid=md.guid,
            unzipDirectory=unzipdir,
            modelIdentifier=md.modelExchange.modelIdentifier,
            instanceName='instance',
        )
        self.fmu.instantiate()
        self.set_dae_mode(True)
        self.fmu.setFloat64([vrs['RShed']], [r_shed])
        if v_start is not None:
            self.fmu.setFloat64([vrs['v']], [v_start])

        self.event_passes = []
        self.events = []

    def set_dae_mode(self, enabled):
        self.fmu.enterConfigurationMode()
        self.fmu.setBoolean([self.vr_enable], [enabled])
        self.fmu.exitConfigurationMode()

    def evaluate(self, t, v, i):
        """Return der(v) and the residual at the given point."""
        self.fmu.setTime(t)
        self.fmu.setContinuousStates(pointer(np.array([v])), 1)
        self.fmu.setFloat64([self.vr_i], [i])
        dx = np.zeros(1)
        self.fmu.getContinuousStateDerivatives(pointer(dx), 1)
        return dx[0], self.fmu.getFloat64([self.vr_residual])[0]

    def indicators(self):
        z = np.zeros(2)
        self.fmu.getEventIndicators(pointer(z), 2)
        return z

    def step(self, t, v, i, f0, h):
        """Solve one implicit trapezoidal step for the state and the algebraic variable."""
        v1, i1 = v, i
        for _ in range(20):
            f1, r1 = self.evaluate(t + h, v1, i1)
            F = np.array([v1 - v - 0.5 * h * (f0 + f1), r1])
            if np.max(np.abs(F)) < 1e-13:
                break
            eps = 1e-7
            f_v, r_v = self.evaluate(t + h, v1 + eps, i1)
            f_i, r_i = self.evaluate(t + h, v1, i1 + eps)
            J = np.array([[1.0 - 0.5 * h * (f_v - f1) / eps, -0.5 * h * (f_i - f1) / eps],
                          [(r_v - r1) / eps, (r_i - r1) / eps]])
            dv, di = np.linalg.solve(J, -F)
            v1, i1 = v1 + dv, i1 + di
        return v1, i1

    def update_until_settled(self, between_passes=lambda: None):
        """Call fmi3UpdateDiscreteStates until no further pass is requested."""
        passes = 0
        while True:
            passes += 1
            need_update, terminate, *_ = self.fmu.updateDiscreteStates()
            assert not terminate
            if not need_update:
                break
            assert passes < 10, "event iteration does not converge"
            between_passes()
        self.event_passes.append(passes)

    def event_iteration(self):
        """Run the event iteration and return the current for the restart."""
        self.update_until_settled()
        return self.fmu.getFloat64([self.vr_i])[0]

    def discrete(self):
        return tuple(self.fmu.getBoolean([vr])[0] for vr in (self.vr_shed, self.vr_tripped))

    def simulate(self, stop_time=STOP_TIME, h=1e-3):
        self.fmu.enterInitializationMode(startTime=0.0)
        self.fmu.exitInitializationMode()
        t, v = 0.0, self.fmu.getFloat64([1])[0]
        i = self.event_iteration()
        self.fmu.enterContinuousTimeMode()

        while t < stop_time - 1e-12:
            hh = min(h, stop_time - t)
            f0, _ = self.evaluate(t, v, i)
            z0 = self.indicators()
            v1, i1 = self.step(t, v, i, f0, hh)
            self.evaluate(t + hh, v1, i1)
            z1 = self.indicators()

            if crossed(z0, z1):
                lo, hi = 0.0, hh
                for _ in range(60):
                    mid = 0.5 * (lo + hi)
                    self.evaluate(t, v, i)
                    vm, im = self.step(t, v, i, f0, mid)
                    self.evaluate(t + mid, vm, im)
                    if crossed(z0, self.indicators()):
                        hi = mid
                    else:
                        lo = mid
                self.evaluate(t, v, i)
                v, stale_i = self.step(t, v, i, f0, hi)
                t += hi
                # The FMU sees i as solved for the discrete states before the event
                self.evaluate(t, v, stale_i)

                self.fmu.enterEventMode()
                i = self.event_iteration()
                residual = self.fmu.getFloat64([self.vr_residual])[0]
                self.events.append({'t': t, 'v': v, 'stale_i': stale_i, 'i': i,
                                    'residual': residual, 'discrete': self.discrete()})
                self.fmu.enterContinuousTimeMode()
            else:
                t, v, i = t + hh, v1, i1

        self.evaluate(t, v, i)
        return t, v, i

    def close(self):
        self.fmu.terminate()
        self.fmu.freeInstance()


class SwitchToOde(DaeImporter):
    """Option A: run the event iteration in ODE mode, so the FMU computes i itself."""

    def event_iteration(self):
        self.set_dae_mode(False)
        self.update_until_settled()
        i = self.fmu.getFloat64([self.vr_i])[0]
        self.set_dae_mode(True)
        self.fmu.setFloat64([self.vr_i], [i])
        return i


class StayInDae(DaeImporter):
    """Option B: stay in DAE mode and solve the residual between the passes."""

    def solve_residual(self):
        i = self.fmu.getFloat64([self.vr_i])[0]
        for _ in range(20):
            self.fmu.setFloat64([self.vr_i], [i])
            r = self.fmu.getFloat64([self.vr_residual])[0]
            if abs(r) < 1e-13:
                return
            eps = 1e-7
            self.fmu.setFloat64([self.vr_i], [i + eps])
            r_eps = self.fmu.getFloat64([self.vr_residual])[0]
            i -= r * eps / (r_eps - r)
        raise AssertionError("the residual did not converge")

    def event_iteration(self):
        self.update_until_settled(between_passes=self.solve_residual)
        return self.fmu.getFloat64([self.vr_i])[0]


OPTIONS = [SwitchToOde, StayInDae]

# Passes per event, with the initial event first. The last pass of an event only
# confirms the result. Option B needs one more when both layers change.
PASSES = {
    (SwitchToOde, 10.0): [1, 2],
    (SwitchToOde, 2.0): [1, 2, 2],
    (StayInDae, 10.0): [1, 2],
    (StayInDae, 2.0): [1, 3, 2],
}


@pytest.fixture(scope='module')
def unzipdir():
    path = extract(FMU)
    yield path
    shutil.rmtree(path, ignore_errors=True)


@pytest.mark.parametrize('option', OPTIONS)
@pytest.mark.parametrize('r_shed, tripped', CASES)
def test_dae_mode(unzipdir, option, r_shed, tripped):
    """A DAE-aware importer gets the analytical solution, using the manifest only."""
    importer = option(unzipdir, r_shed)
    t, v, i = importer.simulate()
    final = importer.discrete()
    importer.close()

    assert t == pytest.approx(STOP_TIME)
    assert v == pytest.approx(analytical_v(STOP_TIME, r_shed, tripped), abs=1e-5)
    assert i == pytest.approx(v / r_shed, abs=1e-8)
    assert final == (True, tripped)


@pytest.mark.parametrize('option', OPTIONS)
@pytest.mark.parametrize('r_shed, tripped', CASES)
def test_event_iteration_sees_the_new_current(unzipdir, option, r_shed, tripped):
    """The when-equation is evaluated with the current that belongs to the new shed.

    Right before the first event the importer holds i = v/R = 0.5 A, above iMax.
    Evaluating the when-equation with that value would latch tripped for both
    values of RShed.
    """
    importer = option(unzipdir, r_shed)
    importer.simulate()
    importer.close()

    event = importer.events[0]

    assert event['t'] == pytest.approx(event_time(), abs=1e-6)
    assert event['stale_i'] > I_MAX, "this test needs a stale current above iMax"
    assert event['i'] == pytest.approx(V_SHED / r_shed, abs=1e-6)
    assert abs(event['residual']) < 1e-12
    assert event['discrete'] == (True, tripped)

    # nothing happens at the initial time, and there is no empty event at the crossing
    assert importer.event_passes == PASSES[option, r_shed]


def test_dae_mode_uses_the_current_of_the_importer():
    """Without solving the residual between the passes, tripped latches.

    This shows that the event iteration in DAE mode depends on the importer: the
    current and the residual recover afterwards, the discrete state does not.
    """
    path = extract(FMU)
    importer = DaeImporter(path, 10.0)
    t, v, i = importer.simulate()
    final = importer.discrete()
    importer.close()
    shutil.rmtree(path, ignore_errors=True)

    assert final == (True, True)
    assert v == pytest.approx(0.428726, abs=1e-5)
    assert v != pytest.approx(analytical_v(STOP_TIME, 10.0, False), abs=0.1)
    assert i == pytest.approx(v / 10.0, abs=1e-8)


@pytest.mark.parametrize('option', OPTIONS)
def test_algebraic_variable_jumps_at_the_event(unzipdir, option):
    """Unlike the state, the algebraic variable is discontinuous at the event."""
    importer = option(unzipdir, 10.0)
    importer.simulate()
    importer.close()

    event = importer.events[0]

    assert event['v'] == pytest.approx(V_SHED, abs=1e-6)
    assert event['stale_i'] == pytest.approx(0.5, abs=1e-6)
    assert event['i'] == pytest.approx(0.05, abs=1e-6)


@pytest.mark.parametrize('option', OPTIONS)
def test_initialization_below_the_threshold(unzipdir, option):
    """Starting with shed true, the when-equation does not fire at the initial time."""
    importer = option(unzipdir, 2.0, v_start=0.45)
    importer.fmu.enterInitializationMode(startTime=0.0)
    importer.fmu.exitInitializationMode()
    i = importer.event_iteration()
    final = importer.discrete()
    importer.close()

    assert i == pytest.approx(0.225)
    assert final == (True, False)
    assert importer.event_passes == [1]
