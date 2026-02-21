from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from models import AnalyzeResponse
from engine.analyzer import analyze_code
from engine.scoring import calculate_green_score
from engine.carbon import (estimate_energy,estimate_co2)
from engine.compare import analyze_comparison  
from engine.rules import get_rule



app = FastAPI()

#CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

 #---------------------------
# analyse endpoint
# ---------------------------
@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: CodeRequest):
    region = "India"

    # Run analyzer
    result = analyze_code(request.code)
    issues = result["issues"]
    total_weight = result["total_operation_weight"]

    # Scoring
    green_score = calculate_green_score(total_weight) 

    # Carbon Estimation 
    energy = estimate_energy(total_weight)
    co2 = estimate_co2(energy, region=region)
 
    return {
        "green_score": green_score,         # from scoring.py
        "estimated_co2_kg":  co2,           # from carbon.py
        "issues": issues,                   # from analyzer.py + suggestion from rules.py
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