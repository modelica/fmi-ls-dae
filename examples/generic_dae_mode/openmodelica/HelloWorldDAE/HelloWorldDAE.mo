model HelloWorldDAE
  Real x(start = 1.0, fixed = true);
  Real y,z;
equation
  der(x) = y;
  y + 2*z = x;
  y - 3*z = 2*x;
end HelloWorldDAE;
