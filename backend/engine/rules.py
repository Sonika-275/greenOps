RULES = {
    "R1": {
        "rule_name": "Nested Loop Detected",
        "base_operation_weight": 40,
        "severity": "Very High",
        "suggestion": "Reduce nested iterations using hashmap, set lookup, or precomputed data structures to avoid quadratic complexity."
    },

    "R2": {
        "rule_name": "Inefficient Membership Check Inside Loop",
        "base_operation_weight": 20,
        "severity": "High",
        "suggestion": "Convert list to set for O(1) membership lookup when used repeatedly inside loops."
    },

    "R3": {
        "rule_name": "Constant Object Creation Inside Loop",
        "base_operation_weight": 15,
        "severity": "Medium",
        "suggestion": "Move constant list/dict/set creation outside the loop to prevent repeated memory allocation."
    }
}


def get_rule(rule_id: str):
    return RULES.get(rule_id)
