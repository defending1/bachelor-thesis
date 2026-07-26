import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')

# --- Data from Wikipedia SVG ---
step = [
    (1965, 3.0), (1969, 3.0), (1969, 2.8074), (1978, 2.8074), (1978, 2.796),
    (1979, 2.796), (1979, 2.780), (1981, 2.780), (1981, 2.522), (1981, 2.517),
    (1981, 2.496), (1986, 2.496), (1986, 2.479), (1990, 2.479), (1990, 2.3755),
    (2010, 2.3755), (2010, 2.3737), (2012, 2.3737), (2012, 2.3729), (2014, 2.3729),
    (2014, 2.3728639), (2020, 2.3728639), (2020, 2.3728596), (2022, 2.3728596),
    (2022, 2.371866), (2024, 2.371866), (2024, 2.371552), (2024, 2.371339),
]

# SVG-to-data conversion
def s2y(x): return (x - 133.5) / 24.4 + 1970
def s2o(y): return 3.0 - (y - 28.5) / 1380

# Label data: (svg_x, svg_y, text, color, y_offset)
# y_offset is an extra vertical nudge in omega units to reduce overlap
labels_data = [
    (81.66, 90.63, 'naive', 'black', 0.0),
    (115.2, 298.9, 'Strassen', 'black', 0.0),
    (335.5, 313.9, 'Pan', 'black', 0.0),
    (359.5, 335.9, 'Bini, Capovani, Romani, Lotti', 'black', 0.0),
    (334.5, 799.8, 'Schönhage', 'black', 0.0),
    (408.6, 699.3, 'Romani', 'black', 0.015),
    (420.6, 728.4, 'Coppersmith, Winograd', 'black', 0.015),
    (530.7, 752.4, 'Strassen', 'black', 0.0),
    (628.8, 895.6, 'Coppersmith, Winograd', 'black', 0.0),
    (1117.4, 897.6, 'Stothers', 'black', 0.002),
    (1166.5, 898.6, 'Williams', 'black', 0.004),
    (1215.5, 898.6, 'Le Gall', 'black', 0.006),
    (1361.7, 898.6, 'Alman, Williams', 'black', 0.008),
    (1410.8, 900.6, 'Duan, Wu, Zhou', '#666666', 0.010),
    (1434.8, 900.6, 'Williams, Xu, Xu, Zhou', '#666666', 0.012),
    (1459.8, 900.6, 'Alman, Duan, Williams, Xu, Xu, Zhou', '#666666', 0.014),
]

labels = [(s2y(x), s2o(y) + dy, txt, col) for x, y, txt, col, dy in labels_data]

# --- Plot ---
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans', 'Helvetica'],
    'font.size': 10,
    'axes.linewidth': 0.8,
})

fig, ax = plt.subplots(figsize=(12.0, 7.0), facecolor='white')

blue = '#3366CC'

# Step path
ax.step([p[0] for p in step], [p[1] for p in step], where='post',
        color=blue, linewidth=2.0, zorder=4)

# Data points
pt_x = [step[i][0] for i in range(1, len(step), 2)]
pt_y = [step[i][1] for i in range(1, len(step), 2)]
ax.scatter(pt_x, pt_y, s=28, color=blue, zorder=5, linewidth=0.3)

# ω=3 dashed line
ax.axhline(y=3.0, color='#999999', linestyle='--', linewidth=1.0, zorder=1)

# Grid
ax.set_axisbelow(True)
ax.grid(True, which='major', color='#E8E8E8', linewidth=0.4, zorder=0)

# Limits
ax.set_xlim(1964, 2032)
ax.set_ylim(2.25, 3.10)

# Ticks
ax.set_xticks(range(1965, 2031, 5))
ax.set_yticks(np.arange(2.3, 3.05, 0.1))
ax.set_xticklabels([str(y) for y in range(1965, 2031, 5)], fontsize=8.5)
ax.set_yticklabels([f'{y:.1f}' for y in np.arange(2.3, 3.05, 0.1)], fontsize=8.5)

# Axis labels
ax.set_xlabel('Year', fontsize=11, labelpad=4)
ax.set_ylabel('ω', fontsize=14, rotation=0, labelpad=8)

# Spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#666666')
ax.spines['bottom'].set_color('#666666')
ax.tick_params(colors='#666666', size=3.5, width=0.7)

# ω=3 label
ax.text(2028, 3.045, 'ω = 3 (naive)', fontsize=8.5, color='#666666',
        ha='right', va='bottom')

# Labels with -45 degree rotation, spaced out
for yr, om, txt, col in labels:
    ax.text(yr, om, txt, fontsize=7, color=col,
            ha='center', va='center',
            rotation=-45, rotation_mode='anchor')

plt.tight_layout()
plt.savefig('/home/alberto/Data/pisa/tesi/sandbox/matrix_mult_timeline.png',
            dpi=250, bbox_inches='tight', facecolor='white')
plt.savefig('/home/alberto/Data/pisa/tesi/sandbox/matrix_mult_timeline.pdf',
            bbox_inches='tight', facecolor='white')
print('Done')
