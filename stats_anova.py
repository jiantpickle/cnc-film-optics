import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

from cnc_common import features, iter_samples, load_sample

rows = []
for ph, dry, rep, num in iter_samples():
    t600, t300 = features(*load_sample(num))
    rows.append({"sample": num, "pH": ph, "drying": dry, "T600": t600, "T300": t300})
df = pd.DataFrame(rows)
print(f"Films analyzed: {len(df)}\n")
print("Mean and SD by pH (all films):")
print(df.groupby("pH")[["T600", "T300"]].agg(["mean", "std", "count"]).round(2), "\n")

main = df[df["pH"] != 2.5]
print("Mean and SD by drying level (pH 4.5-8.5):")
print(main.groupby("drying")[["T600", "T300"]].agg(["mean", "std", "count"]).round(2), "\n")

for y in ["T600", "T300"]:
    model = smf.ols(f"{y} ~ C(pH, Sum) * C(drying, Sum)", data=main).fit()
    print(f"=== {y}: two-way ANOVA (Type III) ===")
    print(sm.stats.anova_lm(model, typ=3)[["df", "F", "PR(>F)"]].round(4))
    groups = [main.loc[main["pH"] == p, y].values for p in (4.5, 6.5, 8.5)]
    print("Levene p = %.3f" % stats.levene(*groups).pvalue)
    tk = stats.tukey_hsd(*groups)
    labels = ("4.5", "6.5", "8.5")
    for i in range(3):
        for j in range(i + 1, 3):
            diff = groups[i].mean() - groups[j].mean()
            print(f"  Tukey pH {labels[i]} vs {labels[j]}: diff {diff:+.2f}, p = {tk.pvalue[i, j]:.4f}")
    print()
