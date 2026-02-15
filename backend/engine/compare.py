# engine/compare.py
from engine.analyzer import analyze_code
from engine.carbon import estimate_energy, estimate_co2,compare_optimization
from engine.scoring import calculate_green_score
from engine.rules import get_rule

def analyze_comparison(original_code: str, optimized_code: str, region: str = "India") -> dict:
    """
    Analyze original and optimized code and return all metrics including comparison.
    """
    # -------- Original Code Analysis --------
    orig_result = analyze_code(original_code)
    orig_weight = orig_result["total_operation_weight"]
    orig_issues = orig_result.get("issues", [])

    orig_energy = estimate_energy(orig_weight)
    orig_co2 = estimate_co2(orig_energy, region)
    orig_score = calculate_green_score(orig_weight)
    orig_recommendations = list(
        set(
            get_rule(issue["rule_id"])["suggestion"]
            for issue in orig_issues
            if get_rule(issue["rule_id"]) is not None
        )
    )
  

    # -------- Optimized Code Analysis --------
    opt_result = analyze_code(optimized_code)
    opt_weight = opt_result["total_operation_weight"]
    opt_issues = opt_result.get("issues", [])

    opt_energy = estimate_energy(opt_weight)
    opt_co2 = estimate_co2(opt_energy, region)
    opt_score = calculate_green_score(opt_weight)

    opt_recommendations = list(
        set(
            get_rule(issue["rule_id"])["suggestion"]
            for issue in opt_issues
            if get_rule(issue["rule_id"]) is not None
        )
    )

    # -------- Impact metrics --------
    impact_projection = compare_optimization(orig_co2, opt_co2) # function from carbon.py
    
    # ---------------- COMPARISON ----------------
    co2_saved = orig_co2 - opt_co2

    if orig_co2 > 0:
        reduction_percent = round((co2_saved / orig_co2) * 100, 2)
    else:
        reduction_percent = 0.0

    # Impact message logic
    if reduction_percent >= 75:
        impact_message = "Massive carbon reduction achieved."
    elif reduction_percent >= 40:
        impact_message = "Significant carbon optimization achieved."
    elif reduction_percent > 0:
        impact_message = "Carbon footprint reduced."
    else:
        impact_message = "No structural carbon improvement detected."
        
    return {
        "original": {
            "green_score": orig_score,
            "co2_kg": orig_co2,
            "issues": orig_issues,
            "optimization_recommendations": orig_recommendations
        },
        "optimized": {
            "green_score": opt_score,
            "co2_kg": opt_co2,
            "issues": opt_issues,
            "optimization_recommendations": opt_recommendations
        },
        "comparison": {
            "co2_saved_kg": co2_saved,
            "reduction_percent": reduction_percent,
            "impact_message": impact_message,
            "annual_projection": impact_projection
        }
    }
