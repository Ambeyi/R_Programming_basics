# Statistical methods

This workflow compares two independent numeric samples, labelled A and B. It develops the two-sample comparison theme in `STAT 5601.R` from the Posit project. The included CSV is an invented teaching example with arbitrary units, not measured participant data.

Welch's test evaluates equal population means without assuming equal variances. Standard error is sqrt(s_A²/n_A + s_B²/n_B), with sample variances using n−1 denominators. Degrees of freedom use the Welch–Satterthwaite formula. A two-sided 95% t interval describes mean(A) minus mean(B). Small-sample inference relies on approximately normal distributions; independence is required.

Mann–Whitney U uses a two-sided normal approximation with tie correction and continuity correction. It tests equal distributions under its null; a pure location interpretation needs additional distribution-shape assumptions. U/(n_A n_B) estimates P(A>B) + 0.5 P(A=B). It is an effect size, not the probability that a hypothesis is true.

The two-sided Kolmogorov–Smirnov test compares empirical distribution functions. Its exact p-value calculation assumes independent samples from continuous distributions. For rounded or tied data, including the bundled integer example, that calibration is not exact; treat its p-value as illustrative. The KS statistic remains a descriptive measure of distribution separation.

The three p-values are unadjusted and answer different questions. They are not three independent confirmations of the same claim. The tool does not establish causation, practical importance or equivalence. Choose a primary analysis before interpreting results.

Input validation rejects nonfinite values, samples smaller than two, multidimensional samples and zero variance within either group. Unequal sample sizes are supported. CSV input has precisely two columns, `group,value`, with group labels A or B. The tool does not silently remove missing values.

Tests verify a hand-calculated Welch statistic and degrees of freedom, effect size by direct pairwise enumeration with ties, invariance under group swapping, identical samples and invalid inputs.
