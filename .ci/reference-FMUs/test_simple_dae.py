"""Simulation tests for the SimpleDAE reference FMU.

Run with:
    SIMPLE_DAE_FMU=path/to/SimpleDAE.fmu pytest test_simple_dae.py -v
"""

import os

import numpy as np
import pytest
from fmpy import simulate_fmu

FMU = os.environ.get('SIMPLE_DAE_FMU', 'SimpleDAE.fmu')

STOP_TIME = 5.0
STEP_SIZE = 1e-4


def test_ode_mode():
    """FMU simulates to stop time in ODE (Model Exchange) mode with correct outputs.

    A non-DAE-aware importer treats z1 and z2 as fixed at 0.0 (their initial
    approximation) and integrates the remaining ODE.  With z1=z2=0 the output
    equations reduce to:
        y1 = sin(u2)
        y2 = sin(u1 * u2)
    These are constant (no state dependence), so the expected values are exact.
    """
    u1, u2 = 2.0, 0.5

    result = simulate_fmu(
        FMU,
        start_time=0.0,
        stop_time=STOP_TIME,
        step_size=STEP_SIZE,
        start_values={'u1': u1, 'u2': u2},
    )

    assert result['time'][-1] >= STOP_TIME - 1e-6, \
        f"simulation stopped early at t={result['time'][-1]}"

    expected_y1 = np.sin(u2)
    expected_y2 = np.sin(u1 * u2)
    atol = 1e-10

    assert np.allclose(result['y1'], expected_y1, atol=atol), \
        f"y1: expected {expected_y1}, got {result['y1'][-1]}"
    assert np.allclose(result['y2'], expected_y2, atol=atol), \
        f"y2: expected {expected_y2}, got {result['y2'][-1]}"


@pytest.mark.skip(reason="DAE-aware importer not yet available")
def test_dae_mode():
    """Simulate with a DAE-aware importer and verify algebraic constraints.

    A DAE-aware importer must:
    - read AlgebraicVariables from extra/org.fmi-standard.fmi-ls-dae/fmi-ls-manifest.xml
    - solve the nonlinear system for z1, z2 at each step via fmi3SetFloat64
    - verify that the residuals (__residual0, __residual1) are driven to zero

    TODO: replace the pass below with a real DAE importer call once one is
    available and assert that residuals stay below a tolerance, e.g.:
        assert np.all(np.abs(result['__residual0']) < 1e-8)
        assert np.all(np.abs(result['__residual1']) < 1e-8)
    """
    pass
