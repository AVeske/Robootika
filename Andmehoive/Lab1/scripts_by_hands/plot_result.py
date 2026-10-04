from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
data = np.loadtxt(HERE / "result.csv", delimiter=";", skiprows=1)
analog, real = data[:, 0], data[:, 1]

saturated = analog >= analog.max()
x, y = real[~saturated], analog[~saturated]
k, b = np.polyfit(x, y, 1)
r2 = 1 - np.sum((y - (k * x + b)) ** 2) / np.sum((y - y.mean()) ** 2)

plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(9, 6), dpi=150)

ax.scatter(x, y, s=45, color="#2a78d6", edgecolor="white", linewidth=0.8,
           zorder=3, label="Measurements")
ax.scatter(real[saturated], analog[saturated], s=45, color="#e34948",
           edgecolor="white", linewidth=0.8, zorder=3,
           label=f"Saturated ({analog.max():.3f})")

xs = np.linspace(real.min(), real.max(), 100)
ax.plot(xs, k * xs + b, color="#52514e", linewidth=1.5, linestyle="--", zorder=2,
        label=f"Linear fit: y = {k:.2f}x {b:+.2f}  (R² = {r2:.3f})")

ax.set_xlabel("Real", fontsize=12)
ax.set_ylabel("Analog", fontsize=12)
ax.set_title("Analog vs real", fontsize=14, fontweight="bold", loc="left", pad=12)
ax.set_ylim(top=analog.max() * 1.08)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=True, facecolor="white", edgecolor="none", loc="upper left")

fig.tight_layout()
fig.savefig(HERE / "result.png")
plt.show()
