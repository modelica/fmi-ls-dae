# FMI Layered Standard for DAE (FMI-LS-DAE)

[![Build Layered Standard DAE][badge-build-ls-dae]][build-ls-dae]
[![Validate XML manifests][badge-validate-xml]][validate-xml]
[![Static Badge][badge-docs]][spec]

This repository contains an early prototype draft for the FMI Layered Standard
for DAE (FMI-LS-DAE) based on the [Function Mock-up Interface][FMI] (FMI).

Based on FMI 3.0, this layered standard plans to define how
differential-algebraic equation systems (DAEs) can be exported for
ModelExchange.

## FMI-LS-DAE Standard

This [FMI 3.0 Layered Standard][spec] for DAE export is currently maintained on
[GitHub][githubspec] and is published here.

## Repository Structure

* `docs` -- Sources of the specification document
* `schema` -- XSD schema for this FMI Layered Standard

## How to Contribute

See [CONTRIBUTING.md][contributing-file].

## Copyright and License

Code and documentation copyright (C) 2025 The Modelica Association Project FMI.
Code released under the [2-Clause BSD License].

## Private Sandbox

For development there is a private sandbox
[modelica/fmi-ls-dae-sandbox][sandbox] to store non-public information.

[2-Clause BSD License]: https://opensource.org/licenses/BSD-2-Clause
[badge-build-ls-dae]: https://github.com/modelica/fmi-ls-dae/actions/workflows/build-ls-dae.yml/badge.svg?branch=main
[badge-docs]: https://img.shields.io/badge/docs-FMI--LS--DAE-blue?logo=github
[badge-validate-xml]: https://github.com/modelica/fmi-ls-dae/actions/workflows/validate-xml.yml/badge.svg?branch=main
[build-ls-dae]: https://github.com/modelica/fmi-ls-dae/actions/workflows/build-ls-dae.yml
[contributing-file]: CONTRIBUTING.md
[FMI]: https://fmi-standard.org/
[githubspec]: docs/index.adoc
[sandbox]: https://github.com/modelica/fmi-ls-dae-sandbox
[spec]: https://modelica.github.io/fmi-ls-dae/main/
[validate-xml]: https://github.com/modelica/fmi-ls-dae/actions/workflows/validate-xml.yml
