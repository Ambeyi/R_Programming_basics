# Methods

The analysis uses the supplied `fish.csv` from the Posit project. Each row is a site and each species column is a binary observation. Location identifies rows and is excluded from the species matrix. The example CSV is synthetic and produces different results.

For species A and B, Jaccard distance is 1 − shared sites / union sites. Joint absences are excluded from the union. Distance zero means identical nonempty observed site sets; distance one means no shared sites when the union is nonempty. Two entirely absent species have an undefined distance, recorded with status both_absent. One absent and one present species have distance one.

Matrix multiplication calculates shared-site counts. Each unordered species pair is counted once, excluding self-pairs. A species' disjoint_partners count includes partners with no shared sites and a nonempty union. The sum of these partner counts is twice the disjoint-pair count.

Species prevalence is observed sites divided by all sites. Site richness is the number of species observed at that site. The richness distribution retains empty sites when present. No missing observations are interpreted as absence; missing or nonbinary values are rejected.

The exported closest-pair table contains up to 20 pairs sorted by distance, then species names for deterministic tie handling. Full pair calculations are available from the analyze function. This exploratory ranking is not a significance test. Rare species, sampling effort and imperfect detection can affect overlap. Absence of observed co-occurrence is not evidence of biological exclusion.

Tests verify a hand-calculated distance, set-based pair calculations, conservation of incidence totals, identical species, empty-species behavior, invalid inputs and row-order invariance. The actual-data reconciliation independently computes every pair using Python sets and checks the disjoint total.
