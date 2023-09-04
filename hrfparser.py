"""
HRFParser
=========

Copyright (c) 2023 Sean Yeatts. All rights reserved.

A convenience pipeline for working with Human-Readable Formats ( HRFs ) such
as YAML and JSON. It's designed to easily read / write data between HRFs and
Python dictionaries, both in raw and flattened ( single key-value pairs )
formats.

Features:
    - Auto-conversion between different HRF formats based on file extensions.
    - 'Unpacking' of nested data to flattened, single key-value pairs.

Current supported HRFs:
    - YAML
    - JSON
"""

# 3rd Party Imports
import yaml                         # yaml
import json                         # json

from quickpathstr import Filepath   # file syntax reducer


# CLASSES
class FlowStyle(yaml.SafeDumper):
    '''
    Custom formatting of lists ( sequences ) to enforce inline representation.
    '''
    def represent_sequence(self, tag, sequence, flow_style=None):
        # Force flow style for lists (sequences)
        return super(FlowStyle, self).represent_sequence(tag, sequence, flow_style=True)


class HRFParser:
    '''
    HRFParser
    ---------
    Reads, writes, and formats data from common Human Readable Formats
    ( HRFs ), such as YAML and JSON.

    Methods:
        - read() : read raw HRF from file
        - write() : write raw HRF to destination
        - unpack() : read and flatten HRF data from file
        - pack() : fold HRF data and write to destination
        - flatten() : deconstruct nested data as single key-value pairs
        - fold() : rebuild data as nested key-value pairs
    '''

    # FUNDAMENTAL METHODS
    def __init__(self):
        # Let PyYAML know about our custom formatter
        yaml.add_representer(list, FlowStyle.represent_list, Dumper=FlowStyle)

    # FORMATTED METHODS : deconstruct / rebuild policy
    def unpack(self, file: Filepath) -> dict:
        '''
        Reads HRF and flattens into single key-value pairs.

        Params:
            - file ( Filepath ) : source file
        '''
        data = self.read(file)
        return self.flatten(data)
    
    def pack(self, data: dict, file: Filepath):
        '''
        Rebuilds single key-value pairs and writes to HRF.
        
        Params:
            - data ( dict ) : dictionary
            - file ( Filepath ) : destination file
        '''
        data = self.fold(data)
        self.write(data, file)

    # UNFORMATTED METHODS : use 'as-is' policy
    def read(self, file: Filepath) -> dict:
        '''
        Reads HRF into Python dictionary.
                        
        Params:
            - file ( Filepath ) : source file
        '''

        # Access source file
        try:
            source = open(file.complete, 'r')
        except Exception as error:
            print(f"File access issue: {str(error)}")
        
        # Select appropriate read method based on file extension
        match file.extension:
            case '.yaml':
                return yaml.safe_load(source)
            case '.json':
                return json.load(source)
            case _:
                raise KeyError(f"File extension '{file.extension}' not supported!")
    
    def write(self, data: dict, file: Filepath):
        '''
        Writes Python dictionary to HRF.
                
        Params:
            - data ( dict ) : dictionary
            - file ( Filepath ) : destination file
        '''
        
        # Access destination file
        try:
            destination = open(file.complete, 'w')
        except Exception as error:
            print(f"File access issue: {str(error)}")
        
        # Select appropriate write method
        match file.extension:
            case '.yaml':
                # Not safedump(), but uses a safedump-derived dumper
                yaml.dump(data, destination, sort_keys=False, Dumper=FlowStyle)
            case '.json':
                json.dump(data, destination, sort_keys=False, indent=2)
            case _:
                raise KeyError(f"File extension '{file.extension}' not supported!")

    # FORMATTING TOOLS
    def flatten(self, data: dict) -> dict:
        '''
        Flattens nested dicts into single key-value pairs.
        
        Params:
            - data ( dict ) : nested dictionary

        Returns:
            - ( dict ) : flattened dictionary ( keys are tuples )
        '''
        result = {}

        # Recursive traversal of nested structures
        def traverse(source, old_key=[]):

            # Iterate on each key-value pair
            for key, value in source.items():   # for each item
                new_key = old_key + [key]       # update current key path

                # Check the nature of the value
                if isinstance(value, dict):             # if we're still seeing a dictionary...
                    nesting = traverse(value, new_key)  # go one deeper
                    result.update(nesting)              # when we get back out, overwrite entry
                else:
                    result[tuple(new_key)] = value      # ...otherwise create entry
            return result
        return traverse(data)

    def fold(self, data: dict) -> dict:
        '''
        Rebuilds a nested dict from single key-value pairs.
                
        Params:
            - data ( dict ) : flat dictionary

        Returns:
            - ( dict ) : folded dictionary ( keys are tuples )
        '''
        result = {}
        
        def set_value(d, keys, value):
            if isinstance(keys, tuple):
                for key in keys[:-1]:  # all keys except the last one
                    d = d.setdefault(key, {})
                d[keys[-1]] = value
            else:
                d[keys] = value

        for keys, value in data.items():
            if isinstance(value, dict):
                nested_dict = self.fold(value)
                set_value(result, keys, nested_dict)
            else:
                set_value(result, keys, value)

        return result

