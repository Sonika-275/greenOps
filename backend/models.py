from pydantic import BaseModel
from typing import Any,List,Dict,Optional

# Request model for sending a single code snippet
class CodeRequest(BaseModel):
    code: str

# Request model for comparing original and optimized code
class CompareRequest(BaseModel):
    original_code: str
    optimized_code: str

# Response model for analysis results
class AnalyzeResponse(BaseModel):
    green_score: int                # Carbon efficiency score
    co2_kg: float                   # Estimated CO2 in kg
    issues: Optional[List[Dict[str, Any]]] = []  # List of detected issues (optional, defaults to empty)