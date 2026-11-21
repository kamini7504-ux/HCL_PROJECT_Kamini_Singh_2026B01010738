"""
Hospital Admissions & Revenue Performance - Scatter Plot Report
Input : Clean_Hospital_Revenue_Performance_RAW_Data.csv
Output: hospital_scatter_report.png
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv(f"C:\Users\lenovo\OneDrive\Desktop\HCL_PROJECT\Project_HCL\Data\Clean_data\Hospital_Revenue_Performance_RAW_Data_clean.csv").drop_duplicates().reset_index(drop=True)
n = len(df)

PALETTE = ["#1f4e79", "#2e86c1", "#f39c12", "#27ae60", "#c0392b",
           "#8e44ad", "#16a085", "#e67e22", "#7f8c8d", "#5dade2"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

def style(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3); ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# =================================================================== SCATTER
fig, axes = plt.subplots(1, 3, figsize=(21, 6.5))
fig.suptitle("Hospital Admissions – Scatter Analysis", fontsize=18, fontweight="bold")
rng = np.random.default_rng(42)
jit = lambda s, w=0.12: s + rng.uniform(-w, w, len(s))   # jitter: LOS is whole days

# 1. Age vs LOS, coloured by ward type, with overall trend line
ax = axes[0]
for ward, c in zip(["General", "Semi-Private", "Private", "ICU"], PALETTE[1:5]):
    d = df[df.Ward_Type == ward]
    ax.scatter(d.Age, jit(d.Length_of_Stay_Days), s=45, alpha=0.75, c=c,
               label=ward, edgecolor="white", lw=0.5)
m, b = np.polyfit(df.Age, df.Length_of_Stay_Days, 1)
xs = np.linspace(df.Age.min(), df.Age.max(), 50)
ax.plot(xs, m * xs + b, "k--", lw=1.5,
        label=f"Trend (r = {df.Age.corr(df.Length_of_Stay_Days):.2f})")
ax.legend(frameon=False, fontsize=8)
style(ax, "Age vs Length of Stay (by Ward)", "Age (years)", "Length of Stay (days)")

# 2. Age vs LOS, coloured by outcome
ax = axes[1]
for out, c in zip(["Recovered", "Improved", "LAMA", "Referred"], [PALETTE[3], PALETTE[1], PALETTE[4], PALETTE[2]]):
    d = df[df.Outcome == out]
    ax.scatter(d.Age, jit(d.Length_of_Stay_Days), s=45, alpha=0.75, c=c,
               label=out, edgecolor="white", lw=0.5)
ax.legend(frameon=False, fontsize=8)
style(ax, "Age vs Length of Stay (by Outcome)", "Age (years)", "Length of Stay (days)")

# 3. Department bubble chart: volume vs avg LOS, bubble size = total bed-days
ax = axes[2]
g = df.groupby("Department").agg(adm=("Admission_ID", "count"),
                                 los=("Length_of_Stay_Days", "mean"),
                                 bed=("Length_of_Stay_Days", "sum"))
ax.scatter(g.adm, g.los, s=g.bed * 6, c=PALETTE[1], alpha=0.55,
           edgecolor=PALETTE[0], lw=1.2)
for dept, r in g.iterrows():
    ax.annotate(dept, (r.adm, r.los), fontsize=7.5, ha="center", va="center")
ax.margins(0.15)
style(ax, "Department: Volume vs Avg Stay (bubble = bed-days)",
      "Number of Admissions", "Average Length of Stay (days)")

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig("hospital_scatter_report.png", dpi=200, bbox_inches="tight")


plt.show()
print("Saved: hospital_scatter_report.png")