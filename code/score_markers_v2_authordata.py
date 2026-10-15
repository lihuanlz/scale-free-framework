"""Score markers v2: author's own supplementary numerical data (mmc2.xls), same frozen lines.
Only Fig5C/5E glycerol arms remain digitized (not present in mmc2)."""
import numpy as np
import pandas as pd
from pathlib import Path

XLS = Path(r"D:\Kimi_Agent_细胞仿真工具包扩展以及具身智能20260911\05_主线纲领与设计\渗透压线\data\muzzey2009\mmc2.xls")


def sheet(name, tcol=0):
    df = pd.read_excel(XLS, sheet_name=name, header=0)
    return df


def sustained(x, y, cond, hold=8.0):
    idx = np.where(cond(y))[0]
    for i in idx:
        j = np.where((x >= x[i]) & (x <= x[i] + hold))[0]
        if len(j) and cond(y[j]).all():
            return x[i]
    return None


print("=" * 72)
print("M1  (author data, Figure2A + Figure2B, 0.4 M NaCl step)")
print("=" * 72)
a = sheet("Figure2A"); b = sheet("Figure2B")
ta = a["Time (minutes)"].to_numpy(float); ha = a["Mean Hog1"].to_numpy(float)
tb = b["Time (minutes)"].to_numpy(float); vb = b["Mean Volume"].to_numpy(float)
base = np.median(ha[ta < 0]); peak = ha.max(); tpk = ta[np.argmax(ha)]
thr = base + 0.10 * (peak - base)
t_off = sustained(ta, ha, lambda v: v <= thr)
late = ha[ta > 45].mean()
vbase = np.median(vb[tb < 0]); vmin = vb.min()
rec = vbase + 0.10 * (vmin - vbase)
t_rec = sustained(tb, vb, lambda v: v >= rec)
print(f"Hog1: baseline={base:.4f} peak={peak:.4f}@{tpk:.2f}min  thr10%={thr:.4f}")
print(f"      t_off={t_off:.2f} min   late(>45min)={late:.4f} ({abs(late-base)/peak*100:.2f}% of peak)")
print(f"Vol : baseline={vbase:.4f} min={vmin:.4f}  90%band={rec:.4f}")
print(f"      t_rec90={t_rec:.2f} min")
print(f"      |t_off - t_rec| = {abs(t_off-t_rec):.2f} min   (line <5)  -> {'PASS' if abs(t_off-t_rec)<5 else 'FAIL'}")
print(f"      Hog1 adaptation (<10% of peak late) -> {'PASS' if abs(late-base)<0.10*(peak-base) else 'FAIL'}")

print()
print("Dose generality (Figure3A/3B, author data):")
fa = sheet("FIgure3A"); fb = sheet("Figure3B")
t3a = fa["Time (minutes)"].to_numpy(float)
t3b = fb["Time (minutes)"].to_numpy(float)
for dose, col in [("0.2M", "0.2M"), ("0.4M", "0.4M"), ("0.6M", "0.6M")]:
    h = fa[f"{col}, Mean Hog1"].to_numpy(float)
    v = fb[f"{col}, Mean Volume"].to_numpy(float)
    pk = h.max(); lt = h[t3a > 50].mean()
    mn = v.min(); band = 0.10 * mn
    tr = sustained(t3b, v, lambda x: x >= band)
    fin = v[t3b > 55].mean()
    print(f"  {dose}: Hog1 peak={pk:.3f} late50-60={lt:.4f} adapted={'Y' if lt < 0.1*pk else 'N'} | "
          f"vol min={mn:.3f} t_rec90={f'{tr:.2f}' if tr is not None else '>60'} final55-60={fin:.4f}")
h0 = fa["0M, Mean Hog1"].to_numpy(float)
print(f"  0M control Hog1: min={h0.min():.4f} max={h0.max():.4f} (flat)")

print()
print("=" * 72)
print("P-1 registration (Figure5B author data, 0.4 M, hog1-as +/- PP1)")
print("=" * 72)
f5b = sheet("Figure5B")
t5 = f5b["Time (minutes)"].to_numpy(float)
for arm, col in [("-PP1", "0.4M, Volume, -PP1"), ("+PP1", "0.4M, Volume, +PP1")]:
    v = f5b[col].to_numpy(float)
    dip = np.median(v[(t5 >= 5) & (t5 <= 12)])
    latev = np.median(v[t5 > 30])
    frac = (latev - dip) / (0 - dip)
    print(f"  {arm}: dip(5-12min)={dip:.4f} late(>30min)={latev:.4f} recovery_fraction={frac:.3f}")
print("  frozen reading: -PP1 frac>0.5 recovers, +PP1 frac<0.5 fails -> P-1 verdict above")

print()
print("=" * 72)
print("M2 headline (0.4 M, the moderate shock)")
print("=" * 72)
print(f"  Fig2B author data: t_rec90={t_rec:.2f} min  (line <=30) -> {'PASS' if t_rec<=30 else 'CHECK'}")
v4 = fb["0.4M, Mean Volume"].to_numpy(float)
m4 = v4.min(); b4 = 0.10 * m4
tr4 = sustained(t3b, v4, lambda x: x >= b4)
print(f"  Fig3B author data 0.4M: t_rec90={tr4:.2f} min -> {'PASS' if tr4 and tr4<=30 else 'CHECK'}")

print()
print("=" * 72)
print("EXPLORATORY (post-hoc, labelled): alternative coincidence operationalisations")
print("=" * 72)
# (i) 50% crossing times
t50_off = sustained(ta, ha, lambda v: v <= base + 0.5 * (peak - base), hold=4.0)
t50_rec = sustained(tb, vb, lambda v: v >= vbase + 0.5 * (vmin - vbase), hold=4.0)
print(f"  t50(Hog1 decline)={t50_off:.2f}  t50(volume recovery)={t50_rec:.2f}  |dt|={abs(t50_off-t50_rec):.2f} min")
# (ii) paper's own definition: turgor recovered when volume-growth slope matches unstressed slope
post = tb >= 28
sl_late = np.polyfit(tb[tb > 35], vb[tb > 35], 1)[0]
sl_pre = np.polyfit(tb[tb < 0], vb[tb < 0], 1)[0]
print(f"  volume slope pre-shock={sl_pre:.5f}/min, post-35min={sl_late:.5f}/min")
# (iii) correlation of decline/recovery phases (5-30 min)
w = (ta >= 4) & (ta <= 30)
hv = ha[w]
w2 = (tb >= 4) & (tb <= 30)
vv = vb[w2]
n = min(len(hv), len(vv))
cc = np.corrcoef(hv[:n], vv[:n])[0, 1]
print(f"  corr(Hog1, volume) over 4-30min window: r={cc:.3f} (strong anticorrelation expected)")
