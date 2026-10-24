"""Lab 1 noise analysis: sample rate, noise in LSB and kPa, Pa per ADC step, spectra.

usage: python noise_analysis.py
reads ../data/l1_*.csv, writes ../Docs/l1_spectrum.png and prints a table
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, welch

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
DOCS = HERE.parent / "Docs"
FS = 100.0            # Hz
SENS_MV_KPA = 6.43    # MPX5700AP: 5 V * 0.0012858 = 6.43 mV/kPa

FILES = {
    "pump off": "l1_noise_off.csv",
    "pump on": "l1_noise_on.csv",
    "servos off": "l1_noise_servo_off.csv",
}


def load(name, config="raw"):
    """Returns columns of one file, only raw sensor rows."""
    path = DATA / name
    head = path.open().readline().strip().split(",")
    rows = np.genfromtxt(path, delimiter=",", skip_header=1, dtype=str)
    col = {h: rows[:, i] for i, h in enumerate(head)}
    if "config" in col:
        keep = col["config"] == config
        col = {h: c[keep] for h, c in col.items()}
    t = col["t_ms"].astype(float) / 1000
    return {
        "t": t - t[0],
        "adc": col["adc"].astype(float),
        "v": col["volts"].astype(float),
        "p": col["p_kpa"].astype(float),
        "pump": col["pump"].astype(int),
        "has_raw": "config" in head,
    }


def steady(d, pump):
    """Only rows with this pump state, and not the first 2 s after it changed."""
    keep = d["pump"] == pump
    change = np.r_[0, np.flatnonzero(np.diff(d["pump"])) + 1]
    for i in change:
        keep &= ~((d["t"] >= d["t"][i]) & (d["t"] < d["t"][i] + 2.0))
    return {k: (v[keep] if isinstance(v, np.ndarray) else v) for k, v in d.items()}


# --- 1. sample rate check (10 s log)
d = load("l1_10s.csv")
dur = d["t"][-1]
print(f"l1_10s.csv: {len(d['t'])} rows in {dur:.2f} s -> {len(d['t']) / dur:.1f} Hz, "
      f"{len(d['t']) / dur * 10:.0f} rows per 10 s, mean {d['v'].mean():.3f} V")

# --- 2. Pa per ADC step, from volts vs code over all logs
v_all, a_all = [], []
for name in ["l1_10s.csv"] + list(FILES.values()):
    x = load(name)
    if x["has_raw"]:
        v_all.append(x["v"]); a_all.append(x["adc"])
v_all, a_all = np.concatenate(v_all), np.concatenate(a_all)
mv_per_step = np.polyfit(a_all, v_all, 1)[0] * 1000
print(f"ADC step: {mv_per_step:.3f} mV measured (3.3 V / 4096 = 0.806 mV ideal) -> "
      f"{mv_per_step / SENS_MV_KPA * 1000:.0f} Pa per step")

# --- 3. noise and spectra
fig, ax = plt.subplots(figsize=(9, 5), dpi=130)
print(f"\n{'case':12s} {'rows':>5s} {'mean V':>7s} {'std LSB':>8s} {'std kPa':>8s}  peaks (Hz)")
for label, name in FILES.items():
    x = load(name)
    if not x["has_raw"]:
        print(f"{label:12s} {name}: no raw channel (recorded with the Lab1 script), skipped")
        continue
    x = steady(x, 1 if label == "pump on" else 0)
    p = x["p"] - x["p"].mean()
    f, psd = welch(p, fs=FS, nperseg=512)
    peaks, _ = find_peaks(psd, height=psd[1:].mean() * 5)
    top = sorted(peaks, key=lambda i: psd[i], reverse=True)[:4]
    print(f"{label:12s} {len(p):5d} {x['v'].mean():7.3f} {x['adc'].std():8.2f} {p.std():8.2f}  "
          + ", ".join(f"{f[i]:.1f}" for i in sorted(top)))
    ax.semilogy(f, psd, label=f"{label} (std {p.std():.2f} kPa)")

ax.set_xlabel("Frequency, Hz")
ax.set_ylabel("PSD, kPa²/Hz")
ax.set_title("Lab 1, raw sensor noise (Welch, 100 Hz)", loc="left")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
DOCS.mkdir(exist_ok=True)
fig.savefig(DOCS / "l1_spectrum.png")
print("\nsaved", DOCS / "l1_spectrum.png")
