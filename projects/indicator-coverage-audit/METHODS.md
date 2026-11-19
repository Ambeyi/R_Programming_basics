# Methods and input schema

Input is a UTF-8 CSV with Country Code, Indicator Code, Year and Value columns. Other columns are ignored. Country and indicator keys must be nonblank; years must parse as integers from 1 to 9999; values must be finite numbers. Zero and negative values are accepted because indicator units differ.

Rows are rejected in order: missing key, invalid year, invalid value. Duplicate keys count all rows with valid country, indicator and year, even if a value is invalid. Duplicate values are not averaged: coverage counts a year once when at least one value is valid. Conflicting duplicates require separate review before value analysis.

Coverage is the number of distinct valid years divided by the inclusive span from first to last valid year. Internal gaps lie inside this span; no coverage requirement is inferred before or after it. A single observation has 100% internal coverage, which does not imply suitability for time-series modelling. Series with only invalid values have zero valid years and blank endpoints and coverage.

Annual counts represent series with a valid value in each year. No imputation, trend estimation or comparison of values across different units is performed. Results describe the supplied historical snapshot and do not establish current indicator availability.
