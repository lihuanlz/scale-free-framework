# Build fig4_instances.png: four worked instances of the framework
# (a) Bicoid->gap scaling profile; (b) Wnt fold-change plateau/breakdown;
# (c) M3R->Ca cascade gain-distribution confinement; (d) yeast osmotic causal arm.
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()
import numpy as np
import matplotlib.pyplot as plt
import csv

BASE = r'D:\Kimi_Agent_细胞仿真工具包扩展以及具身智能20260911\05_主线纲领与设计'
fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.6))
plt.subplots_adjust(hspace=0.42, wspace=0.30, left=0.075, right=0.975, top=0.90, bottom=0.09)

BLUE, ORANGE, GREEN, GRAY = '#2166ac', '#b35806', '#1b7837', '#666666'

# ---------- (a) Bicoid scaling ----------
ax = axes[0, 0]
rows = list(csv.DictReader(open(BASE + r'\形态发生素线\data\bergmann2010_datasetS2_scaling.csv')))
dosage_style = {'1': (BLUE, 'o', r'1$\times$ bcd'), '2': (ORANGE, 's', r'2$\times$ bcd'), '4': (GREEN, '^', r'4$\times$ bcd')}
for dose, (c, m, lab) in dosage_style.items():
    xs = [float(r['100*x/L']) for r in rows if r['bcd dosage'] == dose]
    ss = [float(r['Scaling coefficient']) for r in rows if r['bcd dosage'] == dose]
    es = [float(r['68% CI']) for r in rows if r['bcd dosage'] == dose]
    ax.errorbar(xs, ss, yerr=es, fmt=m, color=c, ms=4.5, capsize=2, lw=0.8, label=lab, alpha=0.9)
ax.axhline(1.0, color='k', lw=1.0, ls='--', alpha=0.6)
ax.set_xlabel(r'boundary position  $x/L$  (% embryo length)')
ax.set_ylabel(r'scaling coefficient $S$')
ax.set_ylim(-0.08, 2.45)
ax.legend(fontsize=8, frameon=False, loc='upper right')
ax.text(0.03, 0.10, 'mid-embryo $S\\approx1$; dose-monotone $1.07\\to0.96\\to0.84$\nanchor absolute: $\\alpha=-0.18$ $[-0.48,+0.11]$ (581 embryos)',
        transform=ax.transAxes, fontsize=8, color=GRAY)
ax.set_title('a   morphogen readout (Bicoid to gap genes)', fontsize=10.5, loc='left')

# ---------- (b) Wnt plateau ----------
ax = axes[0, 1]
wr = list(csv.DictReader(open(BASE + r'\Wnt线\data\fig4F_digitized.csv')))
x = [float(r['LiCl_mM']) for r in wr]
y = [float(r['fold_change']) for r in wr]
ax.axhspan(0.95, 1.05, color=BLUE, alpha=0.12, label=r'$\pm$5% plateau band')
ax.axvspan(50, 58, color=ORANGE, alpha=0.18)
ax.plot(x, y, 'o-', color=BLUE, ms=6, lw=1.4)
ax.axhline(1.0, color='k', lw=0.8, ls='--', alpha=0.5)
ax.set_xlabel('LiCl (mM)')
ax.set_ylabel(r'fold change of $\beta$-catenin signalling')
ax.set_ylim(0, 1.35)
ax.text(52, 1.22, 'breakdown onset\n50–58 mM', fontsize=8.5, color=ORANGE, ha='left')
ax.text(6, 0.28, 'plateau 0.96–1.04 over 0–50 mM\n(fold-change readout confirmed)', fontsize=8.5, color=GRAY)
ax.set_title(r'b   Wnt/$\beta$-catenin fold-change plateau (digitised)', fontsize=10.5, loc='left')

# ---------- (c) cascade CV decomposition ----------
ax = axes[1, 0]
d = json.load(open(BASE + r'\级联线\cascade_audit_results.json'))
doses = [10, 3, 1.5, 0.75, 0.5, 0.25, 0.1]
wc = d['within_cell_CV']; ac = d['across_cell_CV']
ax.plot(doses, ac, 's-', color=ORANGE, lw=1.5, ms=5.5, label='across-cell CV (gain distribution)')
ax.plot(doses, wc, 'o-', color=BLUE, lw=1.5, ms=5.5, label='within-cell CV (5 repeats)')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'acetylcholine dose ($\mu$M)')
ax.set_ylabel('coefficient of variation')
ax.legend(fontsize=8, frameon=False, loc='center right')
ax.text(0.03, 0.04, 'per-cell rank preserved: $\\rho=0.58$–$0.90$\nEC$_{50}$ scatter across experiments: 32-fold',
        transform=ax.transAxes, fontsize=8, color=GRAY)
ax.set_title('c   cascade relay (M3R to Ca$^{2+}$, 353 cells)', fontsize=10.5, loc='left')

# ---------- (d) yeast osmotic causal arm ----------
ax = axes[1, 1]
def load(name):
    rr = list(csv.DictReader(open(BASE + r'\渗透压线\data\muzzey2009\digitized\\' + name)))
    return np.array([float(r['x']) for r in rr]), np.array([float(r['y']) for r in rr])
xm, ym = load('f5B_vol_minusPP1.csv')
xp, yp = load('f5B_vol_plusPP1.csv')
ax.plot(xm, ym, '-', color=BLUE, lw=1.8, label='control (Hog1 active)')
ax.plot(xp, yp, '-', color=ORANGE, lw=1.8, label='Hog1 inhibited (PP1)')
ax.set_xlabel('time after 0.4 M NaCl shock (min)')
ax.set_ylabel('relative cell volume')
ax.set_ylim(-0.20, 0.03)
ax.legend(fontsize=8, frameon=False, loc='upper right')
ax.text(0.50, 0.28, 'absolute-scale recovery collapses\n0.644 $\\to$ 0.070 when maintenance\nis inhibited', transform=ax.transAxes, fontsize=8, color=GRAY)
ax.set_title('d   paid reference, positive control (yeast osmotic)', fontsize=10.5, loc='left')

out = Path(__file__).with_name('fig4_instances.png')
fig.savefig(out, dpi=150, bbox_inches='tight')
print('saved', out)
