import ast
from engine.rules import get_rule

# ==========================================================
# MASTER ANALYZER
# ==========================================================

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
    
    # checking for issues
    detectors = [
        detect_nested_loops,
        detect_inefficient_membership,
        detect_object_creation_in_loop
    ]

    for detector in detectors:
        detected = detector(tree)
        issues.extend(detected)

    # ---- Remove duplicate issues ----
    unique_issues = []
    seen = set()

    for issue in issues:
        key = (issue["rule_id"], issue["line"])
        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)

    issues = unique_issues

    # Sum weights
    for issue in issues:
        total_operation_weight = sum(
    issue["weight"] for issue in issues
    )

    return {
        "issues": issues,
        "total_operation_weight": total_operation_weight
    }

# ==========================================================
# R1 – Nested Loop Detection
# ==========================================================

def detect_nested_loops(tree):
    issues = []
    SMALL_RANGE_THRESHOLD = 5

    for node in ast.walk(tree):
        if isinstance(node, ast.For):

            for child in node.body:
                if isinstance(child, ast.For):

                    # Check if inner loop is small constant range
                    if isinstance(child.iter, ast.Call):
                        if isinstance(child.iter.func, ast.Name) and child.iter.func.id == "range":
                            args = child.iter.args
                            if len(args) == 1 and isinstance(args[0], ast.Constant):
                                if args[0].value <= SMALL_RANGE_THRESHOLD:
                                    continue  # Ignore small constant loop

                    # Otherwise flag as nested loop
                    rule = get_rule("R1")
                    issues.append({
                        "rule_id": "R1",
                        "title": rule["rule_name"],
                        "suggestion": rule["suggestion"],
                        "line": child.lineno,
                        "weight": rule["base_operation_weight"],
                        "severity": rule["severity"]
                    })

    return issues

# ==========================================================
# R2 – Inefficient Membership Inside Loop
# Only flag if container is NOT a set
# ==========================================================

def detect_inefficient_membership(tree):
    issues = []
    variable_types = {}

    # Step 1: Track variable assignments
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.List):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variable_types[target.id] = "list"

            elif isinstance(node.value, ast.Set):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variable_types[target.id] = "set"

    # Step 2: Detect inefficient membership inside loops
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            for child in ast.walk(node):
                if isinstance(child, ast.Compare):
                    if isinstance(child.ops[0], ast.In):

                        # Check container type
                        if isinstance(child.comparators[0], ast.Name):
                            container_name = child.comparators[0].id
                            container_type = variable_types.get(container_name)

                            if container_type == "list":  # Only penalize lists
                                rule = get_rule("R2")

                                issues.append({
                                    "rule_id": "R2",
                                    "title": rule["rule_name"],
                                    "suggestion": rule["suggestion"],
                                    "line": child.lineno,
                                    "weight": rule["base_operation_weight"],
                                    "severity": rule["severity"]
                                })

    return issues


# ==========================================================
# R3 – Constant Object Creation Inside Loop
# Only detect constant literals recreated repeatedly
# ==========================================================

def detect_object_creation_in_loop(tree):
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            for child in ast.walk(node):

                if isinstance(child, (ast.List, ast.Set)):
                    if all(isinstance(elt, ast.Constant) for elt in child.elts):
                        rule = get_rule("R3")
                        issues.append({
                            "rule_id": "R3",
                            "title": rule["rule_name"],
                            "suggestion": rule["suggestion"],
                            "line": child.lineno,
                            "weight": rule["base_operation_weight"],
                            "severity": rule["severity"]
                        })

                if isinstance(child, ast.Dict):
                    if all(isinstance(k, ast.Constant) and isinstance(v, ast.Constant)
                           for k, v in zip(child.keys, child.values)):
                        rule = get_rule("R3")
                        issues.append({
                            "rule_id": "R3",
                            "message": rule["rule_name"],
                            "line": child.lineno,
                            "weight": rule["base_operation_weight"],
                            "severity": rule["severity"]
                        })

    return issues
