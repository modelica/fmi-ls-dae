# FMI Layered Standard for DAE (FMI-LS-DAE)

[![Build Layered Standard DAE][badge-build-ls-dae]][build-ls-dae]
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

## Copyright and License

Code and documentation copyright (C) 2025 The Modelica Association Project FMI.
Code released under the [2-Clause BSD License].

## Private Sandbox

For development there is a private sandbox
[modelica/fmi-ls-dae-sandbox][sandbox] to store non-public information.

[build-ls-dae]: https://github.com/modelica/fmi-ls-dae/actions/workflows/build-ls-dae.yml
[badge-build-ls-dae]: https://github.com/modelica/fmi-ls-dae/actions/workflows/build-ls-dae.yml/badge.svg?branch=main
[badge-docs]: https://img.shields.io/badge/docs-FMI--LS--DAE-blue?logo=github
[FMI]: https://fmi-standard.org/
[githubspec]: docs/index.adoc
[spec]: https://modelica.github.io/fmi-ls-dae/main/
[2-Clause BSD License]: https://opensource.org/licenses/BSD-2-Clause
[sandbox]: https://github.com/modelica/fmi-ls-dae-sandbox
