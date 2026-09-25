"""Module with all Streamlit application styles and page setup (loads the css file)."""

from pathlib import Path

import streamlit.components.v1 as components
import streamlit as st
import base64
import json


def _load_stylesheet():
    """Loads the shared stylesheet used by the Streamlit page and iframes."""

    stylesheet_file = Path(__file__).with_name("styles.css")
    return stylesheet_file.read_text(encoding="utf-8")


def apply_page_config():
    """Applies basic page configuration, logo, and layout tweaks."""
    
    # Set page logo from the project-level media folder.
    logo_file = Path(__file__).resolve().parents[1] / "media" / "logo.svg"
    
    if logo_file.is_file():
        svg_bytes = logo_file.read_bytes()
        svg_b64 = base64.b64encode(svg_bytes).decode("utf-8")
        icon = f"data:image/svg+xml;base64,{svg_b64}"
    else:
        icon = "📏"
        
    st.set_page_config(
        page_title="Uncertainty Calculator",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Logo display in the sidebar
    if logo_file.is_file() and hasattr(st, "logo"):
        st.logo(f"data:image/svg+xml;base64,{svg_b64}", size="large")

    # Hide Streamlit's default menu and footer, and adjust padding
    st.markdown(
        f"<style>{_load_stylesheet()}</style>",
        unsafe_allow_html=True,
    )


def github_link(
    repo_url="https://github.com/joao-canais/Propagation-of-Uncertainty-Calculator.git",
    label="GitHub Repository",
):
    """Renders GitHub badge with SVG icon in the sidebar."""
    st.sidebar.markdown(
        f"""
        <a href="{repo_url}" target="_blank" class="github-link">
            <svg height="18" width="18" viewBox="0 0 16 16">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
            </svg>
            <span>{label}</span>
        </a>
        """,
        unsafe_allow_html=True,
    )


def disable_streamlit_scrollbar():
    """Disables the default Streamlit scrollbar ONLY for the Theory page."""
    st.markdown(
        """
        <style>
        [data-testid="stLatex"],
        [data-testid="stLatex"] > div {
            overflow-x: visible !important;
            overflow-y: visible !important;
        }

        .katex-display,
        .katex-display > .katex,
        .katex-display .katex-html {
            overflow-x: visible !important;
            overflow-y: visible !important;
            padding: 4px 0 !important; /* margem de segurança para a borda do \boxed */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def copy_excel_button(
    text, 
    caption="Copy Excel Formula to clipboard", 
    height=80
):
    """Renders a button that copies the provided Excel formula text to the clipboard."""
    
    safe_text = json.dumps(text)

    copy_button_html = f"""
    <style>{_load_stylesheet()}</style>
    <html>
    <body class="copy-excel-frame">
    <div style="display: inline-block;">
        <button id="copy-btn" onclick="copyToClipboard()">{caption}</button>
    </div>

    <script>
    const btn = document.getElementById("copy-btn");

    function copyToClipboard() {{
        const text = {safe_text};
        navigator.clipboard.writeText(text).then(() => {{
            btn.classList.add("copied");

            setTimeout(() => {{
                btn.classList.remove("copied");
            }}, 350);

        }}).catch(err => {{
            console.error("Erro ao copiar:", err);
        }});
    }}
    </script>
        </body>
        </html>
    """
    
    st.iframe(copy_button_html, height=height)

 
def clickable_latex(latex_str, font_size=1.95, height=120, help="Copy LaTeX code to clipboard"):
    """
    Renders a LaTeX expression and allows copying the full code on click. 
    Falls back to displaying the LaTeX code if an error occurs.
    """
    
    try:
        raw_code = latex_str.strip()                  # Latex code to display
        copy_latex_code = rf"\[{latex_str}\]".strip() # Latex code to copy

        # Just to make sure the help text is safe for HTML attributes
        safe_help = help.replace('"', '&quot;')
        
        # HTML and JavaScript for the clickable LaTeX
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
            <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
            <style>{_load_stylesheet()}</style>
            <style>
                .latex-frame .katex {{
                    font-size: {font_size}rem;
                    line-height: 1.3;
                }}
            </style>
        </head>
        <body class="latex-frame">
            <div id="math-container" title="{safe_help}">
                <span id="math-target"></span>
            </div>

            <script>
                const latex = {json.dumps(raw_code)};
                const copy_latex = {json.dumps(copy_latex_code)};
                const target = document.getElementById('math-target');
                const container = document.getElementById('math-container');

                katex.render(latex, target, {{
                    throwOnError: false,
                    displayMode: true
                }});

                container.addEventListener('click', async () => {{
                    try {{
                        await navigator.clipboard.writeText(copy_latex);
                        const originalColor = container.style.color;
                        container.style.color = '#dadde0a6';
                        setTimeout(() => {{
                            container.style.color = originalColor;
                        }}, 350);
                    }} catch (err) {{
                        console.error('Falha ao copiar:', err);
                    }}
                }});
            </script>
        </body>
        </html>
        """
        components.html(html_code, height=height, scrolling=True)
        return True
        
    except Exception as e:
        st.latex(rf"\[{latex_str}\]")  # Fallback to just displaying the LaTeX code
        return False
