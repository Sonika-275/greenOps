import math

#  Grid emission intensity (kg CO2 per kWh)
GRID_INTENSITY = {
    "India": 0.7,
    "USA": 0.4,
    "EU": 0.3
}

#Tree absorption per year (kg CO2)
CO2_PER_TREE_PER_YEAR = 21

# car emission factor (kg CO2 per km)
CAR_CO2_PER_KM = 0.12


def estimate_energy(total_operation_weight: float) -> float:
    """
    Estimate energy consumption in kWh based on operation weight.
    """
    energy_factor =  0.005  # Tunable
    return round(total_operation_weight * energy_factor, 3)


def estimate_co2(energy_kwh: float, region: str = "India") -> float:
    """
    Estimate CO2 emissions based on energy and region.
    """
    intensity = GRID_INTENSITY.get(region, 0.7)
    return round(energy_kwh * intensity, 3)


def annual_projection(co2_per_run: float, executions_per_day: int = 40000) -> dict:
    """
    Project annual carbon impact based on daily executions.
    """
    annual_co2 = co2_per_run * executions_per_day * 365
    annual_co2 = round(annual_co2, 2)

    trees_needed = round(annual_co2 / CO2_PER_TREE_PER_YEAR, 2)

    return {
        "executions_per_day": executions_per_day,
        "annual_co2_kg": annual_co2,
        "trees_needed_per_year": trees_needed
    }













# mathematical calculation for compare.py
def compare_optimization( 
    original_co2_per_run: float,   # orig_co2 from compare.py
    optimized_co2_per_run: float,  # opt_co2 from compare.py
    executions_per_day: int = 10000
) -> dict:
    """
    Compare before and after optimization impact.
    """
    original_annual = original_co2_per_run * executions_per_day * 365
    optimized_annual = optimized_co2_per_run * executions_per_day * 365

    savings = original_annual - optimized_annual
    
    return {
        "annual_co2_before_kg": round(original_annual, 2),
        "annual_co2_after_kg": round(optimized_annual, 2),
        "annual_co2_savings_kg": round(savings, 2),
        "trees_saved_per_year": round(savings / CO2_PER_TREE_PER_YEAR, 2)
    }