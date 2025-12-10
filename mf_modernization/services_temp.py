# functiion for Object Oriented Design Document
def oo_design():
    path = "C:/Extracted_dir/MFApplication/LTCHPPSPricerMFApp2021/SampleOutputs"
    file_name = "consolidated_FunctionalSpecification.md"

    with open(f"{path}/{file_name}","r",encoding="utf-8", errors="ignore") as file:
        content = file.read()
        if (content is None) or (content.strip() ==""):
            return "Could not  read the Functional specification file or it is empty."
        else:
            oo_design = design_agent.execute(functional_spec=content)
            oo_design_content = oo_design.content
            md_file_path = Path(path) /"OO_Design_Document.md"
            
            try:
                with open(md_file_path, "w", encoding="utf-8") as f:
                    f.write(oo_design_content)
            except:
                return "Could not generate OO Design Document"

            pdf_file = md_string_to_pdf(oo_design_content, "OO_Design_Document.pdf", title="Object Oriented Design Document")
            return "OO Dsign Document generated successfully!!!"

#oo_design()




def class_diagram():
    path = "C:/Extracted_dir/MFApplication/LTCHPPSPricerMFApp2021/SampleOutputs"
    file_name = "OO_Design_Document.md"

    with open(f"{path}/{file_name}","r",encoding="utf-8", errors="ignore") as file:
        content = file.read()
        if (content is None) or (content.strip() ==""):
            return "Could not read the Design Document file or it is empty."
        else:
            mermaid_digram = mermaid_generator_agent.execute(diagram_type="class_diagram",data_for_diagram=content)
            logger.info(f"mermaid_digram:{mermaid_digram}") # Use your logger
            mermaid_content=mermaid_digram.content


            pattern = r"```mermaid(.*?)```"
            match = re.search(pattern, mermaid_content, re.DOTALL)
            mermaid_code="""
                """
            if match:
                mermaid_code = match.group(1).strip()   
                print(f"mermaid_code",mermaid_code)

            mermaid_content = re.sub(r"^```mermaid\s*\n?", "", mermaid_content, flags=re.IGNORECASE)
            mermaid_content = re.sub(r"\n?\s*```\s*$", "", mermaid_content, flags=re.IGNORECASE)
            mermaid_content = mermaid_content.strip()
            md_file_path = Path(path) /"class_diagram.md"
            try:
                with open(md_file_path, "w", encoding="utf-8") as f:
                    f.write(mermaid_code)
            except:
                return "Could not generate OO Design Document"

            
# class_diagram()