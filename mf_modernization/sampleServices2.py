import os
import markdown2
from xhtml2pdf import pisa

def md_string_to_pdf(md_content: str, output_file: str = "output.pdf", title: str = None):
    """
    Convert Markdown to styled PDF using markdown2 + xhtml2pdf
    """

    # Convert Markdown → HTML
    html_content = markdown2.markdown(md_content, extras=["tables", "fenced-code-blocks"])

    # Wrap with HTML/CSS
    html_template = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Calibri, Helvetica, Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.5;
                margin: 50px;
            }}
            /* ✅ First line (title) centered */
            .doc-title {{
                text-align: center;
                font-size: 20pt;
                font-weight: bold;
                margin-bottom: 20px;
                color: #003366; /* Dark Blue */
            }}
            /* ✅ Heading colors */
            h1 {{ font-size: 18pt; margin: 20px 0 10px 0; color: #003366; }}
            h2 {{ font-size: 16pt; margin: 18px 0 8px 0; color: #006600; }}
            h3 {{ font-size: 14pt; margin: 16px 0 6px 0; color: #993300; }}
            p {{ margin: 6px 0; }}
            ul {{ margin: 6px 0 6px 20px; }}
            li {{ margin: 4px 0; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 12px 0;
            }}
            th, td {{
                border: 1px solid #444;
                padding: 6px 10px;
                text-align: left;
            }}
            th {{
                background: #eee;
            }}
            code {{
                font-family: Consolas, monospace;
                background: #f4f4f4;
                padding: 2px 4px;
                border-radius: 3px;
                white-space: pre-wrap; /* This allows the text to wrap */
                word-break: break-word;
            }}
            pre {{
                background: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
            blockquote {{
                border-left: 4px solid #ccc;
                margin: 10px 0;
                padding-left: 12px;
                color: #555;
                font-style: italic;
            }}
        </style>
    </head>
    <body>
        {f"<div class='doc-title'>{title}</div>" if title else ""}
        {html_content}
    </body>
    </html>
    """
    output_path =f"C:\\Extracted_dir\\MFApplication\\LTCHPPSPricerMFApp2021\\SampleOutputs"
    os.makedirs(output_path, exist_ok=True)
    # Convert HTML → PDF
    output_file_path = output_path+"\\"+output_file
    with open(output_file_path, "wb") as f:
        pisa_status = pisa.CreatePDF(html_template, dest=f)

    if pisa_status.err:
        raise Exception("Error during PDF generation")

    print(f"✅ PDF saved at {output_file_path}")
    return output_file_path


# # Example usage
# if __name__ == "__main__":
#     md_content = """

# """
#     md_string_to_pdf(md_content, "L7_FunctionalSpecification.pdf", title="L7 - Functional Specifications")



