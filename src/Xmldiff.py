import json, os, sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom

ROOT_FOLDER = sys.path[0].strip("/src")
OUTPUT_FOLDER = Path(f"/output/diffOutput")
OLD_FILE = Path(f"/strings/old")
NEW_FILE = Path(f"/output")

def open_file(xml_file):
    xml_contents = ET.parse(xml_file)
    return xml_contents

def get_languages():
    lang_data = ""
    with open("languages.json", mode="r", encoding="utf-8") as lang_json:
        lang_data = json.load(lang_json)
    return lang_data

def get_country_code_list():
    language_list = get_languages()
    country_codes = ""
    country_codes = [list(lang.values())[0] for lang in language_list['languages']]
    return country_codes


def append_tags(old_contents, new_contents):
    old_dict = {}
    new_dict = {}
    for tag in old_contents:
        try:
            old_dict[tag.attrib["name"]] = tag.text
        except KeyError:
            pass
    for tag in new_contents:
        try:
            new_dict[tag.attrib["name"]] = tag.text
        except KeyError:
            pass
    
    for tag in new_dict:
        if tag in old_dict:
            #Check if content is the same
            try:
                old_dict[tag] = new_dict[tag]
            except AttributeError:
                pass
        else:
            #Tag in the new file is NOT on old file, so should be appended
            try:
                old_dict[tag.attrib["name"]] = tag.text
            except AttributeError:
                pass
    #return a transformed old_dict
    return old_dict



def compare_files(language):
    os.chdir("./strings/old")
    old_root = open_file(f"{language}.xml").getroot()
    os.chdir("../..")
    os.chdir("./output")
    new_root = open_file(f"{language}.xml").getroot()
    os.chdir("..")
    result = append_tags(old_root, new_root)
    return result

def write_file(language, content_dict):
    os.chdir("./output/diffOutput")
    root = ""
    root = ET.Element("resources")
    for tag in content_dict:
        ET.SubElement(root, "string", name=f"{tag}").text = content_dict[tag]

    xml_str = ET.tostring(root, encoding="unicode")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="    ")

    with open(f"{language}.xml", "w", encoding="utf-8") as f:
        f.write(pretty_xml)


    
if __name__ == "__main__":
    os.chdir("./src")
    list = get_country_code_list()
    os.chdir("..")
    for language in list:
        transformed_file = compare_files(language)
        write_file(language, transformed_file)
        os.chdir("../..")
    