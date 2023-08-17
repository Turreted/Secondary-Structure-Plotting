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
parser.add_argument(
    "-r",
    "--residues",
    help="Number of Residues in Chain",
    type=int,
    required=True,
)
parser.add_argument("-o", "--output", help="Output file", required=True)
args = parser.parse_args()

df = pd.read_csv(args.input, delimiter="\s+")

num_frames = len(df.index)
num_residues = args.residues

x = np.arange(1, num_residues+1, 1, dtype=int)
bar_incr = np.ones((num_residues,), dtype=int)
fig, ax = plt.subplots()
plt.ylim(0.0, 1.1)

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
alpha = np.zeros(num_residues)
beta = np.zeros(num_residues)
turn = np.zeros(num_residues)


for i, col in enumerate(df):
    res_index = i % num_residues
    for structure in df[col]:
        # alpha-helix
        if structure in ["H", "G", "I"]:
            alpha[res_index] += 1
        
        # beta strand or sheet
        elif structure in ["B", "b", "E"]:
            beta[res_index] += 1
        
        # turn
        elif structure in ["T"]:
            turn[res_index] += 1
    
    alpha[res_index] /= num_frames
    beta[res_index] /= num_frames
    turn[res_index] /= num_frames

print(beta, turn)
plt.xlabel("Residue")
plt.ylabel("Frequency")

bottom = np.zeros(num_residues)
width = 0.5

p = ax.bar(x, alpha, width, label="Alpha", bottom=bottom, color=alpha_color)
bottom += alpha
p = ax.bar(x, beta, width, label="Beta", bottom=bottom, color=beta_color)
bottom += beta
p = ax.bar(x, turn, width, label="Turn", bottom=bottom, color=turn_color)

alpha_leg = mpatches.Patch(color=alpha_color, label='Alpha Helices')
beta_leg = mpatches.Patch(color=beta_color, label='Beta Strands')
turn_leg = mpatches.Patch(color=turn_color, label='Turns')

ax.legend(handles=[alpha_leg, beta_leg, turn_leg])

plt.savefig(
    "test.png", dpi=500, bbox_inches="tight", transparent=True, pad_inches=0.01
)
