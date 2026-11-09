"""Annual solar energy bookkeeping with explicit physical units."""
import math

def calculate(area_m2, irradiation_kwh_m2_year, efficiency, performance_factor, demand_kwh_year):
    values=(area_m2,irradiation_kwh_m2_year,efficiency,performance_factor,demand_kwh_year)
    if any(isinstance(x,bool) or not isinstance(x,(float,int)) or not math.isfinite(x) for x in values):
        raise ValueError('Inputs must be finite numbers')
    if area_m2<0 or irradiation_kwh_m2_year<=0 or demand_kwh_year<=0:
        raise ValueError('Area must be nonnegative; irradiation and demand must be positive')
    if not 0<efficiency<=1 or not 0<performance_factor<=1:
        raise ValueError('Efficiency and performance factor must lie in (0,1]')
    yield_per_m2=irradiation_kwh_m2_year*efficiency*performance_factor
    energy=area_m2*yield_per_m2
    return dict(annual_energy_kwh=energy,required_area_m2=demand_kwh_year/yield_per_m2,
                annual_demand_ratio=energy/demand_kwh_year,
                annual_balance_kwh=energy-demand_kwh_year,
                annual_yield_kwh_m2=yield_per_m2)
