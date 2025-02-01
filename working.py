import os
import yaml



parts = {}
configuration = {}

def get_configuration(**kwargs):
    global configuration
    folder = kwargs.get("folder", f"{os.path.dirname(__file__)}/parts")
    #first try a configuration fodler one up from the parts folder supplied
    folder = folder.replace("\\","/")
    folder = folder.replace("parts","")
    folder_configuration = "configuration"
    folder_configuration = os.path.join(folder, folder_configuration)
    file_configuration = os.path.join(folder_configuration, "oomlout_oomp_utility_file_filter_configuration.yaml")
    if not os.path.exists(file_configuration):    
        #check for configuration in current oomp folder
        folder_configuration = "configuration"
        folder_configuration = os.path.join(os.path.dirname(__file__), folder_configuration)
        file_configuration = os.path.join(folder_configuration, "configuration.yaml")
        #check if exists
        if not os.path.exists(file_configuration):
            print(f"no configuration.yaml found in {folder_configuration} using default")
            file_configuration = os.path.join(folder_configuration, "oomlout_oomp_utility_file_filter_configuration.yaml")



    #import configuration

    with open(file_configuration, 'r') as stream:
        try:
            configuration = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:   
            print(exc)
    kwargs["configuration"] = configuration


def main(**kwargs):
    get_configuration(**kwargs)
    folder = kwargs.get("folder", f"{os.path.dirname(__file__)}/parts")
    folder = folder.replace("\\","/")
    
    kwargs["configuration"] = configuration
    print(f"running utility oomlout_oomp_utility_file_filter: {folder}")
    create_recursive(**kwargs) ## load all parts into parts dictionary
    #all parts loaded now make csv
    print(f"creating csv")
        

def create_recursive(**kwargs):
    folder = kwargs.get("folder", os.path.dirname(__file__))
    kwargs["folder"] = folder
    filter = kwargs.get("filter", "")
    #if folder exists
    if os.path.exists(folder):        
        count = 0
        for item in os.listdir(folder):
            if filter in item:
                directory_absolute = os.path.join(folder, item)
                directory_absolute = directory_absolute.replace("\\","/")
                if os.path.isdir(directory_absolute):
                    #if working.yaml exists in the folder
                    if os.path.exists(os.path.join(directory_absolute, "working.yaml")):
                        kwargs["directory_absolute"] = directory_absolute
                        create(**kwargs)
                        count += 1
                        if count % 100 == 0:
                            break
                            print(f"    {count} parts loaded")
    else:
        print(f"no folder found at {folder}")

def create(**kwargs):
    directory_absolute = kwargs.get("directory_absolute", os.getcwd())    
    kwargs["directory_absolute"] = directory_absolute    
    generate(**kwargs)
    

def generate(**kwargs):    
    directory_absolute = kwargs.get("directory_absolute")
    configuration = kwargs.get("configuration")
    file_keep_list = configuration.get("file_keep_list", [])
    file_list_current_directory = os.listdir(directory_absolute)
    for file in file_list_current_directory:
        if file not in file_keep_list:
            file_absolute = os.path.join(directory_absolute, file)
            if os.path.isfile(file_absolute):
                os.remove(file_absolute)
                print(f"removed {file_absolute}")

if __name__ == '__main__':
    #folder is the path it was launched from
    
    kwargs = {}
    folder = os.path.dirname(__file__)
    #folder = "C:/gh/oomlout_oomp_builder/parts"
    folder = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
    #folder = "C:/gh/oomlout_oobb_version_4/things"
    #folder = "C:/gh/oomlout_oomp_current_version"
    kwargs["folder"] = folder
    overwrite = False
    kwargs["overwrite"] = overwrite
    main(**kwargs)