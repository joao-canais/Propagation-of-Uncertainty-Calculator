"""Module with utility functions for the app logistics and mathematical computations."""

from sympy.parsing.sympy_parser import parse_expr, standard_transformations, convert_xor
from decimal import Decimal

import streamlit as st
import sympy as sp
import json
import re


def spaces(number_of_spaces):
    """Returns a specified number of empty lines in the Streamlit app for spacing purposes."""
    
    for number_of_spaces in range(number_of_spaces):
        st.write(" ")
    

def add_var():
    """Adds a new variable to the session state, ensuring no duplicates and filling in missing variable names."""
    
    if st.session_state.num_vars < 10:  # maximum of 10 variables
        next_index = st.session_state.num_vars + 1
        missing_variables = get_undefined_variable_names(
            st.session_state.get("equation", "")
        )
        current_names = {
            st.session_state.get(f"var{i + 1}_name", "").strip()
            for i in range(st.session_state.num_vars)
        }
        next_name = next(
            (name for name in missing_variables if name not in current_names),
            "",
        )

        st.session_state.num_vars = next_index
        st.session_state[f"var{next_index}_name"] = next_name


def remove_var():
    """Removes a variable from the session state, ensuring at least one variable remains."""
    
    if st.session_state.num_vars > 1:
        st.session_state.num_vars -= 1


def get_clean_equation(equation):
    """Cleans the equation string and validates syntax"""
    
    # Clean the equation where it might be in the form of "R = expression"
    if "=" in equation:
        equation = equation.split("=", 1)[1].strip()
    if not equation:
        raise ValueError("Equation cannot be empty after `=`.")

    # Normalizes the equation by replacing certain characters and symbols
    equation = equation.replace("–", "-").replace("—", "-")
    equation = equation.replace("×", "*").replace("÷", "/") 
    equation = equation.replace(",", ".")
    
    # Removes empty spaces
    equation = equation.replace(" ", "")
    
    # Replaces the reserved Python name only when it is a complete variable name.
    equation = re.sub(r"\blambda\b", "lambda_", equation)

    # Empty parentheses: '()'
    if "()" in equation:
        raise ValueError("Contains empty parentheses `()`.")

    # Mismatched parentheses: (x + y ou x + y))
    if equation.count("(") != equation.count(")"):
        raise ValueError("Mismatched parentheses (check opening and closing brackets).")

    # Consecutive invalid operators (ex: 'x++y', 'x*/y', 'x^^y')
    # Allows '**', but blocks '++', '///', '*+', etc.
    if re.search(r"(\+\+|\-\-|\/\/|\/\*|\*\/|\^{2,}|\+{2,}|\-{2,})", equation):
        raise ValueError("Contains consecutive invalid operators.")

    # Operator at the beginning or end (ex: '/x*y' ou 'x+y*')
    # Allows '+' or '-' in the beginning but blocks '*', '/', '^'
    if equation[0] in "*/^":
        raise ValueError(f"Cannot start with operator `{equation[0]}`.")
    if equation[-1] in "+-*/^":
        raise ValueError(f"Cannot end with operator `{equation[-1]}`.")

    # Adjacent operators to parentheses (ex: '(+)', '(*x)', '(x*)')
    if re.search(r"\([\*\/\^]", equation):
        raise ValueError("Parentheses cannot immediately start with `*`, `/` or `^`.")
    if re.search(r"[\+\-\*\/\^]\)", equation):
        raise ValueError("Parentheses cannot end with an operator.")

    # Avoids invalid characters (only allows letters, numbers, and valid operators)
    invalid_chars = set(re.findall(r"[^\w\+\-\*\/\^\(\)\.]", equation))
    if invalid_chars:
        chars_str = ", ".join(f"{c}" for c in invalid_chars)
        raise ValueError(f"Contains invalid character(s): `{chars_str}`")

    return equation


def get_undefined_variable_names(equation):
    """Returns a sorted list of variable names in the equation that are not yet defined in the session state."""
    
    defined_names = {
        st.session_state.get(f"var{i + 1}_name", "").strip()
        for i in range(st.session_state.num_vars)
    }
    defined_names.discard("")

    try:
        transformations = standard_transformations + (convert_xor,)
        parsed_equation = parse_expr(
            equation,
            transformations=transformations,
            local_dict={
                "e": sp.E,
                "lambda_": sp.Symbol("lambda"),
            },
        )
    except Exception:
        return []

    return sorted(
        symbol.name
        for symbol in parsed_equation.free_symbols
        if symbol.name not in defined_names
    )


def get_dynamic_step(val_key, default_step=0.001):
    """Calculates a dynamic step size for number inputs based on the current value and a default step."""
    
    val = st.session_state.get(val_key)
    
    # Uses default step if the value is None or zero
    if val is None or val == 0:
        decimal_places = max(0, -Decimal(str(default_step)).as_tuple().exponent)
        return default_step, f"%.{decimal_places}f"
    
    # extracts the exponent from the Decimal representation of the value to determine the step size
    d = Decimal(str(val))
    exponent = d.as_tuple().exponent  # ex: 0.0004 -> exponent is -4
    
    if exponent < 0:
        step = float(Decimal(1).scaleb(exponent))  # -4 -> 0.0001
        return step, f"%0.{-exponent}f"

    return 1.0, "%.0f"


def latex_variable_name(name):
    """Returns the LaTeX spelling used for a user-defined variable name."""

    greek_latex_names = {
        "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon",
        "zeta", "eta", "theta", "vartheta", "iota", "kappa", "lambda",
        "mu", "nu", "xi", "pi", "varpi", "rho", "varrho", "sigma",
        "tau", "upsilon", "phi", "varphi", "chi", "psi", "omega",
    }
    return rf"\{name}" if name in greek_latex_names else name


def equation_latex_representation(equation, variables):
    """Renders an equation while preserving ordinary user-defined names."""

    symbol_names = {
        sp.Symbol(name): latex_variable_name(name)
        for name in variables
    }
    return sp.latex(equation, symbol_names=symbol_names)


def uncertainty_latex_representation(equation, variables):
    """Generates LaTeX representations for the symbolic and analytical uncertainty propagation expressions."""

    # Keep ordinary names unchanged while rendering Greek names as Greek symbols.
    latex_names = {name: latex_variable_name(name) for name in variables}
    sym_dict = {sp.Symbol(name): latex_name for name, latex_name in latex_names.items()}

    symbolic_expression = ""
    analytical_expression = ""
    
    # Loop through each variable to compute the symbolic and analytical expressions
    for name in variables:
        var_symbol = sp.Symbol(name)
        latex_name = latex_names[name]
        uncertainty = rf"u({{{latex_name}}})"

        # Symbolic representation
        symbolic_diff_latex = rf"\frac{{\partial R}}{{\partial {latex_name}}}"
        symbolic_expression += (
            rf"\left( {symbolic_diff_latex} \cdot {uncertainty} \right)^2 + "
        )

        # Analytical representation with the variable names
        diff_expr = sp.diff(equation, var_symbol)
        analytical_diff_latex = sp.latex(diff_expr, symbol_names=sym_dict)

        analytical_expression += (
            rf"\left( {analytical_diff_latex} \cdot {uncertainty} \right)^2 + "
        )
        
    return symbolic_expression[:-3], analytical_expression[:-3]  # Remove the last " + "


def get_excel_syntax(expression):
    """Converts a SymPy expression into a string formatted for Excel compatibility."""
    
    s = str(expression) 
    s = s.replace("**", "^")         # Replace exponentiation operator
    s = re.sub(r'\blog\(', 'LN(', s) # Converts log() to LN()

    # Convert standard functions to uppercase
    excel_funcs = ['sqrt', 'exp', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'abs']
    for f in excel_funcs:
        s = re.sub(rf'\b{f}\(', f.upper() + '(', s)

    return s


def uncertainty_excel_representation(equation, variables):
    """
    Generates the uncertainty propagation formula formatted for Excel.
    Example: =SQRT((diff_1 * u_var1)^2 + (diff_2 * u_var2)^2 + ...)
    """
    
    terms = []

    for name in variables:
        var_symbol = sp.Symbol(name)
        
        # uncertainty symbol for Excel representation
        unc_symbol = sp.Symbol(f"u_{name}")

        # partial derivative of the equation with respect to the variable
        diff_expr = sp.diff(equation, var_symbol)
        
        # Convert each term (dF/dx * u_x)^2
        term = (diff_expr * unc_symbol) ** 2
        terms.append(get_excel_syntax(term))

    # Adds all the terms inside the SQRT
    inner_sum = " + ".join(terms)
    
    return f"=SQRT({inner_sum})"


def compute_combined_uncertainty(equation, variables):
    """
    Computes the combined uncertainty using the law of propagation of uncertainty.
    The formula used is: u_c = sqrt(Σ(dF/dx * u_x)^2)
    """
    
    variance = sp.Integer(0)

    # Loop through each variable to compute the variance contribution
    for name, data in variables.items():
        
        sensibility_coeff = sp.diff(equation, sp.Symbol(name))
        variance += (sensibility_coeff * data["uncertainty"])**2

    # Extracts the variable values
    values = {
        name: data["value"]
        for name, data in variables.items()
        if data["value"] is not None
    }
    
    # Computes the combined uncertainty
    combined_uncertainty = sp.sqrt(variance.subs(values))
    
    return combined_uncertainty


def scientific_notation(value, decimals=3):
    """Converts a value to scientific notation and returns the mantissa and exponent."""
    
    try:
        val_float = float(value)
        scientific_result = f"{val_float:.{decimals}e}"
        
        if "e" in scientific_result:
            mantissa, exponent = scientific_result.split("e")
            return mantissa, int(exponent)
        
        return str(val_float), 0
    
    except (ValueError, TypeError):
        return str(value), 0


def compute_relative_uncertainty(combined_uncertainty, computed_result):
    """Computes the relative uncertainty as a percentage"""
    
    # Just to avoid division by zero, we check if the computed result is not too close to zero
    if abs(computed_result) > 1e-12:
        return (combined_uncertainty / abs(computed_result)) * 100
    else:
        return None
    
    
def compute_contributions(equation, variables, combined_uncertainty, values):
    """Computes the individual contributions of each variable to the combined uncertainty."""
    
    breakdown_data = []
    total_variance = combined_uncertainty ** 2

    for var_name, data in variables.items():

        sym = sp.Symbol(var_name)                         # Variable symbol/name
        u_i = float(data["uncertainty"])                  # Variable uncertainty

        # Sensitivity coefficient (partial derivative)
        try:
            c_i = float(sp.diff(equation, sym).subs(values))
        except (TypeError, ValueError, ZeroDivisionError):
            c_i = 0.0
            
        # Contribution percentage and relative uncertainty
        contribution = ((abs(c_i * u_i)) ** 2 / total_variance * 100) if total_variance > 0 else 0.0
        rel_uncertainty = (u_i / abs(data["value"]) * 100) if abs(data["value"]) > 1e-12 else 0.0
        
        breakdown_data.append({
            "Variable": var_name,
            "Value": data["value"],
            "Uncertainty": u_i,
            "Relative Uncertainty (%)": round(rel_uncertainty, 3),
            "Sensitivity Coefficients (cᵢ)": round(c_i, 4),
            "Contribution (%)": round(contribution, 2)
        })
    
    return breakdown_data