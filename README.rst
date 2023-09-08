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
    
Methods:
    - read() : read raw HRF from file
    - write() : write raw HRF to destination
    - unpack() : read and flatten HRF data from file
    - pack() : fold HRF data and write to destination
    - flatten() : deconstruct nested data as single key-value pairs
    - fold() : rebuild data as nested key-value pairs