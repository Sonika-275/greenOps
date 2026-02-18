export interface Issue {
  rule_id: string;
  message: string;
  line: number;
  weight: number;
  severity: string;
}

export interface CodeAnalysisResult {
  green_score: number;
  co2_kg: number;
  issues:Issue[];
  optimization_recommendations: string[];
}

export interface ComparisonResponse {
  original: CodeAnalysisResult;
  optimized: CodeAnalysisResult;
  comparison: {
    co2_saved_kg: number;
    reduction_percent: number;
    impact_message: string;
    annual_projection: {
        annual_co2_before_kg: number;
        annual_co2_after_kg: number;
        annual_co2_savings_kg: number;
        trees_saved_per_year: number;
    };
  };
}
