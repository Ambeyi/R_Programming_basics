# Resolution rules

Mapping intervals include both start and end dates. Names are trimmed but remain case-sensitive: no fuzzy matching, case folding or punctuation substitution occurs. An event matches only a former-name field, not a canonical-name field.

A unique canonical candidate produces `matched`. Multiple distinct candidates produce `ambiguous` with a blank canonical field. No candidates produce `unmatched`; the original name remains available for review. Duplicate mapping rows for the same canonical target do not create ambiguity. Overlaps are evaluated at the event date, not automatically rejected.

Dates must be valid ISO YYYY-MM-DD strings. Blank names, reversed intervals and missing required fields raise errors. Mappings can be empty. This is a deterministic lookup utility, not a historical verification service. All bundled mappings, events and results are synthetic.
