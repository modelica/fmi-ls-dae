# SimpleDAE

A reference FMU demonstrating [FMI-LS-DAE] — the Layered Standard for DAE support in FMI 3.0.

The model is a semi-explicit index-1 DAE with two differential states, two algebraic variables, two inputs, and two outputs:

```text
der(x1) = sin(x1) + sin(z1 * z2 * u1)
der(x2) = sin(x1 * x2) + sin(z1 * z2 * u2) + u1²

0 = z1 * u1² + tanh(3 * z1) + u2 * x1³          (residual 0)
0 = exp(z1 * z2 * u1) / 3 - sin(z2 * x2)        (residual 1)

y1 = u1 * x1 * z1 + sin(u2)
y2 = u2 * x2 * z2 + sin(u1 * u2)
```

| Variable      | Kind               | Value reference | Initial value |
| ------------- | ------------------ | --------------- | ------------- |
| `x1`          | differential state | 1               | 0.5           |
| `x2`          | differential state | 3               | 0.5           |
| `z1`          | algebraic variable | 5               | approx 0.0    |
| `z2`          | algebraic variable | 6               | approx 0.0    |
| `u1`          | input              | 7               | 0.0           |
| `u2`          | input              | 8               | 0.0           |
| `y1`          | output             | 9               | —             |
| `y2`          | output             | 10              | —             |
| `__residual0` | residual           | 11              | —             |
| `__residual1` | residual           | 12              | —             |

The algebraic variables `z1` and `z2` and the residual equations are declared in [`fmi-ls-manifest.xml`][manifest], which is packaged into the FMU under `extra/org.fmi-standard.fmi-ls-dae/`.

## FMI interface

- FMI version: 3.0
- Interface type: Model Exchange only
- `canGetAndSetFMUState`: yes
- `canSerializeFMUState`: yes
- `providesDirectionalDerivatives`: yes
- `providesAdjointDerivatives`: yes

## Build

Prerequisites: [CMake] 3.17+ and a C99 compiler.

From the repository root:

```sh
cd reference-FMUs
cmake -B build
cmake --build build --config Release
```

The FMU is written to `build/fmus/SimpleDAE.fmu`.

By default CMake detects the host architecture. To cross-compile, pass `-DFMI_ARCHITECTURE=<arch>` where `<arch>` is one of `x86_64` or `aarch64`.

## Files

| File                    | Purpose                                                     |
| ----------------------- | ----------------------------------------------------------- |
| `config.h`              | Model identifier, value references, `ModelData` struct      |
| `model.c`               | Model equations (ODE right-hand sides, residuals, outputs)  |
| `modelDescription.xml`  | FMI 3.0 model description                                   |
| `buildDescription.xml`  | FMI 3.0 build description (source compilation)              |
| `fmi-ls-manifest.xml`   | LS-DAE manifest declaring algebraic variables and residuals |

[FMI-LS-DAE]: https://github.com/modelica/fmi-ls-dae
[manifest]: fmi-ls-manifest.xml
