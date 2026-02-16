from pydantic import BaseModel
from typing import List

# Request model for sending a single code snippet
class CodeRequest(BaseModel):
    code: str

# Request model for comparing original and optimized code
class CompareRequest(BaseModel):
    original_code: str
    optimized_code: str

# Response model for analysis results
class Issue(BaseModel):
    rule_id: str
    message: str
    line: int
    weight: int
    severity: str

class AnalyzeResponse(BaseModel):
    green_score: float
    estimated_co2_kg: float
    issues: List[Issue]
    optimization_recommendations: List[str]