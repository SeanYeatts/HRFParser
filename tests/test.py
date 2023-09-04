
# 3rd Party Imports
from quickpathstr import Filepath

# Project Imports
from hrfparser import HRFParser

# INPUTS
SOURCE = Filepath(fr"resources\user_config.yaml")

# OUTPUTS
TEST_YAML   = Filepath(fr"tests\test.yaml")
TEST_JSON   = Filepath(fr"tests\test.json")

# QUICK PARAMETER CONTROLS
formatted:      bool        = True
source:         Filepath    = SOURCE
destination:    Filepath    = TEST_YAML
show_result:    bool        = True

# TESTS
parser = HRFParser()
data = None

# TEST CASE : FORMATTED
if formatted:
    data = parser.unpack(source)

    if show_result:
        print('FORMATTED')
        for key in data:
            print(f"{key} : {data[key]}")
        print('')

    parser.pack(data, destination)

# TEST CASE : UNFORMATTED
else:
    data = parser.read(source)
    # data = parser.flatten(data)

    if show_result:
        print('UNFORMATTED')
        for key in data:
            print(f"{key} : {data[key]}")
        print('')

    # data = parser.fold(data)
    parser.write(data, destination)

# TEST : querying
def query_dict(query: tuple, data: dict):

    # Search for matching key
    result = None
    for key in data.keys():
        if key == query:
            result = data[key]

    # Handle result
    if result:
        print(f"Query '{query}' yielded: {result}")
    else:
        print(f"Query '{query}' yielded: None")
    return result

query = ('VIDEO', 'DISPLAY_MODE', 'constraints')
query_dict(query, data)
