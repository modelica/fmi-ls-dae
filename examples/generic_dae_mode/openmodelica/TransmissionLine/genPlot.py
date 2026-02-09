import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
# Load CSV

csv_file = os.path.join(os.path.dirname(__file__), "times.csv")
df = pd.read_csv(csv_file)

# Unique N values
Ns = sorted(df['N'].unique())

# Prepare data for stacked bars
timeSimulation_ODE = []
timeExport_ODE = []
timeSimulation_DAE = []
timeExport_DAE = []

export_columns = ['timeFrontend', 'timeBackend', 'timeSimCode', 'timeTemplates', 'timeCompile']

for n in Ns:
    # Filter by N and ODE
    ode_row = df[(df['N'] == n) & (df['ODE'] == 1)]
    dae_row = df[(df['N'] == n) & (df['ODE'] == 0)]

    timeSimulation_ODE.append(ode_row['timeSimulation'].values[0] if not ode_row.empty else 0)
    timeExport_ODE.append(ode_row[export_columns].values.sum() if not ode_row.empty else 0)

    timeSimulation_DAE.append(dae_row['timeSimulation'].values[0] if not dae_row.empty else 0)
    timeExport_DAE.append(dae_row[export_columns].values.sum() if not dae_row.empty else 0)

# X positions for bars
x = np.arange(len(Ns))
width = 0.35  # space between ODE and DAE bars

fig, ax = plt.subplots(figsize=(10, 6))

# Plot stacked bars
ax.bar(x - width/2, timeExport_ODE, width, label='ODE: FMU Export', color='steelblue')
ax.bar(x - width/2, timeSimulation_ODE, width, bottom=timeExport_ODE, label='ODE: Simulation', color='skyblue')

ax.bar(x + width/2, timeExport_DAE, width, label='DAE: FMU Export', color='darkred')
ax.bar(x + width/2, timeSimulation_DAE, width, bottom=timeExport_DAE, label='DAE: Simulation', color='lightcoral')

# Labels and ticks
ax.grid(axis='y', linestyle='--', alpha=0.25)
ax.set_xlabel('ScalableTestSuite.Electrical.TransmissionLine.ScaledExperiments.TransmissionLineModelica_N_<N>')
ax.set_ylabel('Time (s)')
ax.set_title('FMU Export and Simulation Time for ODE vs DAE')
ax.set_xticks(x)
ax.set_xticklabels(Ns)
ax.legend()

plt.tight_layout()

png_file = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "docs", "images", "ODE_vs_DAE_export_times.png")
plt.savefig(png_file)
