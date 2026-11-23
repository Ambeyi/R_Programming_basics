# Methods

Each accepted row is one event, not a unique person, session, customer or purchase. Timestamps use month/day/year and 24-hour hour:minute. Timezone is unspecified; times are not converted. Invalid timestamps are excluded and counted. The stored Hour and Month columns, when present, are ignored in favour of the parsed Date.

Categories are trimmed and lowercased. Empty categories become `(missing)`; this bucket also includes a literal category with that name. Daily reports contain only dates with accepted events; absent dates are not interpreted as zero activity. Hourly reports contain all 24 hours, pooled across dates. Duplicate rows are counted as separate events. The script does not identify bots or infer conversions.

IP addresses, URLs, products and departments are not retained in outputs. Output categories come from the input and should be reviewed before publication for other datasets. Summary totals and each report's event counts reconcile to accepted rows. The historical reports describe the supplied snapshot; example data are fictional.
