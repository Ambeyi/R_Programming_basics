# Methods

The workflow develops the partitioning theme in `data_prep.R` using the supplied `mailing.csv`. The source records are not bundled; the included forty-row example is synthetic.

For each class, a seeded NumPy generator permutes row positions. Training takes floor(0.70 × class count), validation takes floor(0.15 × class count), and testing takes all remaining positions. No replacement or oversampling occurs. Consequently, small classes may deviate visibly from nominal proportions. At least ten rows per class are required. The original source order is restored within each partition, and reproducibility assumes the same input row order and software behavior.

Row-position overlap checks whether the same source row was assigned more than once. Feature-pattern overlap hashes all columns except class using pandas, without the row index, and counts distinct hashes shared by each pair of partitions. Hash collisions are theoretically possible; this is an audit signal rather than proof that records refer to the same entity. Conversely, different feature patterns can still belong to the same entity. The source schema does not provide an established unique person identifier.

Duplicate feature rows are counted beyond first occurrences across the full dataset. Duplicates remain present and can cross partitions. For entity-level evaluation, use a verified grouping key and a group-aware split. For temporal evaluation, use suitable timestamps and a chronological design. This tool implements neither policy automatically.

Class labels must be complete 0/1 values. Feature missingness is reported but not filled; downstream preprocessing must be fitted on training data only. No feature encoder, balancing step or prediction model is fitted. The class label retains its numeric meaning because its substantive definition is not established here.

Seven tests cover hand-calculated class allocation, complete disjoint row assignment, reproducibility, invalid labels, feature duplicates, missing-feature retention and rounding remainders. The reports describe a reproducible preparation audit, not a validated predictive model or a leakage-free evaluation guarantee.
