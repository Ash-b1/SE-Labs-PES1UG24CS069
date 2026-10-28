**Known Issue Table: scholarship_system.py**

**Name: Annanya Sharma**

**SRN: PES1UG24CS069**



| **Issue** | **Type** | **Severity** | **Tool (ID)** | **Line(s)** | **Description** | **Fix Approach** |
| --- | --- | --- | --- | --- | --- | --- |
| **Use of eval() on user input** | Security vulnerability | **High** | Bandit B307 (CWE-78) | 11,12 | The merit formula typed in through input() is passed to eval(), so a user could run arbitrary Python code. Bandit rates it Medium, but here the input is user-controlled. | Replace eval() with ast.parse() plus a small whitelist evaluator (_safe_eval) that only allows numbers, gpa, credits and + - * /. ast.literal_eval cannot evaluate expressions. |
| **Mutable default argument** | Bug | **Medium** | Pylint W0102 | 14 | logs=[] is created once and shared across all calls, so log entries leak between calls. | Change default to None and append only when logs is not None. |
| **Bare except with pass** | Error handling | **Medium** | Bandit B110 (CWE-703) | 37,38 | A bare except: pass catches every exception and hides failures, so a missing or corrupt file goes unnoticed. | Catch only (FileNotFoundError, json.JSONDecodeError) and print a message instead of passing silently. |
| **File not closed safely** | Resource leak | **Medium** | Pylint R1732 | 29, 36 | Files are opened without a with block. If write() fails, close() is skipped, and open(file).read() is never closed explicitly. | Use with open(...) as f together with json.dump / json.load. |
| **Redefining built-in 'credits'** | Bug risk (shadowing) | **Low** | Pylint W0622 | 11, 16 | The parameter and variable named credits shadow a Python built-in. | Rename the Python variable to credit_points; keep the string "credits" used in the formula and input data. |
| **open() without encoding** | Portability | **Low** | Pylint W1514 | 29, 36 | The platform default encoding is used, so behaviour can differ between Windows and Linux. | Pass encoding="utf-8" to open(). |
| **Use of global statement** | Design | **Low** | Pylint W0603 | 25, 34 | Functions reassign module-level state with global, which makes the code harder to test and reason about. | Mutate the state instead: MERIT_CONFIG dict for the formula, results.clear() and results.update() for results. |
| **Comparison to True** | Style | **Low** | flake8 E712 | 43 | == True is redundant for a boolean value. | Use if info["eligible"]: directly. |
| **Unused imports** | Code quality | **Low** | flake8 F401 | 2,3 | math and sys are imported but never used. | Remove both import lines. |
| **Old-style % string formatting** | Style | **Low** | Pylint C0209 | 21 | % formatting used where an f-string is clearer. | Use f"{student_id} scored {score}". |
| **Function name not snake_case** | Naming | **Low** | Pylint C0103 | 40 | printShortlist does not follow PEP 8 naming. | Rename to print_shortlist in the definition and in the call inside main(). |
| **Missing docstrings** | Documentation | **Low** | Pylint C0114, C0116 | 1, 11, 14, 24, 28, 33, 40, 46 | The module and all functions have no docstrings. | Add a module docstring and a one-line docstring to each function. |
| **Missing blank lines** | Style | **Low** | flake8 E302, E305 | 11, 14, 24, 28, 33, 40, 46, 59 | PEP 8 expects two blank lines before top-level functions and after the last function. | Add the extra blank line at each location. |

