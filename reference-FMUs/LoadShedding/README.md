# LoadShedding

A reference FMU demonstrating **event iteration** with [FMI-LS-DAE] — the Layered Standard for DAE support in FMI 3.0.

The model is a capacitor discharging into two parallel loads. When the voltage falls below `vShed`, the main load is shed by raising its resistance from `R` to `RShed`. If the main load then still draws more than `iMax`, the auxiliary load is disconnected for good.

Written as a semi-explicit index-1 DAE, with the main load current `i` as the algebraic variable:

```modelica
model LoadShedding
  parameter Real C = 1, R = 1, RShed = 10, RAux = 2, vShed = 0.5, iMax = 0.2;
  Real v(start = 1, fixed = true);
  Real i;
  Boolean shed;
  Boolean tripped(start = false, fixed = true);
equation
  C*der(v) = -i - (if tripped then 0 else v/RAux);
  shed = v < vShed;
  0 = (if shed then RShed else R)*i - v;      // residual 0
  when shed and i > iMax then
    tripped = true;
  end when;
end LoadShedding;
```

| Variable         | Kind                 | Value reference | Initial value |
| ---------------- | -------------------- | --------------- | ------------- |
| `v`              | differential state   | 1               | 1.0           |
| `i`              | algebraic variable   | 3               | approx 1.0    |
| `C`              | parameter            | 4               | 1.0           |
| `R`              | parameter            | 5               | 1.0           |
| `RShed`          | parameter            | 6               | 10.0          |
| `RAux`           | parameter            | 7               | 2.0           |
| `vShed`          | parameter            | 8               | 0.5           |
| `iMax`           | parameter            | 9               | 0.2           |
| `__residual0`    | residual             | 10              | —             |
| `g1`             | event indicator      | 11              | —             |
| `g2`             | event indicator      | 12              | —             |
| `shed`           | output, discrete     | 13              | false         |
| `tripped`        | output, discrete     | 14              | false         |
| `ODE_DAE_Switch` | structural parameter | 15              | `false`       |

The model is constructed for this purpose, it is not an established benchmark.

## Why this model

The event at `t = ln(2)/1.5 ≈ 0.4621` has to be evaluated in the sorted order

```text
shed -> i -> tripped -> der(v)
```

Right before the event `i = v/R = 0.5`, above `iMax`. Once `shed` is true, the current is `i = v/RShed = 0.05`, below `iMax`, so `tripped` has to stay false.

In DAE mode the importer owns `i`. When the FMU enters Event Mode, the value it holds still belongs to the old value of `shed`. An FMU that evaluates the when-equation with that value latches `tripped`, and no later pass can undo it. The current and the residual are correct even then, only the discrete state and the rest of the trajectory are wrong.

| Evaluation at the event                        | `RShed = 10`: must not trip | `RShed = 2`: must trip |
| ---------------------------------------------- | --------------------------- | ---------------------- |
| Exact solution, `v(2)`                         | 0.198714                    | 0.231750               |
| Using the `i` of the importer, before re-solve | 0.428726, trips             | 0.231750               |

The second parameter set guards against the opposite mistake, not evaluating `tripped` after the current has changed.

Between events the solution is an exponential decay, so the exact solution is available in closed form. This is the solution the [tests][tests] compare against. `v` is continuous at the event, while `i` and `der(v)` jump.

## Event handling

Event handling is outside the scope of version `1.0.0-alpha.1` of the layered standard. This FMU supports two possible conventions, and the value of `ODE_DAE_Switch` during the event iteration selects between them. An importer has to follow one of them: if it stays in DAE mode and does not solve the residual between passes, `tripped` latches with the old current.

### Option A: switch to ODE mode

The importer switches the FMU to ODE mode for the event iteration, using Reconfiguration Mode as described in the layered standard:

1. Enter Event Mode, then switch to ODE mode with `fmi3EnterConfigurationMode`, `fmi3SetBoolean` and `fmi3ExitConfigurationMode`.
2. Call `fmi3UpdateDiscreteStates` until `discreteStatesNeedUpdate` is `false`. The FMU evaluates `shed`, `i = v/R(shed)`, the when-condition and `tripped` in sorted order within one pass.
3. Read `i` with `fmi3GetFloat64`.
4. Switch back to DAE mode, set `i` with `fmi3SetFloat64`, and restart the integration.

### Option B: stay in DAE mode

The FMU stays in DAE mode and does not use the causalized form during the event iteration. The discrete equations are split into two layers, separated by the algebraic variable they depend on:

| Layer | Equations                                 | Needs                  |
| ----- | ----------------------------------------- | ---------------------- |
| 1     | `shed = v < vShed`                        | the state `v`          |
| 2     | `tripCondition`, then `tripped`           | `i`, solved for `shed` |

1. Call `fmi3UpdateDiscreteStates`. A pass that changes `shed` stops there and sets `discreteStatesNeedUpdate` to `true`. Otherwise the pass also evaluates layer 2.
2. While `discreteStatesNeedUpdate` is `true`, solve the residual for `i`, using `fmi3SetFloat64` and `fmi3GetFloat64` in Event Mode, and call `fmi3UpdateDiscreteStates` again.
3. Restart the integration.

Setting `i` and reading the residual in Event Mode, and the meaning of the layers, are not defined by the layered standard. This option needs a protocol defined by it.

### Both options

- `discreteStatesNeedUpdate` is `true` after a pass that changed a discrete variable, so the last pass only confirms the result. At the event with `RShed = 2`, option A takes 2 passes and option B takes 3.
- The event indicator `g2` uses `i`. In DAE mode this is the current solved by the importer, so the crossing is located up to the tolerance of that solution.
- The FMU initializes in ODE mode, also when DAE mode is enabled, and leaves a consistent value of `i`. Initialization in DAE mode is not fully specified by the layered standard.

## FMI interface

- FMI version: 3.0
- Interface type: Model Exchange only
- `canGetAndSetFMUState`: yes
- `canSerializeFMUState`: yes
- `providesDirectionalDerivatives`: no
- `providesAdjointDerivatives`: no

## Build

Prerequisites: [CMake] 3.17+ and a C99 compiler.

From the repository root:

```sh
cd reference-FMUs
cmake -B build
cmake --build build --config Release
```

The FMU is written to `build/fmus/LoadShedding.fmu`.

By default CMake detects the host architecture. To cross-compile, pass `-DFMI_ARCHITECTURE=<arch>` where `<arch>` is one of `x86_64` or `aarch64`.

## Files

| File                   | Purpose                                                                  |
| ---------------------- | ------------------------------------------------------------------------ |
| `config.h`             | Model identifier, value references, `ModelData` struct                   |
| `model.c`              | Model equations, event indicators and event iteration                    |
| `modelDescription.xml` | FMI 3.0 model description                                                |
| `buildDescription.xml` | FMI 3.0 build description (source compilation)                           |
| `fmi-ls-manifest.xml`  | LS-DAE manifest declaring the algebraic variable and residual            |

[FMI-LS-DAE]: https://github.com/modelica/fmi-ls-dae
[CMake]: https://cmake.org/
[tests]: ../../.ci/reference-FMUs/test_load_shedding.py
