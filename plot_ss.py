import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import argparse

parser = argparse.ArgumentParser(
    description="Plot the secondary structure of a trajectory file"
)
parser.add_argument(
    "-i",
    "--input",
    help="Input file (should be the output of plot_ss.tcl)",
    required=True,
)
parser.add_argument("-o", "--output", help="Output file", required=True)
args = parser.parse_args()

df = pd.read_csv(args.input, delimiter="\s+")
num_frames = len(df.index)
num_residues = len(df.columns)
print(num_residues, num_frames)

x = np.arange(1, num_residues+1, 1, dtype=int)
bar_incr = np.ones((num_residues,), dtype=int)
fig, ax = plt.subplots()

beta_color = "orange"
alpha_color = "blue"
turn_color = "green"
coil_color = "black"

color_dict = {
    "B": beta_color,
    "b": beta_color,
    "E": beta_color,
    "H": alpha_color,
    "G": alpha_color,
    "I": alpha_color,
    "T": turn_color,
    "c": coil_color,
    "C": coil_color,
}

values = np.array([bar_incr for i in range(num_frames)])

# plot bars in stack manner
for i in range(values.shape[0]):
    ax.bar(
        x,
        values[i],
        bottom=np.sum(values[:i], axis=0),
        color=[color_dict[r] for r in df.iloc[i]],
    )

plt.xlabel("Residue")
plt.ylabel("Frame")

alpha_leg = mpatches.Patch(color=alpha_color, label='Alpha Helices')
beta_leg = mpatches.Patch(color=beta_color, label='Beta Strands')
turn_leg = mpatches.Patch(color=turn_color, label='Turns')
other_leg = mpatches.Patch(color=coil_color, label='Coils / Other')

ax.legend(handles=[alpha_leg, beta_leg, turn_leg, other_leg])

plt.savefig(
    args.output, dpi=500, bbox_inches="tight", transparent=True, pad_inches=0.01
)
