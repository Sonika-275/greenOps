import axios from "axios";
import type { ComparisonResponse } from "../types/comparison";

const API_BASE = "http://127.0.0.1:8000";

export const compareCode = async (
  originalCode: string,
  optimizedCode: string
): Promise<ComparisonResponse> => {

  const response = await axios.post(`${API_BASE}/compare`, {
    original_code: originalCode,
    optimized_code: optimizedCode
  });

  return response.data;
};
