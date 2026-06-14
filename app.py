from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import re

app = Flask(__name__)

def normalize(text):
    if not text:
        return ""
    text = text.strip()
    # Remove non-alphanumeric characters from beginning/end
    text = re.sub(r'^[^\w]+|[^\w]+$', '', text)
    return text

def analyze_xmls(pavast_file, fs_file):
    # ==========================
    # PAVAST XML
    # ==========================
    tree = ET.parse(pavast_file)
    root = tree.getroot()

    variables, parameters, system_constants, messages = set(), set(), set(), set()

    for elem in root.findall(".//SW-VARIABLE"):
        short_name = elem.find("SHORT-NAME")
        if short_name is None or not short_name.text: continue
        name = normalize(short_name.text)
        impl_policy = elem.find(".//SW-IMPL-POLICY")
        if impl_policy is not None and impl_policy.text == "MESSAGE":
            messages.add(name)
        else:
            variables.add(name)

    for elem in root.findall(".//SW-CALPRM"):
        short_name = elem.find("SHORT-NAME")
        if short_name is not None and short_name.text:
            parameters.add(normalize(short_name.text))

    for elem in root.findall(".//SW-SYSTEMCONST"):
        short_name = elem.find("SHORT-NAME")
        if short_name is not None and short_name.text:
            system_constants.add(normalize(short_name.text))

    # ==========================
    # Second XML (FS)
    # ==========================
    tree2 = ET.parse(fs_file)
    root2 = tree2.getroot()

    missing_from_pavast = set()
    fs_names = set()
    incorrect_tags = []

    for tt in root2.findall(".//TT"):
        tt_type = tt.get("TYPE")
        if tt.text is None: continue
        name = normalize(tt.text)
        fs_names.add(name)

        if name in variables:
            if tt_type != "SW-VARIABLE":
                incorrect_tags.append(f"{name}: Expected SW-VARIABLE, Found {tt_type}")
        elif name in parameters:
            if tt_type != "SW-CALPRM":
                incorrect_tags.append(f"{name}: Expected SW-CALPRM, Found {tt_type}")
        elif name in system_constants:
            if tt_type != "SW-SYSTEMCONST":
                incorrect_tags.append(f"{name}: Expected SW-SYSTEMCONST, Found {tt_type}")
        elif name in messages:
            if tt_type != "SW-VARIABLE":
                incorrect_tags.append(f"{name}: Expected MESSAGE, Found {tt_type}")
        else:
            if tt_type != "OTHER":
                missing_from_pavast.add(name)

    # ==========================
    # Calculate Missing & Return
    # ==========================
    all_pavast_items = variables | parameters | system_constants | messages
    missing_from_fs = all_pavast_items - fs_names

    return {
        "missing_from_pavast": sorted(list(missing_from_pavast)),
        "missing_from_fs": sorted(list(missing_from_fs)),
        "incorrect_tags": sorted(incorrect_tags)
    }

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        # Get files from the web form
        pavast_file = request.files.get("pavast_xml")
        fs_file = request.files.get("fs_xml")
        
        if pavast_file and fs_file:
            # Process the files in memory
            results = analyze_xmls(pavast_file.stream, fs_file.stream)
            
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)