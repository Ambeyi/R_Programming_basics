# CSV schemas

Mappings: `current` is the canonical target; `former` is the exact alias; `start_date` and `end_date` define an inclusive validity interval.

Events: `name` is the observed alias; `date` is the event date.

Resolved output: `name`, `date`, `status`, `canonical`, `candidate_count`. Status is matched, ambiguous or unmatched. Summary JSON records mapping-row count, event count and status totals. Extra input fields are ignored.
