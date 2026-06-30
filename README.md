# FMI Layered Standard for DAE (FMI-LS-DAE)

[![FMI-LS-DAE Specification][badge-docs]][spec]
[![Build Layered Standard DAE][badge-build-ls-dae]][build-ls-dae]
[![Validate XML manifests][badge-validate-xml]][validate-xml]

This repository contains an early prototype draft for the FMI Layered Standard
for DAE (FMI-LS-DAE) based on the [Function Mock-up Interface][FMI] (FMI).

Based on FMI 3.0, this layered standard plans to define how
differential-algebraic equation systems (DAEs) can be exported for
ModelExchange.

## FMI-LS-DAE Standard

This [FMI 3.0 Layered Standard][spec] for DAE export is currently maintained in this repository and published at [modelica.github.io/fmi-ls-dae/main][spec].

## Repository Structure

* `docs` -- Sources of the specification document
* `schema` -- XSD schema for this FMI Layered Standard

## Citation

If you use this work, please cite the accompanying pre-print:

> Nahodovic et al., "Towards an FMI Layered Standard for DAE: Applications for Simulation and Optimization", arXiv:2606.22544, 2026.
> <https://doi.org/10.48550/arXiv.2606.22544>

## How to Contribute

See [CONTRIBUTING.md][contributing-file].

## Copyright and License

Code and documentation copyright (C) 2025 The Modelica Association Project FMI.
Code released under the [2-Clause BSD License].

## Private Sandbox

For development there is a private sandbox
[modelica/fmi-ls-dae-sandbox][sandbox] to store non-public information.

[badge-docs]: https://img.shields.io/badge/Specification-FMI--LS--DAE-blue?logo=github
[spec]: https://modelica.github.io/fmi-ls-dae/main/
[badge-build-ls-dae]: https://github.com/modelica/fmi-ls-dae/actions/workflows/build-ls-dae.yml/badge.svg?branch=main
[build-ls-dae]: https://github.com/modelica/fmi-ls-dae/actions/workflows/build-ls-dae.yml
[badge-validate-xml]: https://github.com/modelica/fmi-ls-dae/actions/workflows/validate-xml.yml/badge.svg?branch=main
[validate-xml]: https://github.com/modelica/fmi-ls-dae/actions/workflows/validate-xml.yml
[FMI]: https://fmi-standard.org/
[contributing-file]: CONTRIBUTING.md
[2-Clause BSD License]: https://opensource.org/licenses/BSD-2-Clause
[sandbox]: https://github.com/modelica/fmi-ls-dae-sandbox
