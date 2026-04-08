def setup_notebook(width="1100px", figure_format="svg"):
    from IPython.display import HTML, display
    display(HTML(f"""
    <style>
    .jp-Notebook {{
        max-width: {width};
        margin-left: auto !important;
        margin-right: auto !important;
    }}
    .jp-OutputArea-child {{
        overflow-x: auto !important;
    }}
    .jp-RenderedHTMLCommon table {{
        display: block;
        overflow-x: auto;
    }}
    </style>
    """)) # Centered JupyterLab notebook + SVG inline figures.
    get_ipython().run_line_magic("config", f'InlineBackend.figure_format = "{figure_format}"')
