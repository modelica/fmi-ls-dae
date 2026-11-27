# MassSpringOscillator

A reference FMU demonstrating **invariants** in [FMI-LS-DAE] — the Layered Standard for DAE support in FMI 3.0.

The model is an undamped mass-spring oscillator. A mass `m` is attached to a spring with spring constant `k`; when the mass is displaced by `x` from its equilibrium position, the spring exerts the restoring force `F = -k*x`.

Written as a semi-explicit index-1 DAE, with the spring force `F` as the algebraic variable:

```text
der(x) = v
der(v) = F / m

0 = F + k * x                     (residual 0)

E = m/2 * v² + k/2 * x²           (invariant, also an output)
```

`E` is the total mechanical energy of the system. It is constant along the exact solution, which makes it an **invariant** of the model, declared with the `<Invariant>` element of the extended `<ModelStructure>`.

| Variable         | Kind                  | Value reference | Initial value |
| ---------------- | --------------------- | --------------- | ------------- |
| `x`              | differential state    | 1               | 1.0           |
| `v`              | differential state    | 3               | 0.0           |
| `F`              | algebraic variable    | 5               | approx -1.0   |
| `m`              | parameter             | 6               | 1.0           |
| `k`              | parameter             | 7               | 1.0           |
| `E`              | output, **invariant** | 8               | —             |
| `__residual0`    | residual              | 9               | —             |
| `ODE_DAE_Switch` | structural parameter  | 10              | `false`       |

The algebraic variable `F`, the residual equation and the invariant `E` are declared in [`fmi-ls-manifest.xml`][manifest], which is packaged into the FMU under `extra/org.fmi-standard.fmi-ls-dae/`.

## Why this model

With the default parameters `m = k = 1` and the initial state `(x, v) = (1, 0)`, the analytical solution is `x(t) = cos(t)`, `v(t) = -sin(t)`, and the energy stays at `E = 0.5` forever — in the phase plane the solution traces a closed ellipse.

A numerical solver does not preserve that. Substituting an explicit Euler step into `E` gives, for `m = k = 1`,

```text
E_{n+1} = E_n * (1 + h²)
```

so the energy grows at *every* step and the solution spirals outward. Integrating to `t = 20` with `h = 0.1` raises the energy from `0.5` to `0.5 * 1.01²⁰⁰ ≈ 3.66` — a sevenfold error in a quantity that physics says cannot change at all.

This is the *numerical drift* that motivates exposing invariants. An importer that reads the `<Invariant>` element can evaluate `E` during the simulation, compare it against its initial value, and either report the accumulated drift or project the states back onto the manifold `E = E(0)`.

Version `1.0.0-alpha.2` of the layered standard describes the optional correction `δ = x̃ - x` between the integrated and the projected state, but does not yet define a manifest element for it, so this FMU does not expose it.

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

The FMU is written to `build/fmus/MassSpringOscillator.fmu`.

By default CMake detects the host architecture. To cross-compile, pass `-DFMI_ARCHITECTURE=<arch>` where `<arch>` is one of `x86_64` or `aarch64`.

## Files

| File                   | Purpose                                                                  |
| ---------------------- | ------------------------------------------------------------------------ |
| `config.h`             | Model identifier, value references, `ModelData` struct                   |
| `model.c`              | Model equations (ODE right-hand sides, residual, invariant)              |
| `modelDescription.xml` | FMI 3.0 model description                                                |
| `buildDescription.xml` | FMI 3.0 build description (source compilation)                           |
| `fmi-ls-manifest.xml`  | LS-DAE manifest declaring the algebraic variable, residual and invariant |

[FMI-LS-DAE]: https://github.com/modelica/fmi-ls-dae
[CMake]: https://cmake.org/
[manifest]: fmi-ls-manifest.xml
