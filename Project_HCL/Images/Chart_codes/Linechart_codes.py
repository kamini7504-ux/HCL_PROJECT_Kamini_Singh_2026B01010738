"""
Hospital Admissions & Revenue Performance - Line Graph Report
Input : Clean_Hospital_Revenue_Performance_RAW_Data.csv
Output: hospital_line_report.png
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
OUT_PATH =( f"C:\Users\lenovo\OneDrive\Desktop\HCL_PROJECT\Project_HCL\Images\Chart_comparsion\Linechart.png")
df = pd.read_csv(f"C:\Users\lenovo\OneDrive\Desktop\HCL_PROJECT\Project_HCL\Data\Clean_data\Hospital_Revenue_Performance_RAW_Data_clean.csv").drop_duplicates().reset_index(drop=True)
n = len(df)
# Age groups used by the line graphs
bins = [0, 12, 25, 40, 55, 70, 100]
labels = ["0-12", "13-25", "26-40", "41-55", "56-70", "71+"]
df["Age_Group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=True)

PALETTE = ["#1f4e79", "#2e86c1", "#f39c12", "#27ae60", "#c0392b",
           "#8e44ad", "#16a085", "#e67e22", "#7f8c8d", "#5dade2"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

def style(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3); ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# =================================================================== LINE
fig, axes = plt.subplots(2, 2, figsize=(16, 11))
fig.suptitle("Hospital Admissions – Trend Analysis (Line Graphs)",
             fontsize=18, fontweight="bold")

# 1. Admissions by age group, split by gender
ax = axes[0, 0]
for gen, c in zip(["Male", "Female"], [PALETTE[0], PALETTE[7]]):
    s = df[df.Gender == gen].groupby("Age_Group", observed=False).size()
    ax.plot(labels, s.values, marker="o", lw=2.2, c=c, label=gen)
    for x, y in zip(labels, s.values):
        ax.annotate(y, (x, y), xytext=(0, 6), textcoords="offset points",
                    ha="center", fontsize=8, color=c)
ax.legend(frameon=False)
style(ax, "Admissions by Age Group & Gender", "Age Group", "Number of Admissions")

# 2. Avg LOS by age group, split by admission type
ax = axes[0, 1]
for typ, c in zip(["Elective", "Emergency"], [PALETTE[3], PALETTE[4]]):
    s = (df[df.Admission_Type == typ]
         .groupby("Age_Group", observed=False)["Length_of_Stay_Days"].mean())
    ax.plot(labels, s.values, marker="s", lw=2.2, c=c, label=typ)
ax.legend(frameon=False)
style(ax, "Average Length of Stay by Age Group", "Age Group", "Avg Length of Stay (days)")

# 3. LOS frequency polygon by payer type
ax = axes[1, 0]
days = np.arange(df.Length_of_Stay_Days.min(), df.Length_of_Stay_Days.max() + 1)
for pay, c in zip(df.Payer_Type.unique(), PALETTE):
    s = (df[df.Payer_Type == pay].Length_of_Stay_Days
         .value_counts().reindex(days, fill_value=0))
    ax.plot(days, s.values, marker="o", lw=2, c=c, label=pay)
ax.legend(frameon=False, fontsize=8)
style(ax, "Length-of-Stay Profile by Payer Type", "Length of Stay (days)", "Number of Admissions")

# 4. Cumulative % of admissions by LOS
ax = axes[1, 1]
for typ, c in zip(["Elective", "Emergency"], [PALETTE[3], PALETTE[4]]):
    x = np.sort(df[df.Admission_Type == typ].Length_of_Stay_Days.values)
    ax.step(x, np.arange(1, len(x) + 1) / len(x) * 100, where="post",
            lw=2.2, c=c, label=typ)
x = np.sort(df.Length_of_Stay_Days.values)
ax.step(x, np.arange(1, n + 1) / n * 100, where="post", lw=2.5, c="k", ls="--", label="Overall")
ax.axhline(50, c="grey", lw=0.8, ls=":")
ax.legend(frameon=False)
style(ax, "Cumulative % of Admissions by Length of Stay",
      "Length of Stay (days)", "Cumulative % of Admissions")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(OUT_PATH, dpi=200, bbox_inches="tight")


plt.show()
print("Saved": OUT_PATH)