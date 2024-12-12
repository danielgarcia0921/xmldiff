import os, re, shutil

NEW_STRINGS_FOLDER = f"{os.getcwd()}/strings/new"

OLD_FILENAME = "strings.xml"
def getFilename(string):
    new_string = "strings"
    if string != "values-fr-rCA":
        new_string = re.search(r"-\w{2}\b",string).group()
        new_string = new_string[1:3]
    else:
        new_string = "fr-CA"
    return f"{new_string}.xml"

def convert_to_file():
    os.chdir(NEW_STRINGS_FOLDER)
    for folder in os.listdir():
        if (folder != ".DS_Store" and ".xml" not in folder):
            os.chdir(folder)
            #print(os.getcwd())
            new_filename = getFilename(folder)
            try:
                os.rename(OLD_FILENAME, new_filename)
            except FileNotFoundError:
                print(f"strings.xml not found in {folder}...")
            shutil.copy(new_filename,NEW_STRINGS_FOLDER)
            os.chdir("..")
        
        

convert_to_file()