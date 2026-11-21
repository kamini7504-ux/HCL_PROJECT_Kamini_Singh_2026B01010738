"""
Hospital Admissions & Revenue Performance - Overall Histogram Report
Input : Clean_Hospital_Revenue_Performance_RAW_Data.csv
Output: hospital_overall_report.png (and shown on screen)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CSV_PATH = (f"C:\Users\lenovo\OneDrive\Desktop\HCL_PROJECT\Project_HCL\Data\Clean_data\Hospital_Revenue_Performance_RAW_Data_clean.csv")
OUT_PATH = f"C:/Users/lenovo/OneDrive/Desktop/HCL_PROJECT/Project_HCL/Images/Chart_comparsion/Histogram.png"

# ------------------------------------------------------------------ load
df = pd.read_csv(CSV_PATH)
df = df.drop_duplicates()          # file contains 2 exact duplicate rows
n = len(df)

# ------------------------------------------------------------------ helpers
PALETTE = ["#000000", "#7bff00", "#00f7ff", "#ff9d00", "#ff0400", "#5500ff", "#af0cf5", "#01b24e", "#f806ab", "#FFFF00"]

def style(ax, title, xlabel, ylabel="Number of Admissions"):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

def label_bars(ax, bars, total=n):
    for b in bars:
        h = b.get_height()
        ax.annotate(f"{int(h)}\n({h / total:.0%})" if total else f"{int(h)}",
                    (b.get_x() + b.get_width() / 2, h),
                    ha="center", va="bottom", fontsize=8, xytext=(0, 2),
                    textcoords="offset points")

def numeric_hist(ax, series, bins, title, xlabel, color):
    counts, edges, patches = ax.hist(series, bins=bins, color=color,
                                     edgecolor="white")
    ax.axvline(series.mean(), color="#c0392b", ls="--", lw=1.5,
               label=f"Mean = {series.mean():.1f}")
    ax.axvline(series.median(), color="#27ae60", ls=":", lw=1.8,
               label=f"Median = {series.median():.1f}")
    ax.legend(frameon=False, fontsize=8)
    style(ax, title, xlabel)

def category_hist(ax, column, title, xlabel, color, rotate=0, order=None):
    vc = df[column].value_counts()
    if order:
        vc = vc.reindex(order)
    bars = ax.bar(vc.index, vc.values, color=color, edgecolor="white")
    label_bars(ax, bars)
    ax.set_ylim(0, vc.max() * 1.22)
    plt.setp(ax.get_xticklabels(), rotation=rotate,
             ha="right" if rotate else "center")
    style(ax, title, xlabel)

# ------------------------------------------------------------------ figure
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
fig, axes = plt.subplots(3, 3, figsize=(20, 16))
fig.suptitle("Hospital Admissions & Revenue Performance – Overall Analysis",
             fontsize=20, fontweight="bold", y=0.995)

# 1. Age distribution
numeric_hist(axes[0, 0], df["Age"], bins=range(0, 90, 10),
             title="Patient Age Distribution", xlabel="Age (years)",
             color=PALETTE[1])

# 2. Length of stay
numeric_hist(axes[0, 1], df["Length_of_Stay_Days"],
             bins=np.arange(1.5, 10.5, 1),
             title="Length of Stay Distribution", xlabel="Length of Stay (days)",
             color=PALETTE[5])

# 3. Department
category_hist(axes[0, 2], "Department", "Admissions by Department",
              "Department", PALETTE[0], rotate=40)

# 4. Payer type (revenue source mix)
category_hist(axes[1, 0], "Payer_Type", "Admissions by Payer Type",
              "Payer Type", PALETTE[3], rotate=15)

# 5. Ward type
category_hist(axes[1, 1], "Ward_Type", "Admissions by Ward Type",
              "Ward Type", PALETTE[7],
              order=["General", "Semi-Private", "Private", "ICU"])

# 6. Outcome
category_hist(axes[1, 2], "Outcome", "Patient Outcomes",
              "Outcome", PALETTE[6])

# 7. Admission type
category_hist(axes[2, 0], "Admission_Type", "Elective vs Emergency Admissions",
              "Admission Type", PALETTE[2])

# 8. Gender
category_hist(axes[2, 1], "Gender", "Admissions by Gender",
              "Gender", PALETTE[4])

# 9. Length of stay by ward type (overlaid histograms)
ax = axes[2, 2]
for ward, c in zip(["General", "Semi-Private", "Private", "ICU"],
                   [PALETTE[2], PALETTE[5], PALETTE[3], PALETTE[7]]):
    ax.hist(df.loc[df.Ward_Type == ward, "Length_of_Stay_Days"],
            bins=np.arange(1.5, 10.5, 1), alpha=0.55, label=ward,
            color=c, edgecolor="white")
ax.legend(frameon=False, fontsize=8)
style(ax, "Length of Stay by Ward Type", "Length of Stay (days)")

# ------------------------------------------------------------------ footer KPIs
kpi = (f"Total admissions: {n}   |   Avg age: {df.Age.mean():.1f}   |   "
       f"Avg LOS: {df.Length_of_Stay_Days.mean():.2f} days   |   "
       f"Total bed-days: {df.Length_of_Stay_Days.sum()}   |   "
       f"Emergency share: {(df.Admission_Type == 'Emergency').mean():.0%}   |   "
       f"Recovery rate: {(df.Outcome == 'Recovered').mean():.0%}")
fig.text(0.5, 0.005, kpi, ha="center", fontsize=11,
         bbox=dict(boxstyle="round,pad=0.5", fc="#eaf2f8", ec="#1f4e79"))

plt.tight_layout(rect=[0, 0.03, 1, 0.98])
plt.savefig(OUT_PATH, dpi=200, bbox_inches="tight")
plt.show()
print(f"Saved: {OUT_PATH}")
