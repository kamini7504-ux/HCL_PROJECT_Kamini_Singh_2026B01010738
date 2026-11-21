"""
Hospital Admissions & Revenue Performance - Pie Chart Report
Input : Clean_Hospital_Revenue_Performance_RAW_Data.csv
Output: hospital_pie_report.png
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


# =================================================================== PIE
fig, axes = plt.subplots(2, 3, figsize=(20, 12.5))
fig.suptitle("Hospital Admissions – Share Analysis (Pie Charts)",
             fontsize=18, fontweight="bold")

def pie(ax, col, title, order=None):
    vc = df[col].value_counts()
    if order: vc = vc.reindex(order)
    wedges, _, autotexts = ax.pie(
        vc.values, labels=vc.index, autopct=lambda p: f"{p:.0f}%\n({round(p*n/100)})",
        startangle=90, counterclock=False, colors=PALETTE[:len(vc)],
        pctdistance=0.75, wedgeprops=dict(edgecolor="white", linewidth=1.5),
        textprops=dict(fontsize=8))
    for t in autotexts: t.set_color("white"); t.set_fontweight("bold")
    ax.set_title(title, fontsize=12, fontweight="bold")

pie(axes[0, 0], "Department", "Admissions by Department")
pie(axes[0, 1], "Payer_Type", "Payer Mix")
pie(axes[0, 2], "Ward_Type", "Ward Type", ["General", "Semi-Private", "Private", "ICU"])
pie(axes[1, 0], "Outcome", "Patient Outcomes")
pie(axes[1, 1], "Admission_Type", "Elective vs Emergency")
pie(axes[1, 2], "Gender", "Gender Split")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("hospital_pie_report.png", dpi=200, bbox_inches="tight")


plt.show()
print("Saved: hospital_pie_report.png")