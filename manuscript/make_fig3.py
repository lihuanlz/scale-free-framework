# Build fig3_pdpc_full.png: extended analysis of the covalent cycle (framework paper).
# Adapted from _github/cell-communication-audit/04_code/ed_scripts/edfig2.py with
# layout fixes: panel-a legend moved off the curves, panel e/f titles shortened
# (they ran into each other), no suptitle.
import sys, os
from pathlib import Path
import matplotlib
matplotlib.rcParams.update({"font.size": 8, "axes.linewidth": 0.6,
                            "pdf.fonttype": 42, "ps.fonttype": 42})
import numpy as np
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
BLUE, VERM = '#2166ac', '#b35806'

u = np.linspace(1e-7, 1 - 1e-7, 4000)

def xi_of_u(u, k1, k2):
    return u / (1 - u) * (k1 + 1 - u) / (k2 + u)

fig, axs = plt.subplots(2, 3, figsize=(10.8, 5.6))
plt.subplots_adjust(hspace=0.52, wspace=0.34, left=0.06, right=0.985, top=0.88, bottom=0.10)
axs = axs.ravel()

# ---- a: GK curve family ----
ax = axs[0]
kappas = [0.001, 0.005, 0.01, 0.05, 0.5, 1.0]
cols = plt.cm.viridis(np.linspace(0, 0.9, len(kappas)))
for k, c in zip(kappas, cols):
    xv = xi_of_u(u, k, k)
    ax.plot(xv, u, color=c, lw=1.2, label=rf"$\kappa$ = {k:g}, $n_H$ = {1+1/(2*k):.4g}")
ax.set_xscale("log"); ax.set_xlim(1e-2, 1e3)
ax.set_xlabel(r"activity ratio $\xi$"); ax.set_ylabel("modified fraction $u$")
ax.set_title("Goldbeter--Koshland curve family", fontsize=8)
ax.legend(fontsize=5.6, loc="lower right", framealpha=0.95)

# ---- b: group-action invariance ----
ax = axs[1]
k0 = 0.01
x0 = xi_of_u(u, k0, k0)
ax.plot(x0, u, color="0.2", lw=1.8, label=r"reference ($K_m$, $S_T$)")
ax.plot(xi_of_u(u, 5 * k0, 5 * k0), u, "o", ms=1.4, color=VERM, mfc="none",
        label=r"($K_m$, $S_T$) $\times$5 action")
ax.set_xscale("log"); ax.set_xlim(1e-2, 1e3)
ax.set_xlabel(r"$\xi$"); ax.set_ylabel("$u$")
ax.set_title(r"group action: curves coincide, max $|\Delta u| = 0$", fontsize=8)
ax.text(0.03, 0.58, "four generators verified:\n0, 0, 0, 0 (pure actions)\n0, 2.2e-16, 0, 0 (mixed rate-enzyme)\n"
        "counterexample: 1.45e-1", transform=ax.transAxes, fontsize=5.2, color="0.3", va="top")
ax.legend(fontsize=5.4, loc="lower right")

# ---- c: Fisher condition numbers (recomputed: 20 pts / 3 decades, sigma = 0.03) ----
ax = axs[2]
xj = np.logspace(-1.5, 1.5, 20)
sig = 0.03
kg = np.logspace(np.log10(0.005), 0, 9)
chi_shape, chi_abs = [], []
eps_fd = 1e-6

def uu(x, kk):
    out = np.empty_like(np.atleast_1d(x), dtype=float)
    for i, xx in enumerate(np.atleast_1d(x)):
        lo, hi = 1e-12, 1 - 1e-12
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if xi_of_u(mid, kk, kk) < xx:
                lo = mid
            else:
                hi = mid
        out[i] = 0.5 * (lo + hi)
    return out

for k in kg:
    d_c = (uu(xj * np.exp(eps_fd), k) - uu(xj * np.exp(-eps_fd), k)) / (2 * eps_fd)
    d_k = (uu(xj, k * np.exp(eps_fd)) - uu(xj, k * np.exp(-eps_fd))) / (2 * eps_fd)
    J = np.vstack([d_c, d_k]).T / sig
    F = J.T @ J
    ev = np.linalg.eigvalsh(F)
    chi_shape.append(ev[-1] / max(ev[0], 1e-300))
    u0a = uu(xj, k)
    d_km = (uu(xj, k * np.exp(eps_fd)) - u0a) / eps_fd
    d_st = (uu(xj, k * np.exp(-eps_fd)) - u0a) / eps_fd
    Ja = np.vstack([d_c, d_km, d_st]).T / sig
    Fa = Ja.T @ Ja
    eva = np.sort(np.abs(np.linalg.eigvalsh(Fa)))
    chi_abs.append(eva[-1] / max(eva[0], 1e-300))
ax.plot(kg, chi_shape, "o-", color=BLUE, ms=3.5, label=r"shape block ($\ln c$, $\ln\kappa$)")
ax.plot(kg, chi_abs, "s--", color=VERM, ms=3.5, label=r"absolute block ($\ln c$, $\ln K_m$, $\ln S_T$)")
ax.set_xscale("log"); ax.set_yscale("log")
ax.axhspan(19, 33, color=BLUE, alpha=0.10)
ax.text(0.008, 6, "archived range 19--33", fontsize=5.2, color=BLUE)
ax.set_xlabel(r"$\kappa$"); ax.set_ylabel(r"Fisher condition number $\chi$")
ax.set_title("shape identifiable, scale not (exact zero direction)", fontsize=8)
ax.legend(fontsize=5.2, loc="center left")

# ---- d: asymmetric Michaelis triple ----
ax = axs[3]
k2 = 0.01
for r, c in zip([0.1, 0.3, 1.0, 3.0, 10.0], plt.cm.plasma(np.linspace(0.1, 0.85, 5))):
    ax.plot(xi_of_u(u, r * k2, k2), u, color=c, lw=1.2, label=f"r = {r:g}")
ax.set_xscale("log"); ax.set_xlim(1e-2, 1e3)
ax.set_xlabel(r"$\xi$"); ax.set_ylabel("$u$")
ax.set_title(r"asymmetric Michaelis curves ($\kappa_2$ = 0.01)", fontsize=8)
ax.legend(fontsize=5.2, loc="upper left")
axin = ax.inset_axes([0.45, 0.13, 0.52, 0.42])
rr = np.logspace(np.log10(0.03), np.log10(30), 60)
nH = 4 / (4 - 1 / (rr * k2 + 0.5) - 1 / (k2 + 0.5))
axin.plot(rr, nH, color=BLUE, lw=1.0)
axin.axhline(51.0, color="0.4", ls="--", lw=0.6)
for r0, n0 in [(0.03, 98.973), (30, 5.068)]:
    axin.plot(r0, n0, "o", ms=3.5, color=VERM)
    axin.annotate(f"{n0:.1f}", (r0, n0), textcoords="offset points", xytext=(4, 2), fontsize=4.5)
axin.set_xscale("log")
axin.set_xlabel(r"$r = \kappa_1/\kappa_2$", fontsize=5); axin.set_ylabel(r"$n_H$ closed form", fontsize=5)
axin.tick_params(labelsize=4.5)
for sp in axin.spines.values():
    sp.set_linewidth(0.4)

# ---- e: one-sided protocol (SI S2.3 table) ----
ax = axs[4]
kt = np.array([0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0])
ci = np.array([2551.92, 5.16, 2.39, 1.33, 1.27, 1.31, 1.42])
nh = np.array([501, 101, 51, 11, 6, 2, 1.5])
ax.plot(kt, ci, "o-", color=VERM, ms=4, label="95% CI inflation")
ax.axvspan(10**(-3.4), 0.01, color="0.5", alpha=0.12)
ax.text(0.00135, 8, "deep zero-order:\nonly one-sided\nupper bound\nreportable", fontsize=5.2, color="0.35")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"$\kappa$"); ax.set_ylabel("95% CI inflation factor")
ax2 = ax.twinx()
ax2.plot(kt, nh, "s--", color=BLUE, ms=3.5, label="$n_H$")
ax2.set_yscale("log"); ax2.set_ylabel(r"Hill coefficient $n_H$", color=BLUE)
ax2.tick_params(axis="y", labelcolor=BLUE, labelsize=6)
ax2.spines["right"].set_linewidth(0.6)
ax.set_title(r"one-sided protocol below $\kappa \sim 0.01$", fontsize=8)
ax.legend(fontsize=5.2, loc="upper right")

# ---- f: positive-feedback switch ----
ax = axs[5]
kap = 0.05
M = xi_of_u(u, kap, kap)
dM = np.gradient(M, u)
den = M - u * dM
mask = den > 0
gstar = np.min(dM[mask] / den[mask])
for g, c in zip([0, 2, 5, 10, 20], plt.cm.cividis(np.linspace(0.05, 0.9, 5))):
    xig = M / (1 + g * u)
    ax.plot(xig, u, color=c, lw=1.2, label=f"g = {g}")
ax.set_xscale("log"); ax.set_xlim(1e-2, 30)
ax.set_xlabel(r"activity ratio $\xi$"); ax.set_ylabel("$u$")
ax.set_title(rf"positive-feedback switch: $g^*$ = {gstar:.3f}", fontsize=8)
ax.legend(fontsize=5.2, loc="lower right")
axin = ax.inset_axes([0.40, 0.57, 0.57, 0.41])
ufine = np.linspace(1e-6, 1 - 1e-6, 60000)
Mfine = xi_of_u(ufine, kap, kap)

def dlnxi_ana(uu_, g):
    return 1/uu_ + 1/(1-uu_) - 1/(kap+1-uu_) - 1/(kap+uu_) - g/(1+g*uu_)

gg = np.linspace(0.45, 20, 120)
widths = []
for g in gg:
    xig = Mfine / (1 + g * ufine)
    sgn = np.sign(dlnxi_ana(ufine, g))
    flips = np.where(np.diff(sgn) != 0)[0]
    widths.append(np.log10(xig[flips[0]] / xig[flips[-1]]) if len(flips) >= 2 else np.nan)
axin.plot(gg, widths, color=VERM, lw=1.0)
axin.axvspan(10, 20, color=BLUE, alpha=0.10)
axin.axhspan(0.44, 0.58, xmin=0, xmax=1, color="0.5", alpha=0.15)
axin.text(15, 0.09, "archived 0.44--0.58 dex\nat g = 10--20", fontsize=4.5, ha="center", color="0.35")
axin.text(1.2, 0.60, r"p42 MAPK $n_H$ $\geq$ 35",
          fontsize=4.5, ha="left", va="top", color=BLUE)
axin.set_xlim(0.45, 20); axin.set_ylim(0, 0.65)
axin.set_xlabel("feedback gain g", fontsize=5); axin.set_ylabel("hysteresis width (dex)", fontsize=5)
axin.tick_params(labelsize=4.5)
for sp in axin.spines.values():
    sp.set_linewidth(0.4)

for i, ax in enumerate(axs):
    ax.text(-0.16, 1.04, "abcdef"[i], transform=ax.transAxes, fontsize=10,
            fontweight="bold", va="top", ha="left")

fig.savefig(os.path.join(HERE, "fig3_pdpc_full.png"), dpi=150)
print("saved", os.path.join(HERE, "fig3_pdpc_full.png"), "g* =", f"{gstar:.3f}")
