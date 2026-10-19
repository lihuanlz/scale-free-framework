# Build fig4_instances.png: four worked instances of the framework
# (a) Bicoid->gap scaling profile; (b) Wnt fold-change plateau/breakdown;
# (c) M3R->Ca cascade gain-distribution confinement; (d) yeast osmotic causal arm.
# Drawn at the final printed width (159 mm text block) so that every label is
# at its nominal point size once the figure is placed in the manuscript.
import json, csv
from pathlib import Path

import matplotlib
matplotlib.rcParams.update({"font.size": 6.5, "axes.linewidth": 0.5,
                            "pdf.fonttype": 42, "ps.fonttype": 42})
import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
DATA = REPO / "data_external"
RESULTS = REPO / "results"

fig, axes = plt.subplots(2, 2, figsize=(6.27, 4.9))
plt.subplots_adjust(hspace=0.55, wspace=0.28, left=0.085, right=0.985, top=0.93, bottom=0.105)

BLUE, ORANGE, GREEN, GRAY = '#2166ac', '#b35806', '#1b7837', '#666666'

# ---------- (a) Bicoid scaling ----------
ax = axes[0, 0]
rows = list(csv.DictReader(open(DATA / "bergmann2010" / "bergmann2010_datasetS2_scaling.csv", encoding="utf-8")))
dosage_style = {'1': (BLUE, 'o', r'1$\times$'), '2': (ORANGE, 's', r'2$\times$'), '4': (GREEN, '^', r'4$\times$')}
for dose, (c, m, lab) in dosage_style.items():
    xs = [float(r['100*x/L']) for r in rows if r['bcd dosage'] == dose]
    ss = [float(r['Scaling coefficient']) for r in rows if r['bcd dosage'] == dose]
    es = [float(r['68% CI']) for r in rows if r['bcd dosage'] == dose]
    ax.errorbar(xs, ss, yerr=es, fmt=m, color=c, ms=2.6, capsize=1.2, lw=0.6,
                elinewidth=0.5, label=lab, alpha=0.9)
ax.axhline(1.0, color='k', lw=0.7, ls='--', alpha=0.6)
ax.set_xlabel(r'boundary position $x/L$ (% EL)')
ax.set_ylabel(r'scaling coefficient $S$')
ax.set_ylim(-0.08, 2.45)
ax.legend(fontsize=6, frameon=False, loc='upper right', handletextpad=0.3, borderpad=0.2)
ax.text(0.03, 0.06, r'$\alpha=-0.18\ [-0.48,\,0.11]$' + '\n' + r'581 embryos',
        transform=ax.transAxes, fontsize=5.8, color=GRAY)
ax.set_title('a   morphogen readout', fontsize=7, loc='left', pad=3)

# ---------- (b) Wnt plateau ----------
ax = axes[0, 1]
wr = list(csv.DictReader(open(RESULTS / "fig4F_digitized.csv", encoding="utf-8")))
x = [float(r['LiCl_mM']) for r in wr]
y = [float(r['fold_change']) for r in wr]
ax.axhspan(0.95, 1.05, color=BLUE, alpha=0.12, label=r'$\pm$5%')
ax.axvspan(48.6, 58.1, color=ORANGE, alpha=0.18)
ax.plot(x, y, 'o-', color=BLUE, ms=3.2, lw=1.0)
ax.axhline(1.0, color='k', lw=0.6, ls='--', alpha=0.5)
ax.set_xlabel('LiCl (mM)')
ax.set_ylabel(r'fold change, $\beta$-catenin')
ax.set_ylim(0, 1.35)
ax.text(52, 1.20, 'breakdown\n48.6-58.1 mM', fontsize=5.6, color=ORANGE, ha='left', va='top')
ax.text(9, 0.20, 'plateau 0.96-1.04\n7-49 mM', fontsize=5.6, color=GRAY)
ax.legend(fontsize=5.6, frameon=False, loc='upper left', handletextpad=0.3, borderpad=0.2)
ax.set_title(r'b   Wnt fold-change plateau', fontsize=7, loc='left', pad=3)

# ---------- (c) cascade CV decomposition ----------
ax = axes[1, 0]
d = json.load(open(RESULTS / "cascade_audit_results.json", encoding="utf-8"))
doses = [10, 3, 1.5, 0.75, 0.5, 0.25, 0.1]
wc = d['within_cell_CV']; ac = d['across_cell_CV']
ax.plot(doses, ac, 's-', color=ORANGE, lw=1.0, ms=3.0, label='across-cell CV')
ax.plot(doses, wc, 'o-', color=BLUE, lw=1.0, ms=3.0, label='within-cell CV')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel(r'acetylcholine ($\mu$M)')
ax.set_ylabel('coefficient of variation')
ax.legend(fontsize=5.8, frameon=False, loc='center right', handletextpad=0.3, borderpad=0.2)
ax.text(0.03, 0.05, r'$\rho=0.58$–$0.90$; EC$_{50}$ 32-fold', transform=ax.transAxes,
        fontsize=5.6, color=GRAY)
ax.set_title('c   cascade relay (353 cells)', fontsize=7, loc='left', pad=3)

# ---------- (d) yeast osmotic causal arm ----------
ax = axes[1, 1]
def load(name):
    rr = list(csv.DictReader(open(DATA / "muzzey2009" / "digitized" / name, encoding="utf-8")))
    return np.array([float(r['x']) for r in rr]), np.array([float(r['y']) for r in rr])
xm, ym = load('f5B_vol_minusPP1.csv')
xp, yp = load('f5B_vol_plusPP1.csv')
ax.plot(xm, ym, '-', color=BLUE, lw=1.0, label='Hog1 active')
ax.plot(xp, yp, '-', color=ORANGE, lw=1.0, label='Hog1 inhibited')
ax.set_xlabel('time after 0.4 M NaCl (min)')
ax.set_ylabel('relative cell volume')
ax.set_ylim(-0.20, 0.03)
ax.legend(fontsize=5.8, frameon=False, loc='upper right', handletextpad=0.3, borderpad=0.2)
ax.text(0.30, 0.16, 'recovery collapses\n0.644 $\\to$ 0.070', transform=ax.transAxes,
        fontsize=5.6, color=GRAY)
ax.set_title('d   yeast osmotic control', fontsize=7, loc='left', pad=3)

out = Path(__file__).with_name('fig4_instances.png')
fig.savefig(out, dpi=400, bbox_inches='tight', pad_inches=0.015)
print('saved', out)
