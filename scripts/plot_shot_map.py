import json
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle, Circle
from pathlib import Path

# === CONFIG ===
# Absolute path to your data directory
DATA_PATH = Path("/Users/amandadonohoe/Desktop/VSCode/prem-stats-tracker/data/understat")
FILE_NAME = "26727_by_player.json"

# Load the JSON data
file_path = DATA_PATH / FILE_NAME
with open(file_path, "r") as f:
    shots_by_player = json.load(f)

# Flatten shots into a list, annotate with result and team
all_shots = []
for player, shots in shots_by_player.items():
    for shot in shots:
        all_shots.append({
            "player": player,
            "x": float(shot["X"]),
            "y": float(shot["Y"]),
            "xG": float(shot["xG"]),
            "result": shot["result"],
            "team": shot["team"]
        })

# Convert Understat pitch coordinates to matplotlib-friendly (0 to 120 x 0 to 80)
def scale_coords(x, y):
    return x * 120, y * 80

# Shot result colors
colors = {
    "Goal": "green",
    "SavedShot": "blue",
    "BlockedShot": "orange",
    "MissedShots": "red"
}

# === PLOT SETUP ===
fig, ax = plt.subplots(figsize=(7, 10))  # Taller to match vertical pitch
ax.set_xlim(60, 120)  # Show attacking half only
ax.set_ylim(0, 80)
ax.set_aspect('equal')  # Maintain real-world proportions
ax.set_title("Shot Map: Manchester United vs Everton", fontsize=16, fontweight='semibold', pad=20)
ax.axis("off")

# Pitch background color
ax.set_facecolor("#f4f4f4")

# Draw right-side pitch markings (attacking half)
# Outer boundaries (right half)
ax.plot([60, 60, 120, 120, 60], [0, 80, 80, 0, 0], color="black")

# Halfway line
ax.plot([60, 60], [0, 80], color="black", linestyle="--")

# Half of the center circle (right side)
center_circle = Arc((60, 40), 20, 20, theta1=270, theta2=90, color="black")
ax.add_patch(center_circle)

# 18-yard box
ax.add_patch(Rectangle((100.2, 21.1), 19.8, 37.8, fill=False, edgecolor="black"))
# 6-yard box
ax.add_patch(Rectangle((113.4, 30.2), 6.6, 19.6, fill=False, edgecolor="black"))
# Goal
ax.add_patch(Rectangle((119.5, 36), 0.5, 8, fill=True, color="black"))

# Corrected penalty arc (drawn outward from penalty spot)
penalty_arc = Arc((106.1, 40), height=18.3, width=18.3, angle=0, theta1=130, theta2=230, color="black")
ax.add_patch(penalty_arc)

# Plot each shot
for shot in all_shots:
    x, y = scale_coords(shot["x"], shot["y"])
    if x >= 60:  # Only plot shots in attacking half
        ax.scatter(x, y,
                   s=shot["xG"] * 1000,
                   c=colors.get(shot["result"], "gray"),
                   alpha=0.7,
                   edgecolors="black",
                   linewidths=0.5,
                   label=shot["result"] if shot["result"] not in ax.get_legend_handles_labels()[1] else "")

# Custom legend (separate from plot)
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='SavedShot', markerfacecolor='blue', markersize=10, markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', label='BlockedShot', markerfacecolor='orange', markersize=10, markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', label='MissedShots', markerfacecolor='red', markersize=10, markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', label='Goal', markerfacecolor='green', markersize=10, markeredgecolor='black')
]
ax.legend(handles=legend_elements, loc='lower left', bbox_to_anchor=(0.02, 0.02), frameon=False, title="Shot Result")

# xG marker scale key (visual indicator of marker sizes)
for i, size in enumerate([0.05, 0.1, 0.2, 0.3, 0.4]):
    ax.scatter(63 + i * 4, 74, s=size * 1000, color="gray", alpha=0.4, edgecolor="black")
ax.annotate("Low xG", (63, 76), ha="center", fontsize=8)
ax.annotate("High xG", (63 + 4 * 4, 76), ha="center", fontsize=8)
ax.annotate("xG Marker Size", (62 + 2 * 4, 78), ha="center", fontsize=9, fontweight='bold')
ax.annotate("→", (62 + 2 * 4, 76), ha="center", fontsize=14)

# Save the plot to your local directory
output_path = Path("/Users/amandadonohoe/Desktop/VSCode/prem-stats-tracker/plots/shot_map_26727_half_pitch.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.rcParams['font.family'] = 'DejaVu Sans'  # or 'Arial'
plt.savefig(output_path, dpi=300, bbox_inches="tight")

plt.show()