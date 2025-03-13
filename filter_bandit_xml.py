import xml.etree.ElementTree as ET

INPUT_XML = "bandit-report.xml"
OUTPUT_XML = "bandit-report-filtered.xml"

EXCLUDED_PREFIXES = ["./venv"]  # Qualsiasi file che inizia con ./venv verrà escluso

def is_excluded(filename):
    return any(filename.startswith(prefix) for prefix in EXCLUDED_PREFIXES)

def filter_bandit_xml(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Crea un nuovo root con gli stessi attributi
    new_root = ET.Element(root.tag, root.attrib)

    # Copia tutti i figli di root, tranne "results" che tratteremo dopo
    for child in root:
        if child.tag != "results":
            new_root.append(child)

    # Trova la sezione results
    results = root.find('results')
    if results is not None:
        new_results = ET.SubElement(new_root, 'results')

        # Filtra ogni issue
        for issue in results.findall('issue'):
            filename_element = issue.find('filename')
            if filename_element is not None:
                filename = filename_element.text
                if not is_excluded(filename):
                    new_results.append(issue)

    # Salva il nuovo albero XML filtrato
    tree = ET.ElementTree(new_root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"✅ Report filtrato salvato in {output_file}")

if __name__ == "__main__":
    filter_bandit_xml(INPUT_XML, OUTPUT_XML)
