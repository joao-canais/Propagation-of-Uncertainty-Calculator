"Module with theoretical foundations and mathematical principles behind the propagation of uncertainty."

from src.styles import apply_page_config, github_link, disable_streamlit_scrollbar, clickable_latex

import pandas as pd
import streamlit as st

# Apply configuration
apply_page_config()
disable_streamlit_scrollbar()
github_link("https://github.com/joao-canais/Propagation-of-Uncertainty-Calculator.git")

tab1, tab2 = st.tabs(["English", "Portuguese"])

# English version
with tab1:
    
    st.caption(
        "*This section was created to help understand the theoretical foundations and mathematical principles behind the propagation of uncertainty, including formulas and a worked example.*"
    )
    st.title("Fundamentals of Propagation of Uncertainty")
    st.markdown(
        r"""
    In most scientific and engineering testing, the physical quantity of
    ultimate interest (the **output measurand** $Y$) is not measured directly.
    Instead, it is obtained indirectly from one or more input quantities $(X_i)$, whose values are estimated through the measurement process or from other relevant information:
    """
    )
    st.latex(r"\large Y=f(X_1,X_2,\dots,X_N)")
    st.markdown("**Common examples:**")
    st.markdown(
        r"""
    - **Area of a rectangle:** $A=a \cdot b$, as a function of width $a$ and length $b$;
    - **Density of a body:** $\rho=\dfrac{m}{V}$, as a function of mass $m$ and volume $V$;
    - **Acceleration due to gravity via simple pendulum:** $g=\dfrac{4\pi^2L}{T^2}$, as a function of length $L$ and period of oscillation $T$.
    """
    )
    st.markdown(
        r"""
    If each input quantity $X_i$ has an estimate $x_i$ and a
    standard uncertainty $u(x_i)$, the Law of Propagation of Uncertainty allows
    the determination of the combined standard uncertainty of the estimate of the output quantity $Y$.
    """
    )
    st.header("Taylor Series Expansion")
    st.markdown(
        r"""
    When the functional relationship $f$ is non-linear, the propagation of uncertainty
    can be approximated using a Taylor series expansion. Considering
    a first-order approximation about the estimated values
    $x_1,x_2,\dots,x_N$, we have:
    """
    )
    st.latex(
        r"""
        \large
        \begin{aligned}
        f(X_1,\dots,X_N)
        &\approx
        f(x_1,\dots,x_N)
        + \sum_{i=1}^{N}
        \left.
        \frac{\partial f}{\partial x_i}
        \right|_{\mathbf{x}}
        (X_i-x_i)
        \end{aligned}
        """
    )
    st.markdown(
        r"""
    where $\left.\dfrac{\partial f}{\partial x_i}\right|_{\mathbf{x}}$
    represents the partial derivative of $f$ with respect to the quantity $x_i$.
    This linear approximation relates small variations in the input quantities
    to the corresponding variation in the output quantity. Thus, the
    coefficients
    """
    )
    st.latex(r"""\large c_i= \left.\frac{\partial f}{\partial x_i}\right|_{\mathbf{x}}""")
    
    st.markdown(
        """
    are termed **sensitivity coefficients** and quantify the
    sensitivity of the output quantity to variations in each input quantity.
    """
    )
    st.header("Law of Propagation of Uncertainty")
    st.markdown(
        """
    From the first-order approximation, the variance (or the square of the standard uncertainty) of the output quantity
    can be written, in its most general form, as:"""
    )
    st.latex(r"""\large u_c^2(y) = \sum_{i=1}^{N} \left( \frac{\partial f}{\partial x_i} \right)^2 u^2(x_i) + 2 \sum_{i<j} \frac{\partial f}{\partial x_i} \frac{\partial f}{\partial x_j} \text{cov}(x_i, x_j)""")
    st.markdown("""            
    where the first term represents the contribution of the individual uncertainties of each input quantity and the
    second term accounts for the correlation (covariance) between them.
    """)            
    st.markdown("""                
    However, for **independent or uncorrelated** input quantities, the covariance terms **are zero**, leaving only the first term:
    """    )
    st.latex(
        r"""
        \large
        u_c^2(y)
        =
        \sum_{i=1}^{N}
        \left(
        \frac{\partial f}{\partial x_i}
        \right)^2
        u^2(x_i)
        """
    )
    st.markdown("or, equivalently:")
    st.latex(
        r"""
        \large
        u_c^2(y)=\sum_{i=1}^{N}c_i^2u^2(x_i)\hspace{1mm},
        \qquad
        c_i=\frac{\partial f}{\partial x_i}
        """
    )
    st.markdown("""
    This expression shows that each input uncertainty contributes to the
    final uncertainty according to its magnitude and its respective sensitivity
    coefficient. The contribution of each quantity to the total variance is given by:
    """)
    st.latex(r"\large c_i^2u^2(x_i)")
    st.markdown(
        r"""
    Therefore, a greater sensitivity $|c_i|$ or a larger input uncertainty
    $u(x_i)$ generally leads to a greater contribution to the combined uncertainty.
    Thus, the standard form of the Propagation Law for multiple independent variables is given by:
    """
    )
    st.latex(
        r"""
        \large
        \boxed{
        u_c(y)=
        \sqrt{
        \sum_{i=1}^{N}
        c_i^2u^2(x_i)
        }}
        """
    )
    st.markdown("or, equivalently:")
    st.latex(
        r"""
        \large
        u_c(y)=
        \sqrt{
        \left(\frac{\partial f}{\partial x_1}\right)^2u^2(x_1)
        +
        \left(\frac{\partial f}{\partial x_2}\right)^2u^2(x_2)
        +
        \left(\frac{\partial f}{\partial x_3}\right)^2u^2(x_3)
        +\dots
        }
        """
    )
    st.markdown(
        """*Note: The Law of Propagation of Uncertainty presented here results from a first-order approximation.
        When the non-linearity of the model is significant, it may be necessary to consider higher-order
        terms or use methods such as **Monte Carlo** propagation.*
    """)
    st.header("Relative Uncertainty")
    st.markdown(
        """
    The relative uncertainty corresponds to the ratio of the standard uncertainty of the
    quantity to the absolute value of its estimate:
    """
    )
    st.latex(
        r"""
        \large
        \boxed{
        \frac{u_c(y)}{|y|}
        }
        """
    )
    st.markdown(
        """
    and is a dimensionless quantity, often expressed as a percentage:
    """
    )
    st.latex(r"\large \frac{u_c(y)}{|y|}\times100\%")
    st.markdown(
        """
    The relative form is particularly useful for comparing the importance of
    different input quantities and for analysing the contribution of
    each to the final uncertainty.
    """
    )
    st.header("Summary Tables of Uncertainty Propagation")
    st.markdown(
        """
    The tables below summarize the analytical expressions for the four
    fundamental operations from two complementary perspectives: combined standard uncertainty and relative uncertainty.
    """
    )
    st.subheader("1. Propagation of Combined Standard Uncertainty")
    absolute_data = [
        [
            r"$\large\text{Addition and Subtraction}$",
            r"$\large z = x \pm y$",
            r"$\large |u_c(x \pm y)| = \sqrt{u^2(x) + u^2(y)}$",
        ],
        [
            r"$\large\text{Product}$",
            r"$\large z = x \cdot y$",
            r"$\large |u_c(xy)| = \sqrt{y^2u^2(x) + x^2u^2(y)}$",
        ],
        [
            r"$\large\text{Quotient}$",
            r"$\large z = \dfrac{x}{y}$",
            r"$\large |u_c\left(\frac{x}{y}\right)| = \sqrt{\left(\dfrac{1}{y}\right)^2u^2(x)+\left(-\dfrac{x}{y^2}\right)^2u^2(y)}$",
        ],
        [
            r"$\large\text{Power}$",
            r"$\large z = x^n$",
            r"$\large |u_c(x^n)| = \sqrt{(n x^{n-1})^2u^2(x)} = |n x^{n-1}u(x)|$",
        ],
    ]
    st.table(
        {
            r"$\large\text{Operation}$": [row[0] for row in absolute_data],
            r"$\large\text{Resulting Quantity } (z)$": [
                row[1] for row in absolute_data
            ],
            r"$\large\text{Combined Standard Uncertainty } u_c(z)$": [
                row[2] for row in absolute_data
            ],
        }
    )
    st.caption(
        "Analytical expressions for combined standard uncertainty with uncorrelated quantities."
    )
    st.subheader("2. Propagation of Relative Uncertainty")
    relative_data = [
        [
            r"$\large\text{Addition and Subtraction}$",
            r"$\large z = x \pm y$",
            r"$\large \dfrac{u_c(z)}{|z|} = \dfrac{\sqrt{u^2(x)+u^2(y)}}{|x\pm y|}$",
        ],
        [
            r"$\large\text{Product}$",
            r"$\large z = x \cdot y$",
            r"$\large \dfrac{u_c(z)}{|z|} = \sqrt{\left(\dfrac{u(x)}{x}\right)^2+\left(\dfrac{u(y)}{y}\right)^2}$",
        ],
        [
            r"$\large\text{Quotient}$",
            r"$\large z = \dfrac{x}{y}$",
            r"$\large \dfrac{u_c(z)}{|z|} = \sqrt{\left(\dfrac{u(x)}{x}\right)^2+\left(\dfrac{u(y)}{y}\right)^2}$",
        ],
        [
            r"$\large\text{Power}$",
            r"$\large z = x^n$",
            r"$\large \dfrac{u_c(z)}{|z|} = |n|\dfrac{u(x)}{|x|}$",
        ],
    ]
    st.table(
        {
            r"$\large\text{Operation}$": [row[0] for row in relative_data],
            r"$\large\text{Resulting Quantity } (z)$": [row[1] for row in relative_data],
            r"$\large\text{Relative Uncertainty } \left(\dfrac{u_c(z)}{|z|}\right)$": [
                row[2] for row in relative_data
            ],
        }
    )
    st.caption(
        "Analytical expressions for relative uncertainty with uncorrelated quantities."
    )
    st.header("Worked Example")
    st.markdown(
        r"""
    Determine the density $\rho$ of a solid cylinder from
    the measurements (assumed uncorrelated) of its mass $m$, diameter $d$, and length $l$.
    """
    )
    st.markdown("")
    st.markdown("#### Measurement data:")
    c_massa, sep1, c_diam, sep2, c_comp = st.columns([1, 0.05, 1, 0.05, 1])
    with c_massa:
        st.markdown("**Mass:**")
        st.latex(r"\large m=(185.40\pm0.05)\,\mathrm{g}")
        st.latex(r"\large u(m)=0.05\,\mathrm{g}")
    with sep1:
        st.markdown(
            """
            <div style="
                border-left: 1.5px solid rgba(255, 255, 255, 0.2);
                height: 150px;
                margin: auto;
            "></div>
            """,
            unsafe_allow_html=True,
        )
    with c_diam:
        st.markdown("**Diameter:**")
        st.latex(r"\large d=(20.00\pm0.02)\,\mathrm{mm}")
        st.latex(r"\large u(d)=0.02\,\mathrm{mm}")
    with sep2:
        st.markdown(
            """
            <div style="
                border-left: 1.5px solid rgba(255, 255, 255, 0.2);
                height: 150px;
                margin: auto;
            "></div>
            """,
            unsafe_allow_html=True,
        )
    with c_comp:
        st.markdown("**Length:**")
        st.latex(r"\large l=(40.00\pm0.05)\,\mathrm{mm}")
        st.latex(r"\large u(l)=0.05\,\mathrm{mm}")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown(r"""
    The volume of the cylinder is $V=\dfrac{\pi d^2 l}{4}$. The density is obtained from:
    """
    )
    st.latex(
        r"""
        \large
        \rho
        =\frac{m}{V}
        =\frac{4m}{\pi d^2l}
        """
    )
    st.markdown(r"**1. Calculation of the value of $\rho$:**")
    st.markdown(
        r"""
    Converting the dimensions to centimetres
    ($d=2.000\,\mathrm{cm}$ and $l=4.000\,\mathrm{cm}$):
    """
    )
    st.latex(
        r"""
        \large
        \rho=
        \frac{4\times185.40}
        {\pi\times(2.000)^2\times4.000}
        =
        \frac{741.60}{50.2655}
        \approx14.7538\,\mathrm{g/cm^3}
        """
    )
    st.markdown(r"**2. Calculation of Combined Standard Uncertainty $u_c(\rho)$:**")
    st.markdown(
        r"""
    The combined standard uncertainty can be calculated directly using the Law
    of Propagation of Uncertainty:
    """
    )
    st.latex(
        r"""
        \large
        u_c(\rho)=
        \sqrt{
        \left(\frac{\partial\rho}{\partial m}u(m)\right)^2+
        \left(\frac{\partial\rho}{\partial d}u(d)\right)^2+
        \left(\frac{\partial\rho}{\partial l}u(l)\right)^2
        }
        """
    )
    st.markdown(r"""
        For $\normalsize{\rho=\frac{4m}{\pi d^2l}}$, the partial derivatives are:
        """)
    st.latex(
        r"""
        \large
        \frac{\partial\rho}{\partial m}
        =\frac{4}{\pi d^2l}
        =\frac{\rho}{m},
        \qquad
        \frac{\partial\rho}{\partial d}
        =-\frac{4m}{\pi d^3l}
        =-\frac{2\rho}{d},
        \qquad
        \frac{\partial\rho}{\partial l}
        =-\frac{4m}{\pi d^2l^2}
        =-\frac{\rho}{l}
        """
    )
    st.markdown("Thus we have:")
    st.latex(
        r"""
        \large
        u_c(\rho)=
        \rho\sqrt{
        \left(\frac{u(m)}{m}\right)^2+
        4\left(\frac{u(d)}{d}\right)^2+
        \left(\frac{u(l)}{l}\right)^2
        }
        """
    )
    st.markdown("Substituting the values:")
    st.latex(
        r"""
        \large
        u_c(\rho)=
        14.7538
        \sqrt{
        \left(\frac{0.05}{185.40}\right)^2+
        4\left(\frac{0.02}{20.00}\right)^2+
        \left(\frac{0.05}{40.00}\right)^2
        }
        """
    )
    st.markdown("Therefore, the combined standard uncertainty is:")
    st.latex(
        r"""
        \large
        \boxed{
        u_c(\rho)\approx0.0350\,\mathrm{g/cm^3}
        }
        """
    )
    st.markdown(r"**3. Calculation of Relative Uncertainty:**")
    st.markdown(
        r"""
    To express the relative uncertainty, divide the
    combined standard uncertainty by the central value of $\rho$:
    """
    )
    st.latex(
        r"""
        \large
        \frac{u_c(\rho)}{\rho}
        =
        \sqrt{
        \left(\frac{u(m)}{m}\right)^2+
        4\left(\frac{u(d)}{d}\right)^2+
        \left(\frac{u(l)}{l}\right)^2
        }
        """
    )
    st.markdown("Thus:")
    st.latex(
        r"""
        \large
        \frac{u_c(\rho)}{\rho}
        =
        \sqrt{
        \left(\frac{0.05}{185.40}\right)^2+
        4\left(\frac{0.02}{20.00}\right)^2+
        \left(\frac{0.05}{40.00}\right)^2
        }
        """
    )
    st.markdown("Or alternatively:")
    st.latex(
        r"""
        \large
        \frac{u_c(\rho)}{\rho}
        =
        \sqrt{
        (0.0002697)^2+
        4(0.001000)^2+
        (0.001250)^2
        }
        """
    )
    st.latex(
        r"""
        \large
        \boxed{
        \frac{u_c(\rho)}{\rho}
        =\frac{0.0350}{14.7538}
        \approx0.002372
        =0.237\%
        }
        """
    )
    st.markdown("**4. Relative Contribution of each Quantity:**")
    st.markdown(
        """
        The contribution of each input quantity is obtained by dividing
        its squared term by the total combined relative variance (total contribution):
        """
    )
    st.latex(
        r"""
        \large C_{\mathrm{total}} = \left(\frac{u_c(\rho)}{\rho}\right)^2 \approx 5.627666\times10^{-6}
        """
    )
    st.latex(
        r"""
        \large
        \text{Mass } (m)\!: \quad \frac{(0.0002697)^2}{C_{\mathrm{total}}}\times 100\% \approx 1.3\%
        """
    )
    st.latex(
        r"""
        \large
        \text{Diameter } (d)\!: \quad \frac{4(0.001000)^2}{C_{\mathrm{total}}}\times 100\% \approx 71.0\%
        """
    )
    st.latex(
        r"""
        \large
        \text{Length } (l)\!: \quad \frac{(0.001250)^2}{C_{\mathrm{total}}}\times 100\% \approx 27.8\%
        """
    )
    st.markdown("Thus, the relative contributions are:")
    st.markdown(
        """
    - **Mass:** ≈ 1.3%
    - **Diameter:** ≈ 71.0%
    - **Length:** ≈ 27.8%
    """
    )
    st.markdown(
        """
    *Conclusion:* The diameter has the largest contribution to the combined variance of the density. Therefore, improving the measurement of the diameter
    will have the greatest impact on reducing the uncertainty.
    """
    )
    st.markdown("**5. Final Result:**")
    st.latex(
        r"""
        \large
        \boxed{
        \rho=(14.754\pm0.035)\,\mathrm{g/cm^3}
        }
        """
    )
    
# Portuguese version
with tab2:

    st.caption(
    "*Esta secção foi criada para ajudar a compreender os fundamentos teóricos e os princípios matemáticos por detrás da propagação de incertezas, incluindo fórmulas e um exemplo didático.*"
    )
    
    st.title("Fundamentos de Propagação de Incertezas")

    st.markdown(
        r"""
    Na maioria dos ensaios científicos e de engenharia, a grandeza física de
    interesse final (a **mensuranda de saída** $Y$) não é medida diretamente.
    Em vez disso, é obtida indiretamente a partir de uma ou mais grandezas de entrada $(X_i)$, cujos valores são estimados através do processo de medição ou de outras informações relevantes:
    """
    )
     
    st.latex(r"\large Y=f(X_1,X_2,\dots,X_N)")

    st.markdown("**Exemplos comuns:**")

    st.markdown(
        r"""
    - **Área de um retângulo:** $A=a \cdot b$, em função da largura $a$ e do comprimento $b$;
    - **Densidade de um corpo:** $\rho=\dfrac{m}{V}$, em função da massa $m$ e do volume $V$;
    - **Aceleração da gravidade por pêndulo simples:** $g=\dfrac{4\pi^2L}{T^2}$, em função do comprimento $L$ e do período de oscilação $T$.
    """
    )

    st.markdown(
        r"""
    Se cada grandeza de entrada $X_i$ possui uma estimativa $x_i$ e uma
    incerteza-padrão $u(x_i)$, a Lei de Propagação de Incertezas permite
    determinar a incerteza-padrão combinada da estimativa da grandeza de saída $Y$.
    """
    )

    st.header("Expansão da Série de Taylor")

    st.markdown(
        r"""
    Quando o modelo funcional $f$ é não linear, a propagação das incertezas
    pode ser aproximada através da expansão da Série de Taylor. Considerando
    uma aproximação de primeira ordem em torno dos valores estimados
    $x_1,x_2,\dots,x_N$, tem-se:
    """
    )

    st.latex(
        r"""
        \large
        \begin{aligned}
        f(X_1,\dots,X_N)
        &\approx
        f(x_1,\dots,x_N)
        + \sum_{i=1}^{N}
        \left.
        \frac{\partial f}{\partial x_i}
        \right|_{\mathbf{x}}
        (X_i-x_i)
        \end{aligned}
        """
    )

    st.markdown(
        r"""
    onde $\left.\dfrac{\partial f}{\partial x_i}\right|_{\mathbf{x}}$
    representa a derivada parcial de $f$ relativamente à grandeza $x_i$.

    Esta aproximação linear permite relacionar pequenas variações nas grandezas
    de entrada com a correspondente variação da grandeza de saída. Assim, os
    coeficientes
    """
    )

    st.latex(
        r"""
        \large
        c_i=
        \left.
        \frac{\partial f}{\partial x_i}
        \right|_{\mathbf{x}}
        """
    )

    st.markdown(
        """
    são designados por **coeficientes de sensibilidade** e quantificam a
    sensibilidade da grandeza de saída às variações de cada grandeza de entrada.
    """
    )

    st.header("Lei de Propagação de Incertezas")

    st.markdown(
        """
    A partir da aproximação de primeira ordem, a variância (ou o quadrado da incerteza-padrão) da grandeza de saída
    pode ser escrita, na forma mais genérica, como:""")
    
    st.latex(r"""\large u_c^2(y) = \sum_{i=1}^{N} \left( \frac{\partial f}{\partial x_i} \right)^2 u^2(x_i) + 2 \sum_{i<j} \frac{\partial f}{\partial x_i} \frac{\partial f}{\partial x_j} \text{cov}(x_i, x_j)""")
    
    
    st.markdown("""             
    Onde o primeiro termo representa a contribuição das incertezas individuais de cada grandeza de entrada e o 
    segundo termo contabiliza a correlação (covariância) entre elas.
    """)            
    
    st.markdown("""                
    No entanto, para grandezas de entrada **independentes ou não correlacionadas**, os termos de covariância **são nulos**, ficando apenas o primeiro termo:
    """    )

    st.latex(
        r"""
        \large
        u_c^2(y)
        =
        \sum_{i=1}^{N}
        \left(
        \frac{\partial f}{\partial x_i}
        \right)^2
        u^2(x_i)
        """
    )

    st.markdown("ou, de forma equivalente:")

    st.latex(
        r"""
        \large
        u_c^2(y)=\sum_{i=1}^{N}c_i^2u^2(x_i)\hspace{1mm},
        \qquad
        c_i=\frac{\partial f}{\partial x_i}
        """
    )


    st.markdown("""
    Esta expressão mostra que cada incerteza de entrada contribui para a
    incerteza final de acordo com a sua magnitude e com o respetivo coeficiente
    de sensibilidade. A contribuição de cada grandeza para a variância total é dado por:
    """)

    st.latex(r"\large c_i^2u^2(x_i)")

    st.markdown(
        r"""
    Pelo que uma maior sensibilidade $|c_i|$ ou uma maior incerteza de entrada
    $u(x_i)$ conduz, em geral, a uma maior contribuição para a incerteza combinada.

    Assim, a forma habitual da Lei de Propagação para múltiplas variáveis independentes é dada por:
    """
    )
    
    st.latex(
        r"""
        \large
        \boxed{
        u_c(y)=
        \sqrt{
        \sum_{i=1}^{N}
        c_i^2u^2(x_i)
        }}
        """
    )

    st.markdown("ou, de forma equivalente:")
    
    st.latex(
        r"""
        \large
        u_c(y)=
        \sqrt{
        \left(\frac{\partial f}{\partial x_1}\right)^2u^2(x_1)
        +
        \left(\frac{\partial f}{\partial x_2}\right)^2u^2(x_2)
        +
        \left(\frac{\partial f}{\partial x_3}\right)^2u^2(x_3)
        +\dots
        }
        """
    )
                
    st.markdown(
        """*Nota: A Lei de Propagação de Incertezas apresentada resulta de uma aproximação de primeira ordem. 
        Quando a não linearidade do modelo é significativa, pode ser necessário considerar termos de ordem 
        superior ou utilizar métodos como a propagação de **Monte Carlo.***
    """)

    st.header("Incerteza Relativa")

    st.markdown(
        """
    A incerteza relativa corresponde à razão entre a incerteza-padrão da
    grandeza e o módulo do seu valor estimado:
    """
    )

    st.latex(
        r"""
        \large
        \boxed{
        \frac{u_c(y)}{|y|}
        }
        """
    )

    st.markdown(
        """
    e é uma grandeza adimensional, sendo frequentemente expressa em percentagem:
    """
    )

    st.latex(r"\large \frac{u_c(y)}{|y|}\times100\%")

    st.markdown(
        """
    A forma relativa é particularmente útil para comparar a importância das
    diferentes grandezas de entrada e para analisar a contribuição de
    cada uma para a incerteza final.
    """
    )

    st.header("Quadros Resumo de Propagação de Incertezas")

    st.markdown(
        """
    As tabelas abaixo sistematizam as expressões analíticas para as quatro
    operações fundamentais em duas perspetivas complementares: a incerteza-padrão combinada e a incerteza relativa.
    """
    )

    st.subheader("1. Propagação da Incerteza-Padrão Combinada")

    absolute_data = [
        [
            r"$\large\text{Soma e Subtração}$",
            r"$\large z = x \pm y$",
            r"$\large |u_c(x \pm y)| = \sqrt{u^2(x) + u^2(y)}$",
        ],
        [
            r"$\large\text{Produto}$",
            r"$\large z = x \cdot y$",
            r"$\large |u_c(xy)| = \sqrt{y^2u^2(x) + x^2u^2(y)}$",
        ],
        [
            r"$\large\text{Quociente}$",
            r"$\large z = \dfrac{x}{y}$",
            r"$\large |u_c\left(\frac{x}{y}\right)| = \sqrt{\left(\dfrac{1}{y}\right)^2u^2(x)+\left(-\dfrac{x}{y^2}\right)^2u^2(y)}$",
        ],
        [
            r"$\large\text{Potência}$",
            r"$\large z = x^n$",
            r"$\large |u_c(x^n)| = \sqrt{(n x^{n-1})^2u^2(x)} = |n x^{n-1}u(x)|$",
        ],
    ]

    st.table(
        {
            r"$\large\text{Operação}$": [row[0] for row in absolute_data],
            r"$\large\text{Grandeza Resultante } (z)$": [
                row[1] for row in absolute_data
            ],
            r"$\large\text{Incerteza-Padrão Combinada } u_c(z)$": [
                row[2] for row in absolute_data
            ],
        }
    )

    st.caption(
        "Expressões analíticas para a incerteza-padrão combinada com grandezas não correlacionadas."
    )

    st.subheader("2. Propagação da Incerteza Relativa")

    relative_data = [
        [
            r"$\large\text{Soma e Subtração}$",
            r"$\large z = x \pm y$",
            r"$\large \dfrac{u_c(z)}{|z|} = \dfrac{\sqrt{u^2(x)+u^2(y)}}{|x\pm y|}$",
        ],
        [
            r"$\large\text{Produto}$",
            r"$\large z = x \cdot y$",
            r"$\large \dfrac{u_c(z)}{|z|} = \sqrt{\left(\dfrac{u(x)}{x}\right)^2+\left(\dfrac{u(y)}{y}\right)^2}$",
        ],
        [
            r"$\large\text{Quociente}$",
            r"$\large z = \dfrac{x}{y}$",
            r"$\large \dfrac{u_c(z)}{|z|} = \sqrt{\left(\dfrac{u(x)}{x}\right)^2+\left(\dfrac{u(y)}{y}\right)^2}$",
        ],
        [
            r"$\large\text{Potência}$",
            r"$\large z = x^n$",
            r"$\large \dfrac{u_c(z)}{|z|} = |n|\dfrac{u(x)}{|x|}$",
        ],
    ]

    st.table(
        {
            r"$\large\text{Operação}$": [row[0] for row in relative_data],
            r"$\large\text{Grandeza Resultante } (z)$": [row[1] for row in relative_data],
            r"$\large\text{Incerteza Relativa } \left(\dfrac{u_c(z)}{|z|}\right)$": [
                row[2] for row in relative_data
            ],
        }
    )

    st.caption(
        "Expressões analíticas para a incerteza relativa em grandezas não correlacionadas."
    )

    st.header("Exemplo Didático")

    st.markdown(
        r"""
    Determinar a massa volúmica (densidade) $\rho$ de um cilindro maciço a partir
    da medição (assumidas não correlacionadas) da sua massa $m$, diâmetro $d$ e comprimento $l$.
    """
    )

    st.markdown("")
    st.markdown("#### Dados do ensaio:")

    c_massa, sep1, c_diam, sep2, c_comp = st.columns([1, 0.05, 1, 0.05, 1])

    with c_massa:
        st.markdown("**Massa:**")
        st.latex(r"\large m=(185{,}40\pm0{,}05)\,\mathrm{g}")
        st.latex(r"\large u(m)=0{,}05\,\mathrm{g}")

    with sep1:
        st.markdown(
            """
            <div style="
                border-left: 1.5px solid rgba(255, 255, 255, 0.2);
                height: 150px;
                margin: auto;
            "></div>
            """,
            unsafe_allow_html=True,
        )

    with c_diam:
        st.markdown("**Diâmetro:**")
        st.latex(r"\large d=(20{,}00\pm0{,}02)\,\mathrm{mm}")
        st.latex(r"\large u(d)=0{,}02\,\mathrm{mm}")

    with sep2:
        st.markdown(
            """
            <div style="
                border-left: 1.5px solid rgba(255, 255, 255, 0.2);
                height: 150px;
                margin: auto;
            "></div>
            """,
            unsafe_allow_html=True,
        )

    with c_comp:
        st.markdown("**Comprimento:**")
        st.latex(r"\large l=(40{,}00\pm0{,}05)\,\mathrm{mm}")
        st.latex(r"\large u(l)=0{,}05\,\mathrm{mm}")
        
    st.markdown("")
    st.markdown("")
    st.markdown("")
    
    st.markdown(r"""
    O volume do cilindro é $V=\dfrac{\pi d^2 l}{4}$. A densidade obtém-se por:
    """
    )

    st.latex(
        r"""
        \large
        \rho
        =\frac{m}{V}
        =\frac{4m}{\pi d^2l}
        """
    )

    st.markdown(r"**1. Cálculo do valor de $\rho$:**")

    st.markdown(
        r"""
    Convertendo as dimensões para centímetros
    ($d=2{,}000\,\mathrm{cm}$ e $l=4{,}000\,\mathrm{cm}$):
    """
    )

    st.latex(
        r"""
        \large
        \rho=
        \frac{4\times185{,}40}
        {\pi\times(2{,}000)^2\times4{,}000}
        =
        \frac{741{,}60}{50{,}2655}
        \approx14{,}7538\,\mathrm{g/cm^3}
        """
    )

    st.markdown(r"**2. Cálculo da Incerteza-Padrão Combinada $u_c(\rho)$:**")

    st.markdown(
        r"""
    A incerteza-padrão combinada pode ser calculada diretamente através da Lei
    de Propagação de Incertezas:
    """
    )

    st.latex(
        r"""
        \large
        u_c(\rho)=
        \sqrt{
        \left(\frac{\partial\rho}{\partial m}u(m)\right)^2+
        \left(\frac{\partial\rho}{\partial d}u(d)\right)^2+
        \left(\frac{\partial\rho}{\partial l}u(l)\right)^2
        }
        """
    )

    st.markdown(r"""
        Para $\normalsize{\rho=\frac{4m}{\pi d^2l}}$ as derivadas parciais são:
        """)

    st.latex(
        r"""
        \large
        \frac{\partial\rho}{\partial m}
        =\frac{4}{\pi d^2l}
        =\frac{\rho}{m},
        \qquad
        \frac{\partial\rho}{\partial d}
        =-\frac{4m}{\pi d^3l}
        =-\frac{2\rho}{d},
        \qquad
        \frac{\partial\rho}{\partial l}
        =-\frac{4m}{\pi d^2l^2}
        =-\frac{\rho}{l}
        """
    )

    st.markdown("Assim temos:")

    st.latex(
        r"""
        \large
        u_c(\rho)=
        \rho\sqrt{
        \left(\frac{u(m)}{m}\right)^2+
        4\left(\frac{u(d)}{d}\right)^2+
        \left(\frac{u(l)}{l}\right)^2
        }
        """
    )

    st.markdown("Substituindo pelos valores:")

    st.latex(
        r"""
        \large
        u_c(\rho)=
        14{,}7538
        \sqrt{
        \left(\frac{0{,}05}{185{,}40}\right)^2+
        4\left(\frac{0{,}02}{20{,}00}\right)^2+
        \left(\frac{0{,}05}{40{,}00}\right)^2
        }
        """
    )

    st.markdown("Logo a incerteza-padrão combinada será:")

    st.latex(
        r"""
        \large
        \boxed{
        u_c(\rho)\approx0{,}0350\,\mathrm{g/cm^3}
        }
        """
    )

    st.markdown(r"**3. Cálculo da Incerteza Relativa:**")

    st.markdown(
        r"""
    Caso se pretenda expressar a incerteza relativa, divide-se a
    incerteza-padrão combinada pelo valor central de $\rho$:
    """
    )

    st.latex(
        r"""
        \large
        \frac{u_c(\rho)}{\rho}
        =
        \sqrt{
        \left(\frac{u(m)}{m}\right)^2+
        4\left(\frac{u(d)}{d}\right)^2+
        \left(\frac{u(l)}{l}\right)^2
        }
        """
    )

    st.markdown("Logo:")

    st.latex(
        r"""
        \large
        \frac{u_c(\rho)}{\rho}
        =
        \sqrt{
        \left(\frac{0{,}05}{185{,}40}\right)^2+
        4\left(\frac{0{,}02}{20{,}00}\right)^2+
        \left(\frac{0{,}05}{40{,}00}\right)^2
        }
        """
    )

    st.markdown("Ou de outra forma:")

    st.latex(
        r"""
        \large
        \frac{u_c(\rho)}{\rho}
        =
        \sqrt{
        (0{,}0002697)^2+
        4(0{,}001000)^2+
        (0{,}001250)^2
        }
        """
    )

    st.latex(
        r"""
        \large
        \boxed{
        \frac{u_c(\rho)}{\rho}
        =\frac{0{,}0350}{14{,}7538}
        \approx0{,}002372

        =0{,}237\%
        }
        """
    )

    st.markdown("**4. Contribuição Relativa de cada Grandeza:**")

    st.markdown(
        """
        A contribuição de cada grandeza de entrada é obtida dividindo 
        o seu termo quadrático pela variância relativa combinada total (contribuição total):
        """
    )

    st.latex(
        r"""
        \large C_{\mathrm{total}} = \left(\frac{u_c(\rho)}{\rho}\right)^2 \approx 5{,}627666\times10^{-6}
        """
    )

    st.latex(
        r"""
        \large
        \text{Massa } (m)\!: \quad \frac{(0{,}0002697)^2}{C_{\mathrm{total}}}\times 100\% \approx 1{,}3\%
        """
    )

    st.latex(
        r"""
        \large
        \text{Diâmetro } (d)\!: \quad \frac{4(0{,}001000)^2}{C_{\mathrm{total}}}\times 100\% \approx 71{,}0\%
        """
    )

    st.latex(
        r"""
        \large
        \text{Comprimento } (l)\!: \quad \frac{(0{,}001250)^2}{C_{\mathrm{total}}}\times 100\% \approx 27{,}8\%
        """
    )

    st.markdown("Assim, os contributos relativos são:")

    st.markdown(
        """
    - **Massa:** ≈ 1,3%
    - **Diâmetro:** ≈ 71,0%
    - **Comprimento:** ≈ 27,8%
    """
    )

    st.markdown(
        """
    *Conclusão:* O diâmetro apresenta a maior contribuição para a variância combinada da densidade. Portanto, a melhoria da medição do diâmetro
    terá o maior impacto na redução da incerteza.
    """
    )

    st.markdown("**5. Resultado Final:**")

    st.latex(
        r"""
        \large
        \boxed{
        \rho=(14{,}754\pm0{,}035)\,\mathrm{g/cm^3}
        }
        """
    )

st.divider()

st.subheader("References")

st.markdown("""
* **[JCGM 100:2008 (GUM)](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf)** — *Evaluation of measurement data — Guide to the expression of uncertainty in measurement*.
* **[JCGM GUM-6:2020 (GUM)](https://www.bipm.org/documents/20126/2071204/JCGM_GUM_6_2020.pdf/d4e77d99-3870-0908-ff37-c1b6a230a337)** — *Guide to the expression of uncertainty in measurement — Part 6: Developing and using measurement models*.
* **[JCGM 200:2012 (VIM)](https://www.bipm.org/documents/20126/41373499/JCGM_200_2012.pdf/f0e1ad45-d337-bbeb-53a6-15fe649d0ff1)** — *International Vocabulary of Metrology – Basic and general concepts and associated terms*
* **[IPAC (2015)](https://www.ipac.pt/docs/publicdocs/requisitos/OGC010.pdf)** — *Avaliação da Incerteza de Medição em Calibração* (OGC010). Instituto Português de Acreditação.
* **[RELACRE (2024)](https://www.relacre.pt/assets/relacreassets/files/commissionsandpublications/Guia%20RELACRE_Incertezas_Ed2_VF.pdf)** — *Guia RELACRE 25: Estimativa da Incerteza de Medição em Ensaios de Materiais de Construção* (2.ª ed.). Associação de Laboratórios Acreditados de Portugal.
* **[Departamento de Física, FCUL](https://ciencias.ulisboa.pt/)** — Pedagogical material for the courses **Física Experimental I** and **Engenharia da Medida e Padrões**. Faculdade de Ciências da Universidade de Lisboa.
""")

# Footer
st.divider()
col1, col2 = st.columns([10, 1])
with col1:
    st.caption("This tool is for educational purposes. Verify your own calculations!")
with col2:
    st.caption("© 2026 João Canais")