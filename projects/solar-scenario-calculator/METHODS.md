# Methods and units

This calculator develops the solar-area and solar-energy functions in `UK Sustainability.R` into a self-contained scenario workflow. Its input is annual energy demand in kWh, independent of monetary environmental-cost measures.

Annual energy = active panel area × annual plane-of-array irradiation × conversion efficiency × performance factor.

Units: m² × kWh/(m² year) × dimensionless × dimensionless = kWh/year.

Required active panel area = annual demand / (annual irradiation × efficiency × performance factor).

Annual demand ratio = annual generated energy / annual demand. This ratio is deliberately uncapped: values above one indicate annual generation greater than annual demand. Annual balance is generated energy minus demand.

The performance factor is a single assumed multiplier for combined losses beyond conversion efficiency. Users must avoid counting the same loss twice. Active panel area excludes spacing and site-access allowances. Irradiation must represent energy incident on the panel plane over one year, not instantaneous irradiance in W/m².

The sensitivity grid holds area, irradiation and demand equal to the first scenario and crosses efficiencies 0.15, 0.18 and 0.21 with performance factors 0.75, 0.85 and 0.95. These are illustrative choices, not measured or recommended specifications.

This deterministic arithmetic model has no hourly generation, shading geometry, weather uncertainty, storage, tariff, degradation or financial component. It is suitable for exploring input relationships, not site-specific engineering design. It does not estimate self-consumption or reliability.

Tests cover a hand-calculated 81,000 kWh example, the inverse area relationship, linear area scaling, zero area, uncapped surplus, invalid inputs, the nine-case grid and duplicate names.
