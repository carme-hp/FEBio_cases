import pandas as pd
import matplotlib.pyplot as plt

# Looking for the specific files we generated today
tmax_values = [2, 3, 4, 5]
files = {t: f"tmax{t}_disp.txt" for t in tmax_values}

def parse_febio_log(filepath):
    times = []
    uz_vals = []
    current_time = 0.0
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # 1. Grab the time from the header line
            if line.startswith('*Time'):
                parts = line.split('=')
                current_time = float(parts[1].strip())
            # 2. Grab the displacement data from the number line
            elif not line.startswith('*') and len(line) > 0:
                parts = line.split()
                if len(parts) >= 4:
                    # parts[0] is Node ID (1773)
                    # parts[1] is ux, parts[2] is uy, parts[3] is uz
                    uz = float(parts[3])
                    times.append(current_time)
                    uz_vals.append(uz)
                    
    return pd.DataFrame({'time': times, 'uz': uz_vals})

fig, ax = plt.subplots(figsize=(8, 5))

for tmax, filepath in files.items():
    df = parse_febio_log(filepath)
    ax.plot(df['time'], df['uz'], label=f'Tmax = {tmax}')

ax.set_xlabel('Time (s)')
ax.set_ylabel('Z-Displacement (mm)')
ax.set_title('Node 1773 — Z-Displacement vs Time\nMonolithic Muscle Contraction Parameter Sweep')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('tmax_sweep_comparison.png', dpi=150)
print("Plot successfully saved as tmax_sweep_comparison.png!")
