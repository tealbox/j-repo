from pathlib import Path

def list_of_conf_files(directory="conf"):
    # Specify the directory path
    _directory = Path(directory)
    patterns = ["dunsw05*", "duncr00*"]
    # Define custom filtering logic
    def matches_any_pattern(file_name):
        return (
            file_name.startswith("duncr00") or
            file_name.endswith(".log") or
            file_name.startswith("dunsw05")
        )
    # List all files in the directory
##    files = [f"{directory}/{item.name}" for item in _directory.iterdir("dunsw050*") if item.is_file()]
    files = [f"{directory}/{item.name}" for item in _directory.iterdir() if item.is_file()]
##    files = [f"{directory}/{item.name}" for item in _directory.glob("*") if item.is_file() and matches_any_pattern(item.name)]

    print("Files in directory:")
    return files
##    for file in files:
##        print(file)

##
##files = list_of_conf_files()
##print(files)
    ##
### Specify the directory path
##directory = Path("/path/to/your/directory")
##
### List all files recursively
##files = [item.relative_to(directory) for item in directory.rglob("*") if item.is_file()]
##
##print("Files in directory (recursive):")
##for file in files:
##    print(file)
##
