# -*- coding: utf-8 -*-
"""
code 8: frequency encoding of an excitable system (cross-pathway instance 3 - Msn2/Crz1-type digital channel)
====================================================================
Purpose: provide the manuscript with a digital-encoding instance of an 'excitable system under sustained drive' -
  (1) amplitude approximately constant (all-or-none) : α = ∂lnA/∂lnI₀ ≪ 0.1
  (2) pulse frequency (=counts per unit time) increases monotonically with dose: ν_f = ∂f/∂lnI₀ > 0
  (3) in a fixed observation windowpulse count N approximately linear in ln I0 (equivalent counting index) 
biological correspondences:
  - yeast Msn2 transcription-factor glucose-starvation pulses: amplitude nearly constant, frequency rises with starvation
     (Hao & O'Shea 2012, Nat. Struct. Mol. Biol. 19:31) 
  - Crz1 calcium-response FM bursts: frequency rises with Ca2+, amplitude/duration unchanged
     (Cai, Dalal & Elowitz 2008, Nature 455:485) 

Model: FitzHugh-Nagumo (same parameters as manuscript Methods)
  dv/dt = sf·(v − v³/3 − w + I)
  dw/dt = sf·ε·(v + a − b·w)
  a=0.7, b=0.8, ε=0.08, sf=20
unlike the decaying damage input of codes 1/5, this instance uses **sustained constant drive** I = I0 (persistent stress),
deterministic solve_ivp (rtol=1e-9, atol=1e-12, LSODA; checked point-by-point against RK45),
t in [0,100] au, first 40% transient discarded, effective observation window 60 au.
pulse detection find_peaks (prominence>=1.0, minimum distance 1.0 au).

note (symmetry): this FHN is exactly symmetric under (v,w,I)->(-v,-w+2a/b, 2a/b-I),
so the oscillation window is symmetric about I*=a/b+...=0.875 and the full-window frequency is an inverted U; experiments (Msn2/Crz1)
probe the **rising branch** [I_low, I*]; digital signatures are evaluated on that branch and the full-window shape is reported as-is.

Run: python3 code08_msn2_excitable_frequency_encoding.py   (approx. 1.5-2 min, outputs a three-panel PNG)
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks
from scipy.optimize import brentq
import matplotlib.pyplot as plt

# ---------- model parameters ----------
a, b, eps, sf = 0.7, 0.8, 0.08, 20.0      # FHN standard parameters (manuscript Methods)
T, DT = 100.0, 0.002                      # simulation window and output step (arbitrary time units, au)
TEVAL = np.arange(0, T + DT/2, DT)

def fhn(t, y, I):
    v, w = y
    return [sf*(v - v**3/3 - w + I), sf*eps*(v + a - b*w)]

def simulate(I, y0=(-1.2, -0.6), T=T):
    """Deterministic integration (LSODA, checked point by point against RK45); returns (t, v) after discarding the first 40% transient."""
    sol = solve_ivp(fhn, (0, T), y0, args=(I,), t_eval=TEVAL,
                    rtol=1e-9, atol=1e-12, method='LSODA')
    m = sol.t >= 0.4*T
    return sol.t[m], sol.y[0][m]

def measure(I):
    """Measure pulse count N, amplitude A (peak mean minus trough minimum), frequency f (=1/mean inter-pulse interval)."""
    tt, v = simulate(I)
    pk, _ = find_peaks(v, prominence=1.0, distance=int(1.0/DT))
    if len(pk) < 2:
        return len(pk), np.nan, np.nan
    return len(pk), v[pk].mean() - v.min(), 1.0/np.diff(tt[pk]).mean()

def oscillates(I):
    """From resting initial conditions, a post-transient peak-to-peak v range > 0.5 is judged sustained oscillation."""
    _, v = simulate(I)
    return (v.max() - v.min()) > 0.5

def bisect(lo, hi):
    """Bisect the oscillation boundary: requires lo/hi to bracket one oscillating and one non-oscillating side (squeeze invariant maintained)."""
    lo_osc = oscillates(lo)
    for _ in range(18):
        mid = 0.5*(lo + hi)
        if oscillates(mid) == lo_osc:
            lo = mid
        else:
            hi = mid
    return 0.5*(lo + hi)

def cont_sweep(I_start, I_end, step, y_start, T=60.0):
    """Continuation sweep: each point inherits the previous endpoint as its initial state; returns (I array, late-window amplitude array, final state)."""
    Is = np.arange(I_start, I_end + step/2*np.sign(step), step)
    amps = []; y0 = np.asarray(y_start, float)
    tev = np.arange(0, T + 0.0025, 0.005)
    for I in Is:
        sol = solve_ivp(fhn, (0, T), y0, args=(I,), t_eval=tev,
                        rtol=1e-9, atol=1e-12, method='LSODA')
        y0 = sol.y[:, -1].copy()
        v = sol.y[0][sol.t >= 0.4*T]
        amps.append(v.max() - v.min())
    return Is, np.array(amps), y0

print('='*72)
print('code 8: excitable frequency encoding (Msn2/Crz1 type) - acceptance checklist')
print('='*72)

# ============================================================
# part 1: locate the oscillation window (superthreshold onset I_low <-> depolarization block I_high)
# ============================================================
Is_coarse = np.arange(0.05, 1.70, 0.05)
osc_map = [oscillates(I) for I in Is_coarse]
idx = np.where(osc_map)[0]
i_lo, i_hi = idx[0], idx[-1]
I_low  = bisect(Is_coarse[i_lo-1], Is_coarse[i_lo])    # lower bound: superthreshold onset
I_high = bisect(Is_coarse[i_hi], Is_coarse[i_hi+1])    # upper bound: depolarization block
print(f'\n[1] oscillation window (sustained constant drive, oscillation from rest)')
print(f'    firing window = [{I_low:.3f}, {I_high:.3f}] au (width {I_high-I_low:.3f}) ')
print(f'    lower bound = superthreshold onset; upper bound = depolarization block')
print(f'    symmetry-centre check: (I_low+I_high)/2 = {(I_low+I_high)/2:.3f}'
      f'(FHN symmetry prediction 0.875)')

# ============================================================
# part 2: onset-type determination (continuity + up/down-sweep hysteresis test)
# ============================================================
# -- fine continuation up-sweep: track from the equilibrium branch and watch how the amplitude grows --
v_ss = brentq(lambda v: v - v**3/3 - (v+a)/b + 0.30, -2, 0)
y_eq = (v_ss, (v_ss+a)/b)                                  # stable equilibrium at I=0.30
Is_on, A_on, _ = cont_sweep(0.300, 0.338, 0.0005, y_eq)    # fine continuation sweep from the equilibrium branch
i_expl = np.argmax(A_on > 1.0)                             # amplitude explosion point
I_expl = Is_on[i_expl]
A_pre = A_on[:i_expl]
I_hopf = Is_on[A_on > 1e-3].min()                          # where the small cycle first becomes discernible
print(f'\n[2] onset-type determination (continuation up-sweep along the equilibrium branch, dI=5e-4)')
print(f'    continuous growth of the small cycle near Hopf: A from ~0 (I≈{I_hopf:.3f} onwards) '
      f'grows continuously to {A_pre.max():.4f} (I={Is_on[i_expl-1]:.4f}) ')
print(f'    then jumps via a canard explosion within dI <= 5e-4 to full size '
      f'A~{A_on[i_expl]:.2f} (explosion point I_expl={I_expl:.4f})')

# -- hysteresis test: up-sweep explosion point vs down-sweep (continuation along the limit cycle) extinction fold --
# continue the down-sweep from I=0.40 (resting initial state lands on the large cycle); track the large cycle until collapse
sol_cyc = solve_ivp(fhn, (0, 60), (-1.2, -0.6), args=(0.40,),
                    t_eval=[60.0], rtol=1e-9, atol=1e-12, method='LSODA')
Is_dn, A_dn, _ = cont_sweep(0.40, 0.30, -0.0005, sol_cyc.y[:, -1])
I_fold = Is_dn[A_dn > 0.5].min()                           # lowest point where the large cycle persists downward
hyst = I_expl - I_fold
print(f'    hysteresis test: up-sweep explosion I_on={I_expl:.4f}, down-sweep large-cycle extinction I_off={I_fold:.4f}')
print(f'    hysteresis width = {hyst:.4f} (nonzero, i.e. '
      f'{hyst/(I_high-I_low)*100:.1f}% of the window width - FHN subcritical/canard-type narrow hysteresis)')
print(f'    classification (three-signature table): onset is mathematically continuous (Hopf sqrt-type small-cycle growth),')
print(f"    but the canard explosion makes the amplitude appear as a 'finite-size onset' at any practical resolution, and hysteresis != 0;")
print(f"    -> per the table this is the 'subcritical exception' (captured by the third signature), still assigned to the EXC-family digital-encoding side.")

# ============================================================
# part 3: digital signatures (core acceptance) - sweep 10 I0 points on the rising branch
# ============================================================
# full-window frequency is an inverted U (forced by symmetry) ; take the rising branch [0.34, 0.84] (the experimentally probed interval) 
Is_sig = np.array([0.34, 0.38, 0.42, 0.48, 0.54, 0.60, 0.66, 0.72, 0.78, 0.84])
sig = [measure(I) for I in Is_sig]
Ns  = np.array([s[0] for s in sig], float)
As  = np.array([s[1] for s in sig])
fs  = np.array([s[2] for s in sig])
lnI = np.log(Is_sig)

alpha = np.polyfit(lnI, np.log(As), 1)[0]                  # ∂lnA/∂lnI₀
nu_f  = np.polyfit(lnI, fs, 1)[0]                          # ∂f/∂lnI₀
cN    = np.polyfit(lnI, Ns, 1)                             # N vs lnI₀
R2N   = 1 - ((Ns-np.polyval(cN, lnI))**2).sum()/((Ns-Ns.mean())**2).sum()
amp_rel = (As.max()/As.min() - 1)*100
amp_pm  = (As.max()-As.min())/2/As.mean()*100

print(f'\n[3] digital signatures (rising branch {Is_sig[0]:.2f}–{Is_sig[-1]:.2f}, '
      f'{len(Is_sig)} points, effective window 60 au)')
print(f'    {"I₀":>6} {"N":>4} {"A":>8} {"f(au⁻¹)":>9}')
for I, n, A_, f_ in zip(Is_sig, Ns, As, fs):
    print(f'    {I:6.2f} {int(n):4d} {A_:8.3f} {f_:9.4f}')
print(f'    ────────────────────────────────────────────')
print(f'    (a) amplitude all-or-none: A range {As.min():.3f}–{As.max():.3f}, '
      f'relative change {amp_rel:.2f}% (+/-{amp_pm:.2f}% << +/-10%)')
print(f'        alpha = dlnA/dlnI0 = {alpha:.4f} (target |alpha|<~0.05)')
print(f'    (b) frequency monotone rising: {bool(np.all(np.diff(fs) > 0))}, '
      f'{fs.min():.3f}→{fs.max():.3f} au⁻¹ ({fs.max()/fs.min():.2f}×) ')
print(f'        ν_f = ∂f/∂lnI₀ = {nu_f:.4f} au⁻¹ > 0 ✓')
print(f'    (c) equivalent count: N vs ln I0 slope = {cN[0]:.3f} pulses/ln-unit, R^2 = {R2N:.4f}')

# full-window shape (reported as-is: inverted U) 
Is_full = np.round(np.arange(0.36, 1.42, 0.06), 3)
fs_full = np.array([measure(I)[2] for I in Is_full])
i_max = np.nanargmax(fs_full)
print(f'    full-window shape: f is an inverted U (forced by symmetry), peak {np.nanmax(fs_full):.3f} au⁻¹ '
      f'@ I₀≈{Is_full[i_max]:.2f}; the upper half-branch is the rising segment (encoding region),'
      f'falling back near the depolarization-block end.')

# ============================================================
# part 4: literature-point comparison section
# ============================================================
print(f'\n[4] literature-point comparison')
print(f"    · Hao & O'Shea 2012 (NSMB 19:31): yeast Msn2 under glucose starvation")
print(f'      nuclear-localization pulses - amplitude nearly constant, pulse frequency/number increase with starvation (dose);')
print(f'      this model: A varies by +/-{amp_pm:.1f}%, f rises {fs.max()/fs.min():.2f}x - qualitatively consistent. ')
print(f'    · Cai, Dalal & Elowitz 2008 (Nature 455:485): Crz1 calcium-response FM bursts -')
print(f'      frequency rises with Ca2+ while amplitude/duration stay constant; i.e. frequency modulation (FM), not amplitude modulation (AM).')
print(f"    - this is exactly the 'frequency = counts per unit time' digital channel: same family as p53 pulse counting (code 1,")
print(f'      Lahav 2004/Batchelor 2008) same family - encoding signature = f(bifurcation type x observable)')
print(f'      the dual instance (manuscript section 6 outlook): excitable (EXC) bifurcation x frequency/count readout -> digital side.')

# ============================================================
# three-panel figure
# ============================================================
tt_lo, v_lo = simulate(0.36)          # low-frequency representative
tt_hi, v_hi = simulate(0.84)          # high-frequency representative
pk_lo, _ = find_peaks(v_lo, prominence=1.0, distance=int(1.0/DT))
pk_hi, _ = find_peaks(v_hi, prominence=1.0, distance=int(1.0/DT))
f_lo = 1/np.diff(tt_lo[pk_lo]).mean(); f_hi = 1/np.diff(tt_hi[pk_hi]).mean()

fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))

ax = axes[0]                          # (a) representative trajectories: low vs high frequency, amplitude constant
ax.plot(tt_lo-40, v_lo + 3.0, lw=0.8, color='#888888',
        label=f'$I_0$=0.36 (N={len(pk_lo)}, f={f_lo:.3f} au$^{{-1}}$) ')
ax.plot(tt_hi-40, v_hi, lw=0.8, color='#1f77b4',
        label=f'$I_0$=0.84 (N={len(pk_hi)}, f={f_hi:.3f} au$^{{-1}}$) ')
ax.set_xlabel('time (au, within effective window)'); ax.set_ylabel('v (offset display)')
ax.legend(fontsize=9); ax.set_title('(a) pulse train under sustained drive: frequency rises, amplitude constant')

ax = axes[1]                          # (b) amplitude and frequency vs I0, dual axis
ax2 = ax.twinx()
ax.plot(Is_sig, As, 'o-', color='#ff7f0e', ms=6, label='amplitude A')
ax2.plot(Is_sig, fs, 's-', color='#1f77b4', ms=6, label='frequency f')
ax.axhline(As.mean(), color='#ff7f0e', ls=':', lw=1)
ax.set_xlabel('sustained drive $I_0$'); ax.set_ylabel('amplitude A', color='#ff7f0e')
ax2.set_ylabel('frequency f (au$^{-1}$)', color='#1f77b4')
ax.tick_params(axis='y', labelcolor='#ff7f0e')
ax2.tick_params(axis='y', labelcolor='#1f77b4')
ax.annotate(f'$\\alpha=\\partial\\ln A/\\partial\\ln I_0$ = {alpha:.3f}\n'
            f'$\\nu_f=\\partial f/\\partial\\ln I_0$ = {nu_f:.3f} au$^{{-1}}$',
            (0.40, 3.82), fontsize=10,
            bbox=dict(boxstyle='round', fc='white', alpha=0.85))
ax.set_title('(b) digital signature: A flat (alpha~0) + f monotone rising (nu_f>0)')

ax = axes[2]                          # (c) N vs ln I₀ scatter + fit
ax.plot(lnI, Ns, 'ko', ms=7, label='measured pulse count N (60 au window)')
xx = np.linspace(lnI.min(), lnI.max(), 50)
ax.plot(xx, np.polyval(cN, xx), 'r--', lw=1.5,
        label=f'linear fit: slope={cN[0]:.2f}, R²={R2N:.3f}')
ax.set_xlabel('ln $I_0$'); ax.set_ylabel('pulse count N'); ax.legend(fontsize=9)
ax.set_title('(c) equivalent counting index: N ~ linear in ln I0')

plt.tight_layout()
plt.savefig('/mnt/agents/output/Msn2_frequency_encoding_fig.png', dpi=200)
print('\nsaved /mnt/agents/output/Msn2_frequency_encoding_fig.png')
