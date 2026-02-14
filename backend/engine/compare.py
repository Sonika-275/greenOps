# engine/compare.py
from engine.analyzer import analyze_code
from engine.carbon import estimate_energy, estimate_co2, compare_optimization, annual_projection

def analyze_comparison(original_code: str, optimized_code: str, region: str = "India") -> dict:
    """
    Analyze original and optimized code and return all metrics including comparison.
    """
    # -------- Original Code Analysis --------
    orig_result = analyze_code(original_code)
    orig_weight = orig_result["total_operation_weight"]
    orig_energy = estimate_energy(orig_weight)
    orig_co2 = estimate_co2(orig_energy, region)
    orig_projection = annual_projection(orig_co2)

    # -------- Optimized Code Analysis --------
    opt_result = analyze_code(optimized_code)
    opt_weight = opt_result["total_operation_weight"]
    opt_energy = estimate_energy(opt_weight)
    opt_co2 = estimate_co2(opt_energy, region)
    opt_projection = annual_projection(opt_co2)

    # -------- Comparison Metrics --------
    comparison = compare_optimization(orig_co2, opt_co2) # function from compare.py

    return {
        "original": {
            "weight": orig_weight,
            "energy_kwh": orig_energy,
            "co2_kg": orig_co2,
            "annual_projection": orig_projection,
            "issues": orig_result.get("issues", [])
        },
        "optimized": {
            "weight": opt_weight,
            "energy_kwh": opt_energy,
            "co2_kg": opt_co2,
            "annual_projection": opt_projection,
            "issues": opt_result.get("issues", [])
        },
        "comparison": comparison # output from compare_optimization
    }
