from fastapi import FastAPI
from pydantic import BaseModel
from engine.analyzer import analyze_code
from engine.scoring import calculate_green_score
from engine.carbon import (estimate_energy,estimate_co2,annual_projection,carbon_recommendation)
from engine.compare import analyze_comparison  



app = FastAPI()

# ---------------------------
# Request Models
# ---------------------------
class CodeRequest(BaseModel):
    code: str

class CompareRequest(BaseModel):
    original_code: str
    optimized_code: str

# ---------------------------
# Root Endpoint
# ---------------------------
@app.get("/")
def read_root():
    return {"message": "GreenOps Backend Running"}


# ---------------------------
# Health Endpoint
# ---------------------------
@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.post("/analyze")
def analyze(request: CodeRequest):
    region = "India"

    result = analyze_code(request.code)
    green_score = calculate_green_score(result["total_operation_weight"]) 
    energy = estimate_energy(result["total_operation_weight"])
    co2 = estimate_co2(energy, region=region)
    projection = annual_projection(co2)
    recommendation = carbon_recommendation(region)

    return {
        "green_score": green_score, # from scoring.py
        "total_operation_weight": result["total_operation_weight"], # from analyzer.py
        "estimated_energy_kwh": energy,     # from carbon.py
        "estimated_co2_kg":  co2,           # from carbon.py
        "annual_projection": projection,    # from carbon.py
        "carbon_recommendation": recommendation,  # from carbon.py
        "issues": result["issues"] # from analyzer.py
    }


# ---------------------------
# Compare Original vs Optimized Code
# ---------------------------
@app.post("/compare")
def compare_codes(request: CompareRequest):
    region = "India"
    comparison_result = analyze_comparison(
        original_code=request.original_code,
        optimized_code=request.optimized_code,
        region=region
    )
    
    return comparison_result