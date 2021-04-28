#!/usr/local/bin/python3

import json
import tempfile
import sys
import shutil
import os
from types import FunctionType
from typing import Any, Union

def print_help(error: Union[str, None]):
    if error is not None:
        print(f"Error: {error}\n")

    print(f"""OBS Scene Collection (Un)packer
    Usage:
        {sys.argv[0]} pack <scenes.json file>
            Packs a scene collection JSON file into a single ZIP file containing all assets 
            and the scene JSON file updated to have partial paths, ready for unpacking. 
            
        {sys.argv[0]} unpack <packed zip file>
            Unpacks a scene collection ZIP file into a folder, with the scenes.json file 
            update to have all the paths made absolute ready for importing""")

def process_file(in_file: str, temp_folder: str) -> str:
    """Processes a file path by getting the basename and appending it to [REPLACE] and returning the updated path.
    This also copies the file into the temporary folder provided

    Args:
        in_file (str): the string specified in the scene file which should be copied and renamed
        temp_folder (str): the path to the temporary folder where the files should be copied for packaging

    Returns:
        str: the updated path ready for replacing in the json for packaging
    """
    out_file = os.path.join(temp_folder, os.path.basename(in_file));
    print(f'Made relative: {os.path.basename(in_file)}')
    shutil.copyfile(in_file, out_file)
    return f'[REPLACE]{os.path.basename(in_file)}'

def search_and_execute(entry: Any, action: FunctionType, depth=0):
    # Only process dictionaries
    if type(entry) != dict:
        return

    for key in entry.keys():
        if (key == 'path' or key == 'file' or key == 'local_file') and type(entry[key]) == str:
            action(entry[key], key, entry)
        elif type(entry[key]) == dict:
            search_and_execute(entry[key], action, depth=depth+1)
        elif type(entry[key]) == list:
            for value in entry[key]:
                if type(value) == dict:
                    search_and_execute(value, action, depth=depth+1)

def search_and_restore(entry: Any, absolute: str):
    """Searches through the entire entry structure, recursing down into any dict or array, looking for path, file and local_file keys
    and replaces their content with the file names appended to the end of absolute to form absolute paths for the content. This makes
    the file paths valid again. 

    Args:
        entry (Any): the structure currently being recursed, if it is not a dict it will do nothing
        absolute (str): the absolute paths to where the assets are now stored
    """

    def restore(value, key, e):
        if '[REPLACE]' in value:
            name = value.replace('[REPLACE]', '')
            e[key] = os.path.join(absolute, name)
            print(f'Made absolute: {os.path.basename(name)}')

    search_and_execute(entry, restore)
    
def search_and_copy(entry, temp):
    """Searches through the entire entry structure, recursing down into any dict or array, looking for path, file and local_file keys
    and replaces their content with the file names appended to the end of [REPLACE] copying files to the packaging temp dir

    Args:
        entry (Any): the structure currently being recursed, if it is not a dict it will do nothing
        temp (str): the temporary folder where fils should be copied to be packages
    """

    def replace(value, key, e):
        replacement = process_file(value, temp)
        e[key] = replacement

    search_and_execute(entry, replace)

if len(sys.argv) != 3:
    print_help("Must specify three parameters")
    exit(0)

if sys.argv[1] != 'pack' and sys.argv[1] != 'unpack':
    print_help("Must specify either pack/unpack")
    exit(0)

if sys.argv[1] == 'pack':
    # Make a temporary directory where files should be copied to be packaged
    with tempfile.TemporaryDirectory() as dirpath:
        
        # Load the scenes JSON files and parse it into an object so we can recurse through it and identify keys
        with open(sys.argv[2], 'r') as f:
            scenes = json.loads(f.read())
            
        # search and update the paths to files within it, making them 'relative' and ready to the restored
        search_and_copy(scenes, dirpath)

        # write out the json with the updated dirs
        with open(os.path.join(dirpath, 'scenes.json'), 'w') as f:
            json.dump(scenes, f)
 
        # make the output file match the input file name
        out_file = os.path.splitext(os.path.basename(sys.argv[2]))[0] + '__packaged'

        # zip up the temporary folder including the scenes file which can now be processed by this program in reverse
        shutil.make_archive(out_file, 'zip', dirpath)

        print(f"Zipped and exported as '{out_file}.zip'")
else:
    # Create the output folder which is just the zip file name with __unpack added to it and then unzip the file into it
    output_dir = os.path.basename(sys.argv[2]) + '__unpack'
    shutil.unpack_archive(sys.argv[2], output_dir, 'zip')

    # Load the scenes JSON which will contain the broken relative paths (starting with [REPLACE])
    with open(os.path.join(output_dir, 'scenes.json'), 'r') as f:
        scenes = json.loads(f.read())
        
    # search and update the paths replacing them with the path to the output directory, we make this absolute as this format
    # is used by OBS
    search_and_restore(scenes, os.path.abspath(output_dir))

    print(f'Unzipped and exported to {output_dir}/')

    # write out the json with the updated paths which should be ready to be imported into OBS
    with open(os.path.join(output_dir, 'scenes.json'), 'w') as f:
        json.dump(scenes, f)

    
