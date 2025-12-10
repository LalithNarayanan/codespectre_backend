import yaml

def yaml_to_markdown(yaml_string, include_code=True):
    programs = yaml.safe_load(yaml_string)
    if not isinstance(programs, list):
        programs = [programs]
    md = []
    for prog in programs:
        md.append(f"## Program: {prog.get('ProgramName', '')}\n")
        md.append(f"**Overview:** {prog.get('Overview', '').strip()}\n")

        paragraphs = prog.get('Paragraphs', [])
        if paragraphs:
            md.append("### Paragraphs Execution Order and Descriptions:\n")
            for para in paragraphs:
                md.append(f"#### {para.get('Name', '')}\n")
                md.append(f"**Description:** {para.get('Description', '').strip()}")
                
                calls = para.get('Calls', '')
                if calls:
                    # Handles both string and list
                    if isinstance(calls, list):
                        md.append(f"**Calls:** {'; '.join(str(c) for c in calls)}")
                    else:
                        md.append(f"**Calls:** {calls}")

                # Code snippet
                if include_code and para.get('CodeSnippet'):
                    md.append("**Code Snippet:**")
                    md.append(f"``````")
                md.append("")  # Add line break between paragraphs

        # Business Rules section
        brs = prog.get('BusinessRules', [])
        if brs:
            md.append("### Business Rules:")
            for rule in brs:
                md.append(f"- {rule}")

        # Data Validation
        dv = prog.get('DataValidation', [])
        if dv:
            md.append("\n### Data Validation and Error Handling:")
            for val in dv:
                md.append(f"- {val}")

        # Error Handling
        eh = prog.get('ErrorHandling', [])
        if eh:
            md.append("\n### Error Handling:")
            for err in eh:
                md.append(f"- {err}")

        md.append("\n---\n")  # Separator between programs

    return '\n'.join(md)
