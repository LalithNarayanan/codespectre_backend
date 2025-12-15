import os
from pathlib import Path
import markdown2
from xhtml2pdf import pisa
from loguru import logger


def md_string_to_pdf(md_content: str, output_file: str = "output.pdf", title: str = None, output_dir: str = None):
    """
    Convert Markdown to styled PDF using markdown2 + xhtml2pdf
    
    Args:
        md_content: Markdown content as string
        output_file: PDF filename (e.g., "L10_FunctionalSpecification.pdf")
        title: Document title to display at top
        output_dir: Directory to save PDF. If None, uses default
    
    Returns:
        Full path to generated PDF file
    """
    # ✅ FIX #1: Use output_dir if provided, otherwise use default
    if output_dir is None:
        # Fallback to default if not provided
        try:
            from config import load_config
            config = load_config()
            output_dir = Path(config['source_path']['base_dir_default']) / "output" / "pdfs"
        except:
            output_dir = Path(".") / "output" / "pdfs"
    else:
        output_dir = Path(output_dir)
    
    # ✅ FIX #2: Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # ✅ FIX #3: Full PDF file path using the specified output_dir
    pdf_path = output_dir / output_file
    
    logger.info(f"[PDF] Converting markdown to PDF: {pdf_path}")
    
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
    
    # ✅ FIX #4: Use the specified output_dir instead of hardcoded path
    try:
        with open(str(pdf_path), "wb") as f:
            pisa_status = pisa.CreatePDF(html_template, dest=f)

        if pisa_status.err:
            logger.error(f"[PDF] Error during PDF generation: {pisa_status.err}")
            raise Exception("Error during PDF generation")

        logger.info(f"✅ [PDF] PDF saved successfully at: {pdf_path}")
        return str(pdf_path)
    
    except Exception as e:
        logger.error(f"❌ [PDF] Failed to generate PDF at {pdf_path}: {e}")
        raise


# # Example usage
# if __name__ == "__main__":
#     md_content = """
#     # Sample Document
#     This is a test document.
#     """
#     md_string_to_pdf(md_content, "L7_FunctionalSpecification.pdf", title="L7 - Functional Specifications", output_dir="./output/sas_specifications/pdfs")