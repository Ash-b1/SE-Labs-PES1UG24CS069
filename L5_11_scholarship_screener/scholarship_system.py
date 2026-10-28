"""Scholarship screening system: scores applicants and shortlists them."""

import json
import ast
import operator

# Global state
results = {}
MERIT_CONFIG = {"formula": "gpa * 10 + credits * 2"}
INCOME_LIMIT = 800000
CUTOFF = 85

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv}


def _safe_eval(node, names):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body, names)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id in names:
        return names[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.left, names),
                                   _safe_eval(node.right, names))
    raise ValueError("Unsupported expression")


def calculate_merit_score(gpa, credits_points):
    """Return the merit score for the given GPA and credits."""
    tree = ast.parse(MERIT_CONFIG["formula"], mode="eval")
    return _safe_eval(tree, {"gpa": gpa, "credits": credits_points})


def evaluate_applicant(student_id, test_scores, logs=None):
    """Score an applicant, record the result, and return eligibility."""
    gpa = test_scores["gpa"]
    credits_points = test_scores.get("credits", 0)
    income = test_scores.get("income", 0)
    score = calculate_merit_score(gpa, credits_points)
    eligible = score >= CUTOFF and income < INCOME_LIMIT
    results[student_id] = {"score": score, "eligible": eligible}
    if logs is not None:
        logs.append(f"{student_id} scored {score}")
    return eligible


def change_formula(new_formula):
    """Replace the merit formula used for scoring."""
    MERIT_CONFIG["formula"] = new_formula


def persist_results(file="scholarships.json"):
    """Save all results to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(results, f)


def load_results(file="scholarships.json"):
    """Load results from a JSON file."""
    try:
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
        results.clear()
        results.update(data)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Could not load {file}, keeping current results")


def print_shortlist():
    """Print every applicant who is eligible."""
    print("Shortlisted applicants:")
    for student_id, info in results.items():
        if info["eligible"]:
            print(" ", student_id, "score =", info["score"])


def main():
    """Run the sample applicants and print the shortlist."""
    evaluate_applicant("U001", {"gpa": 9.1, "credits": 4, "income": 450000})
    evaluate_applicant("U002", {"gpa": 7.2, "credits": 1, "income": 300000})
    evaluate_applicant("U003", {"gpa": 12.5, "credits": -3, "income": -1})
    evaluate_applicant("U004", {"gpa": 6.5})
    formula = input("Merit formula (Enter to keep default): ")
    if formula:
        change_formula(formula)
    evaluate_applicant("U005", {"gpa": 8.4, "credits": 3, "income": 600000})
    persist_results()
    load_results()
    print_shortlist()


main()
