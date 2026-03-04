# CauerLowPassAnalog Example

## Build ODE / DAE

The `buildModel.mos` script will export
`Modelica.Electrical.Analog.Examples.CauerLowPassAnalog` to Base Modelica
([CauerLowPassAnalog.bmo](CauerLowPassAnalog.bmo)) and then build both ODE and
DAE versions of the flat model.

```bash
omc buildModel.mos
```

## Index of CauerLowPassAnalog

Index reduction is logged by adding translation flag `-d=bltdump` and the result
was manually pasted into [indexReduction.log](indexReduction.log). To get the
differential / perturbation index of the system count the numbers of `Index
Reduction neccessary!` during matching. OpenModelica will reduce the index to 1.
So this example is an index 2 DAE.

## Image generation

The image [CauerLowPassAnalog.svg](CauerLowPassAnalog.svg) was exported using
OMEdit for `Modelica.Electrical.Analog.Examples.CauerLowPassAnalog`.
