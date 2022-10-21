# Script to convert XML workflows to YAML

With this script, you can convert XML workflows to YAML workflows.\
It does not convert Comments at the moment.

## How to Use
### Usage

The script can be called with the following parameters (all parameters in brackets are optional):

`main.py [-i INPUTFILE] [-o OUTPUTFILE]`

Either input file (`-i`) and output file (`-o`) have to be provided or none.

| Short Option | Long Option | Description                                    |
|:------------:|:------------|:-----------------------------------------------|
|     `-i`     | `--input`   | The xml file to be coonverted (with extension) |
|     `-o`     | `--output`  | The file to output (with extension)            |

#### Usage example

`main.py -i fast.xml -o fast.yaml`

## Requirements

This script was written for Python 3. You can install the necessary packages with

`pip install -r requirements.txt`