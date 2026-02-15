import ast
from engine.rules import get_rule



def analyze_code(code: str):
    issues = []
    total_operation_weight = 0

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {
            "issues": [{"message": "Invalid Python code", "line": None}],
            "total_operation_weight": 0
        }

    # Detect nested loops
    nested_loop_issues = detect_nested_loops(tree)
    issues.extend(nested_loop_issues)
     # Detect membership issues 
    membership_issues = detect_inefficient_membership(tree)
    issues.extend(membership_issues)


    # Sum weights
    for issue in issues:
        total_operation_weight += issue["weight"]

    return {
        "issues": issues,
        "total_operation_weight": total_operation_weight
    }


def detect_nested_loops(tree):
    issues = []
    rule = get_rule("R1")

    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            for child in ast.walk(node):
                if isinstance(child, ast.For):
                    if child != node:
                        issues.append({
                            "rule_id": "R1",
                            "message": rule["rule_name"],
                            "line": child.lineno,
                            "weight": rule["base_operation_weight"],
                            "severity": rule["severity"],
                            "suggestion": rule["suggestion"]
                        })
                        break
    return issues


def detect_inefficient_membership(tree):
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            for child in ast.walk(node):
                if isinstance(child, ast.Compare):
                    if isinstance(child.ops[0], ast.In):
                        rule = get_rule("R6")

                        issues.append({
                            "rule_id": "R6",
                            "message": rule["rule_name"],
                            "line": child.lineno,
                            "weight": rule["base_operation_weight"],
                            "severity": rule["severity"],
                            "suggestion": rule["suggestion"]
                        })

    return issues
