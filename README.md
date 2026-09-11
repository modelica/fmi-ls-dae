# FMI Layered Standard for DAE (FMI-LS-DAE)

[![Static Badge][badge-docs]][spec]
[![Download Reference FMUs][badge-fmus]][fmus-download]
[![Latest release][badge-release]][latest-release]

This repository contains an early prototype draft for the FMI Layered Standard
for DAE (FMI-LS-DAE) based on the [Function Mock-up Interface][FMI] (FMI).

Based on FMI 3.0, this layered standard plans to define how
differential-algebraic equation systems (DAEs) can be exported for
ModelExchange.

## FMI-LS-DAE Standard

This [FMI 3.0 Layered Standard][spec] for DAE export is currently maintained in
this repository and published at [modelica.github.io/fmi-ls-dae/main][spec].

### Latest release

Released versions of this layered standard are tagged and listed on the
[releases page][latest-release]. The specification linked above is built from
`main` and can therefore contain changes that are not part of any release yet.

## Reference FMUs

FMUs implementing this layered standard are maintained in the
[modelica/Reference-FMUs][reference-fmus] repository. Currently there is only
one:

* [`Roberts`][roberts] -- the Robertson problem from chemical kinetics, a
  semi-explicit index-1 DAE with two differential states and one algebraic
  variable. It ships the layered standard manifest `fmi-ls-dae.xml` for
  FMI-LS-DAE version `1.0.0-alpha.1` and is the worked example of the
  [specification][spec].

## Citation

If you use this work, please cite the accompanying pre-print:

> Nahodovic et al., "Towards an FMI Layered Standard for DAE: Applications for Simulation and Optimization", arXiv:2606.22544, 2026.
> <https://doi.org/10.48550/arXiv.2606.22544>

## Copyright and License

Code and documentation copyright (C) 2025 The Modelica Association Project FMI.
Code released under the [2-Clause BSD License].

## How to Contribute

See [CONTRIBUTING.md][contributing-file].

### Repository Structure

* `docs` -- Sources of the specification document
* `schema` -- XSD schema for this FMI Layered Standard

### Private Sandbox

For development there is a private sandbox
[modelica/fmi-ls-dae-sandbox][sandbox] to store non-public information.

[badge-docs]: https://img.shields.io/badge/Specification-FMI--LS--DAE-blue?logo=github
[spec]: https://modelica.github.io/fmi-ls-dae/main/
[badge-fmus]: https://img.shields.io/badge/download-Reference%20FMUs-blue?logo=github
[fmus-download]: https://nightly.link/modelica/fmi-ls-dae/workflows/build-fmus.yml/main/FMI-LS-DAE-FMUs.zip
[badge-release]: https://img.shields.io/github/v/release/modelica/fmi-ls-dae?include_prereleases&logo=github
[latest-release]: https://github.com/modelica/fmi-ls-dae/releases/latest
[FMI]: https://fmi-standard.org/
[reference-fmus]: https://github.com/modelica/Reference-FMUs
[roberts]: https://github.com/modelica/Reference-FMUs/tree/main/Roberts
[contributing-file]: CONTRIBUTING.md
[2-Clause BSD License]: https://opensource.org/licenses/BSD-2-Clause
[sandbox]: https://github.com/modelica/fmi-ls-dae-sandbox
