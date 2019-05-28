# Introduction
This document describes how to perform tests of a python package of arcpy 
scripts.

# Package structure
Mussel-Modeling-Toolbox/
|   MusselModeling.tbx
|   __init__.py
|   setup.py
|   MCAT_Site_score.R
|   ...
*-- tests/
    |   __init__.py
    |   fg_tests_utils.py
    |   ...
    *------ data/
                data.gdb

# Developing test code
* Test scripts are stored in the Mussel-Modeling-Toolbox/tests/ folder.
* For each srcipt in the MusselModeling package there is a matching script in the /tests folder named for the script prepended with test_.
* Develop test code in ArcMap interactive python window:
    >>> sys.path.insert(0, "Z:\Work\Office\Regional\ERDC\EMRRP_Sediment\Methods\FluvialGeomorph")
    >>> from _06_StreamProfilePoints import StreamProfilePoints


# Configure test environment
* Determine python distrubution: `C:\Python27\ArcGIS10.4`
* Determine if pip is installed: `C:\Python27\ArcGIS10.4\Scripts\pip`
* install pytest using pip: `C:\Python27\ArcGIS10.4\Scripts\pip install -U pytest`
* pytest documentation: `https://docs.pytest.org`

# Running test code
* cd to Mussel-Modeling_Toolbox package folder
* run pytest: `C:\Python27\ArcGIS10.4\Scripts\pytest`