RULES = {
    "R1": {
        "rule_name": "Nested Loop Detected",
        "base_operation_weight": 40,
        "severity": "Very High",
        "suggestion": "Reduce nested iterations using hashmap or precomputed lookup."
    },
    "R6": {
         "rule_name": "Inefficient Membership Check",
         "base_operation_weight": 20,
         "severity": "Medium",
         "suggestion": "Convert list to set for O(1) membership lookup when used repeatedly."
}

}


def get_rule(rule_id: str):
    return RULES.get(rule_id)
