"""Main Module for the Streamlit application."""

from src.utils import spaces, add_var, remove_var, get_clean_equation, get_undefined_variable_names, get_dynamic_step, equation_latex_representation, uncertainty_latex_representation, uncertainty_excel_representation, compute_combined_uncertainty, scientific_notation, compute_relative_uncertainty, compute_contributions
from src.styles import apply_page_config, copy_excel_button, github_link, clickable_latex
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, convert_xor

import streamlit as st
import altair as alt
import pandas as pd
import sympy as sp
import math


# Apply configuration
apply_page_config()
github_link("https://github.com/joao-canais/Propagation-of-Uncertainty-Calculator.git")


# Global variables
RESULTS = False
CONST_EQUATION = False


# States Initialization
if "num_vars" not in st.session_state:
    st.session_state.num_vars = 2
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
if "render_state" not in st.session_state:
    st.session_state.render_state = True


# Main title and description
st.title("Propagation of Uncertainty Calculator")

st.markdown(
    """
    This is a tool designed for students and engineers to verify analytical error propagation step by step.
    Found an issue or want to request a feature? [Report here.](https://github.com/joao-canais/Propagation-of-Uncertainty-Calculator/issues/new)
    """
)

# Variables input section
st.header("Variables", help="Define the variable and their uncertainties. You can add up to 10 variables using the buttons below. Don't forget to convert all variables to the same units before entering values!")

cols = list(st.columns(5))
if st.session_state.num_vars > 5:
    st.markdown("<hr style='margin-top: 15px; margin-bottom: 30px; opacity: 1;'>", unsafe_allow_html=True)
    cols += list(st.columns(5))
    
variables = {}

# Variable input fields
for i in range(st.session_state.num_vars):
    with cols[i]:
        var_name = st.text_input(
            f"Variable {i+1} Name",
            key=f"var{i+1}_name",
            placeholder=f"Variable {i+1} Name",
            label_visibility="collapsed"
        )
        
        val_key = f"var{i+1}_value"
        unc_key = f"var{i+1}_uncertainty"
        
        # Calcula o step com base no que já está no state
        value_step, value_format = get_dynamic_step(val_key, default_step=0.001)
        unc_step, unc_format = get_dynamic_step(unc_key, default_step=0.001)

        var_value = st.number_input(
            "Value",
            key=val_key,
            value=None,
            placeholder="1.000",
            step=value_step,
            format=value_format,
        )

        var_uncertainty = st.number_input(
            "Uncertainty",
            key=unc_key,
            value=None,
            placeholder="0.001",
            step=unc_step,
            format=unc_format,
        )
        
        if var_name:
            variables[var_name] = {
                "value": var_value,
                "uncertainty": var_uncertainty,
            }

# Gather all the values
values = {
    name: data["value"]
    for name, data in variables.items()
    if data["value"] is not None
}
# Checks for missing values and uncertainties
missing_values = [
    name for name, data in variables.items()
    if data["value"] is None
]
missing_uncertainties = [
    name for name, data in variables.items()
    if data["uncertainty"] is None
]
   
# Buttons (+/-)
col_ctrl1, col_ctrl2, _ = st.columns([1, 1, 25])
with col_ctrl1:
    st.button(
        "",
        icon=":material/add:",
        on_click=add_var,
        disabled=st.session_state.num_vars >= 10
    )
with col_ctrl2:
    st.button(
        "",
        icon=":material/remove:",
        on_click=remove_var,
        disabled=st.session_state.num_vars <= 1
    )
       
 
# Equation input section
help_msg = "Once you type a valid equation, you can copy the LaTeX code of the equation by clicking on it." if st.session_state.render_state else "At the moment, the LaTeX copy functionality is not working."
st.header("Equation", help=help_msg)

with st.expander(r"Click here to view some **Syntax Tips:**", expanded=False, type="step"):
    st.markdown(r"""
        * **Use the variable names that you defined above.** For example, if you named your variables x, y, and z, write equations like `x * y / z` (the spaces are not mandatory).
        * **Basic operators:** Use `+` (addition), `-` (subtraction), `*` (multiplication) and `/` (division).
        * **Grouping:** Use parentheses `()` to group operations and control evaluation order.
        * **Powers & Roots:** Use  `**` or `^` for exponentiation and `sqrt()` for square roots. For example, `x**2` or `x^2` and `sqrt(x)` or `x**(1/2)`.
        * **Functions:** `sin()`, `cos()`, `tan()`, `log()`, `exp()`, etc. For example, `sin(x)` or `log(y)`.
        * **Constants:** You can use constants like `pi` and `e` (or `exp()` like before). For example, `pi * x` or `e**x`. Therefore, avoid using them as variable names.
        * **Undefined operations:** Avoid operations such as division by zero or taking the square root of a negative number
        * **Problematic naming:** You can use spell out Greek letter names, like `theta` or `mu`, instead of using symbols like $\theta$ or $\mu$. Also avoid using `lambda` ($\lambda$), since its a [Python keyword](https://www.w3schools.com/Python/python_ref_keywords.asp).
        """)

col1, col2 = st.columns([0.03, 1.0], vertical_alignment="center")

with col1:
    st.markdown(r"$\large R =$")
with col2:
    equation = st.text_input(
        label="Equation input",
        key="equation",
        placeholder="x * y / z",
        label_visibility="collapsed",
    )   

# After the user inputs the equation:
st.session_state.render_state = True
if equation.strip():
    try:
        # Cleans the equation in order to be compatible with sympy parsing
        clean_equation = get_clean_equation(equation)

        # Parse the equation to check for undefined variables
        transformations = standard_transformations + (convert_xor,)
        parsed_equation = parse_expr(clean_equation, transformations=transformations,
                               local_dict={
                                   **{name: sp.Symbol(name) for name in variables},
                                   "e": sp.E,
                                   "lambda_": sp.Symbol("lambda"),
                               })

        # Exctracts ALL symbol names from the parsed equation for the LaTeX equation representation
        equation_symbol_names = {
            symbol.name
            for symbol in parsed_equation.free_symbols
        }
        expression_string = rf"R ={equation_latex_representation(parsed_equation, equation_symbol_names)}"
        spaces(1)
        
        # Check for undefined variables
        undefined_variables = get_undefined_variable_names(clean_equation)
        if undefined_variables:
            missing = ", ".join(f"`{name}`" for name in undefined_variables)
            st.markdown(f":red[Variable(s) not defined: {missing}]")
        else:
            RESULTS = True
            
        equation_rendered = clickable_latex(expression_string, height=120, help="Copy LaTeX code to clipboard")
        if not equation_rendered:
            # changes the help message to indicate that the LaTeX copy functionality is not working
            st.session_state.render_state = False
            
        
    except ValueError as error:
        st.markdown(f":red[Equation not valid: {error}]")
    except Exception:
        st.markdown(":red[Equation not valid...]")
        

# Results section
if RESULTS==True:

    st.divider()
    
    help_unc_msg = "You can also copy the LaTeX code of the uncertainty propagation formula by clicking on the formulas below." if st.session_state.render_state else "At the moment, the LaTeX copy functionality is not working."
    st.header("Uncertainty Propagation Formula", help=help_unc_msg)
    
    # Extracts ONLY the variables present in the equation
    eq_variables = {
        name: variables[name]
        for name in (s.name for s in parsed_equation.free_symbols)
        if name in variables
    }
    

    # If the equation has variables, compute the uncertainty propagation formula
    if eq_variables:
        
        symbolic_expression, analytical_expression = uncertainty_latex_representation(parsed_equation, eq_variables)
        
        if symbolic_expression and analytical_expression:
            symbolic_expression_string = rf"u_R = \sqrt{{{symbolic_expression}}}"
            analytical_expression_string = rf"\Leftrightarrow u_R = \sqrt{{{analytical_expression}}}"
        
            # Copy the LaTeX code by clicking
            symbolic_rendered = clickable_latex(symbolic_expression_string, height=130, help="Copy LaTeX code to clipboard")
            spaces(2)
            analytical_rendered = clickable_latex(analytical_expression_string, height=150, help="Copy LaTeX code to clipboard")

            if not symbolic_rendered or not analytical_rendered:
                st.session_state.render_state = False
        
            spaces(1)
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Excel Button
                excel_expression = uncertainty_excel_representation(parsed_equation, eq_variables)
                copy_excel_button(excel_expression, caption="Copy Uncertainty Propagation Formula to Excel", height=50)
            with col2:
                # Tip for Excel
                st.markdown(
                        """
                        <div style="display: flex; align-items: center; height: 35px;">
                            <small style="color: #dadde0a6;"><b>Tip: replace your variable names with their corresponding Excel cells (ex: A1, B2...). After that, you only need to replace the uncertainties.</b></small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.markdown(":red[The uncertainty propagation formula cannot be defined. Check your equation and variables.]")
            
    # In case the equation is constant (by user mistake), the uncertainty propagation formula will be empty
    else:
        CONST_EQUATION = True
        st.caption("Your equation is constant (contains no variables), therefore the uncertainty is simply zero.")

    
    st.divider()
    
    # Final Result Section
    st.header("Final Result")
    
    if missing_values:
        # Displays a warning message
        missing = ", ".join(f"`{name}`" for name in missing_values)
        st.markdown(f":red[Please provide values for: {missing}]")
    else:
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Compute the result of the equation with the provided values
            computed_result = parsed_equation.subs(values)
            try:
                computed_result_value = float(computed_result)
                result_is_finite = math.isfinite(computed_result_value)
            except (TypeError, ValueError, OverflowError):
                result_is_finite = False

            if result_is_finite:
                st.latex(rf"\LARGE R = {sp.latex(computed_result)}")

                coeff, exponent = scientific_notation(computed_result, decimals=3)

                formula = rf"\LARGE \Leftrightarrow R = {coeff} \times 10^{{{exponent}}}" if exponent != 0 else rf"\LARGE \Leftrightarrow R = {coeff}"
                st.latex(formula)
                
            else:
                # Prevents problems like division by zero or undefined results
                st.markdown(":red[The equation cannot be defined. Check your values and equation.]")
            
        with col2:
            if missing_uncertainties:
                # Displays a warning message
                missing = ", ".join(f"`{name}`" for name in missing_uncertainties)
                st.markdown(f":red[Please provide uncertainties for: {missing}]")
            else:
                    # Compute the combined uncertainty
                    try:
                        combined_uncertainty = compute_combined_uncertainty(parsed_equation, eq_variables)
                        combined_uncertainty_value = float(combined_uncertainty)
                        uncertainty_is_finite = math.isfinite(combined_uncertainty_value)
                    except (TypeError, ValueError, OverflowError, ZeroDivisionError):
                        combined_uncertainty = None
                        uncertainty_is_finite = False

                    if uncertainty_is_finite:
                        st.latex(rf"\LARGE u_R = {sp.latex(combined_uncertainty)}")

                        coeff_u, exponent_u = scientific_notation(combined_uncertainty, decimals=3)

                        formula_u = rf"\LARGE \Leftrightarrow u_R = {coeff_u} \times 10^{{{exponent_u}}}" if exponent_u != 0 else rf"\LARGE \Leftrightarrow u_R = {coeff_u}"
                        st.latex(formula_u)
                    else:
                        st.markdown(":red[The combined uncertainty cannot be defined. Check your values, uncertainties and equation.]")
                
        # Final result with uncertainty display
        if not missing_uncertainties and result_is_finite and uncertainty_is_finite:
            
            common_exponent = int(exponent)
            uncertainty_mantissa = float(coeff_u) * 10 ** (int(exponent_u) - common_exponent)

            final_result = (
                rf"R = ({coeff} \pm {uncertainty_mantissa:.3f})"
                rf" \times 10^{{{common_exponent}}}"
                if common_exponent != 0
                else rf"R = ({coeff} \pm {uncertainty_mantissa:.3f})"
            )

            spaces(1)
            st.latex(rf"\LARGE {{{final_result}}}", help="Don't forget to add the unit in the final result if needed!")
            spaces(1)
        
        
            # Relative Uncertainty and Contributions (Bonus Section)
            if CONST_EQUATION==False and len(eq_variables) > 1:
                
                spaces(2)
                
                with st.expander("Relative Uncertainty & Contributions (Bonus)", expanded=False):
                    
                    result = float(computed_result)
                    uncertainty = float(combined_uncertainty)

                    relative_uncertainty = compute_relative_uncertainty(uncertainty, result)

                    col_metric, col_formulas = st.columns([1, 4.5])

                    with col_metric:
                        if relative_uncertainty is not None:
                            st.metric("Total Relative Uncertainty", f"{relative_uncertainty:.1f} %")
                        else:
                            st.write(r"Relative uncertainty is undefined when $R \approx 0$.")

                    with col_formulas:
                        
                        with st.expander("Formulas", expanded=False, type="step"):

                            latex_equations = r"""
                            \begin{aligned}
                            \text{Rel. Uncertainty (\%): } & u_{r}(x_i) = \frac{u(x_i)}{|x_i|} \times 100 \hspace{1.5cm}
                            \text{Sensitivity Coeff.: } c_i = \frac{\partial R}{\partial x_i} \hspace{1.5cm}
                            \text{Contribution (\%)} = \frac{\left(c_i \cdot u(x_i)\right)^2}{u_R^2} \times 100
                            \end{aligned}
                            """
                            st.latex(latex_equations)

                    breakdown_data = compute_contributions(parsed_equation, eq_variables, uncertainty, values)
                    
                    st.dataframe(breakdown_data, width='stretch')

                    spaces(1)
                    
                    df = pd.DataFrame(breakdown_data)

                    chart = (
                        alt.Chart(df)
                        .mark_bar()
                        .encode(
                            x=alt.X("Variable:N", axis=alt.Axis(labelAngle=0)),
                            y=alt.Y("Contribution (%):Q", scale=alt.Scale(domain=[0, 100])),
                            tooltip=["Variable", "Contribution (%)"]
                        )
                        .properties(
                            title=alt.TitleParams(
                                text="Uncertainty Contribution per Variable",
                                anchor="middle",    
                                fontSize=15,        
                                fontWeight="bold",
                                color="#ffffff"    
                            )
                        )
                    )
                    st.altair_chart(chart, width='stretch')
                    
                    # spaces(4)
                
                
    
if RESULTS:
    st.divider()
else:
    st.markdown("<hr style='margin-top: 170px; margin-bottom: 30px; opacity: 1;'>", unsafe_allow_html=True)
    
col1, col2 = st.columns([10, 1])
with col1:
    st.caption(
        "This tool is for educational purposes. Verify your own calculations!"
    )
with col2:
    st.caption(
        "© 2026 João Canais",
    )
