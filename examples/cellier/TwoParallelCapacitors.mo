model TwoParallelCapacitors
  extends Modelica.Icons.Example;
  import SI = Modelica.Units.SI;

  parameter SI.Resistance r=1 "Resistance";
  parameter SI.Capacitance c1=1 "Capacitance of capacitor 1";
  parameter SI.Capacitance c2=1 "Capacitance of capacitor 2";
  Modelica.Electrical.Analog.Basic.Ground ground annotation(
    Placement(transformation(origin = {-20, -80}, extent = {{-20, -20}, {20, 20}})));
  Modelica.Electrical.Analog.Sources.SineVoltage sineVoltage(V = 1, f = 1)  annotation(
    Placement(transformation(origin = {-60, 0}, extent = {{-20, -20}, {20, 20}}, rotation = -90)));
  Modelica.Electrical.Analog.Basic.Resistor resistor(R = r)  annotation(
    Placement(transformation(origin = {-20, 60}, extent = {{-20, -20}, {20, 20}})));
  Modelica.Electrical.Analog.Basic.Capacitor capacitor_1(C = c1)  annotation(
    Placement(transformation(origin = {20, 0},extent = {{-20, -20}, {20, 20}}, rotation = -90)));
  Modelica.Electrical.Analog.Basic.Capacitor capacitor_2(C = c2) annotation(
    Placement(transformation(origin = {70, 0}, extent = {{-20, -20}, {20, 20}}, rotation = -90)));
equation
  connect(sineVoltage.p, resistor.p) annotation(
    Line(points = {{-60, 20}, {-60, 60}, {-40, 60}}, color = {0, 0, 255}));
  connect(resistor.n, capacitor_1.p) annotation(
    Line(points = {{0, 60}, {20, 60}, {20, 20}}, color = {0, 0, 255}));
  connect(resistor.n, capacitor_2.p) annotation(
    Line(points = {{0, 60}, {70, 60}, {70, 20}}, color = {0, 0, 255}));
  connect(capacitor_1.n, ground.p) annotation(
    Line(points = {{20, -20}, {20, -60}, {-20, -60}}, color = {0, 0, 255}));
  connect(ground.p, sineVoltage.n) annotation(
    Line(points = {{-20, -60}, {-60, -60}, {-60, -20}}, color = {0, 0, 255}));
  connect(capacitor_2.n, ground.p) annotation(
    Line(points = {{70, -20}, {70, -60}, {-20, -60}}, color = {0, 0, 255}));

annotation(
    uses(Modelica(version = "4.1.0")));
end TwoParallelCapacitors;
