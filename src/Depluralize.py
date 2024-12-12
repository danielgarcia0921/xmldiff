import json, os
import xml.etree.ElementTree as ET
from xml.dom import minidom

NEW_STRINGS_FOLDER = f"{os.getcwd()}/strings/new"

def get_languages():
    lang_data = ""
    with open("src/languages.json", mode="r", encoding="utf-8") as lang_json:
        lang_data = json.load(lang_json)
    return lang_data


def get_country_code_list():
    language_list = get_languages()
    country_codes = ""
    country_codes = [list(lang.values())[0] for lang in language_list['languages']]
    return country_codes

def open_file(xml_file):
    os.chdir(NEW_STRINGS_FOLDER)
    xml_contents = ET.parse(xml_file)
    return xml_contents
    
def create_tag(xml_file, item_tag, prefix):
    root = xml_file.getroot()
    new_element = ET.SubElement(root, "String")
    try:
        new_element.set("name", f"{prefix}_{item_tag.attrib["quantity"]}")
    except KeyError:
        try:
            new_element.set("name", f"{item_tag.attrib["name"]}")
        except KeyError:
            print("Element has not name or quantity attribute, skipping...")

    new_element.text = str(item_tag.text)
    
    b_xml = ET.tostring(root).decode("utf-8")
    reparsed = minidom.parseString(b_xml)
    pretty_xml = reparsed.toprettyxml(indent="    ")
    pretty_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip()])
    return pretty_xml

def write_to_file(tag, lang):
    os.chdir("../../output")
    with open(f"{lang}.xml", "w", encoding='utf-8') as f:
        f.write(tag)
    os.chdir("..")


def depluralize(xml_contents, language):
    #Create tags for each plural item
    for plural in xml_contents.findall("plurals"):
         plural_items = plural.findall("item")
         for item_tag in plural_items:
             os.chdir(NEW_STRINGS_FOLDER)
             new_tag = create_tag(xml_contents, item_tag, plural.attrib["name"])
             write_to_file(new_tag, language)

    #Create tags for each string array item
    for string_array in xml_contents.findall("string-array"):
         string_array_items = string_array.findall("item")
         for item_tag in string_array_items:
             os.chdir(NEW_STRINGS_FOLDER)
             new_tag = create_tag(xml_contents, item_tag, "")
             write_to_file(new_tag, language)

def delete_tags(lang):
    os.chdir("./output")
    tree = ET.parse(f"{lang}.xml")
    root = tree.getroot()
    for plurals in root.findall(".//plurals"):
        root.remove(plurals)
    for arrays in root.findall(".//string-array"):
        root.remove(arrays)
    os.chdir("..")
    return ET.tostring(root, "unicode")
    


if __name__ == "__main__":
    list = get_country_code_list()
    for language in list:
        current_xml = open_file(f"{language}.xml")
        depluralize(current_xml, language)
        file_clean = delete_tags(language)
        os.chdir(NEW_STRINGS_FOLDER)
        write_to_file(file_clean, language)
    
