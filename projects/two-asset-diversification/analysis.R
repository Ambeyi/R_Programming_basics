# Base R counterpart of the reviewed two-asset exercise.
# Run from this project's directory: Rscript analysis.R
mu_a <- 0.12
mu_b <- 0.10
sd_a <- 0.30
sd_b <- 0.20
weights <- seq(0, 1, by = 0.1)
rows <- do.call(rbind, lapply(c(0.0417, 1), function(rho) {
  variance <- weights^2 * sd_a^2 + (1 - weights)^2 * sd_b^2 +
    2 * weights * (1 - weights) * rho * sd_a * sd_b
  data.frame(correlation = rho, weight_A = weights, weight_B = 1 - weights,
             expected_return = weights * mu_a + (1 - weights) * mu_b,
             standard_deviation = sqrt(variance))
}))
dir.create('results', showWarnings = FALSE)
write.csv(rows, 'results/portfolio_grid_R.csv', row.names = FALSE)
print(rows)
