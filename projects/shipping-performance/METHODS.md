# Definitions and interpretation

An order is identified by `Order Id`. Repeated lines must agree on shipping mode, actual days and scheduled days. Conflicting orders cause an error rather than silently selecting a line.

Delay equals actual days minus scheduled days. Over-schedule means delay greater than zero; this metric is computed directly and is not the dataset's separate delivery-risk flag. It does not establish carrier responsibility or distinguish cancelled orders.

Each mode's rate divides its over-schedule orders by all orders in that mode. Negative delay means earlier than schedule. Missing required values are rejected. Numeric durations must be between zero and 3,650 days, a broad input-validation limit rather than a service standard.

Comparisons are descriptive. Shipping modes have different promised durations and customer/order mixes. The analysis does not estimate causal effects or forecast delivery times. No customer identifiers are included in aggregate outputs.
