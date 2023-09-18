# Find and delete empty series

These scripts can be used to

1. find series that don't have events (`find-empy-series`), and
2. use that output to delete those series (`delete-empty-series`).

The affected series ids will be written into a text file.

To use, first update `config.py` for your installation.

**Use the second script with caution since it will delete data that cannot be
recovered!**

## Requirements

This scrypt was written for Python 3.11. You can install the necessary packages with

```
pip install -r requirements.txt
```

Additionally, this script uses modules contained in the _lib_ directory.