"""____________________________________________________________________________
Script Name:          bil2mxe.py
Description:          Converts a folder of rasters in the .bil format to the 
                      Maxent .mxe format. 
Date:                 06/03/2019

Usage:
Converts a folder of rasters in the .bil format that can be read by ESRI into 
the Maxent .mxe format. 

This tool assumes that you have created a new folder preferably named 
`input_bil` that holds all of the .bil rasters to be converted. 

This tool will create a new folder named `input_mxe` in the same root folder 
as the `input_bil` folder you provided in the first parameter. This folder will 
hold the rasters converted from .bil format to .mxe format. 

You will see a command window opened by the maxent.jar program that will display
progress of the .bil to .mxe conversion process. Do not close this window, it 
will close on its own when the conversion of all rasters is complete. 

Parameters:
input_bil_folder      -- Path to a folder of .bil files created by a Maxent 
                         model

Outputs:
Creates a new folder `input_mxe` containing rasters converted to the Maxent .mxe 
format.
____________________________________________________________________________"""
 
import arcpy
import os
import subprocess

def bil2mxe(input_bil_folder):
    # Set environment variables
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = input_bil_folder
    
    # List parameter values
    arcpy.AddMessage("input_bil_folder: {}".format(input_bil_folder))

    # Convert .bil format to .mxe format
    ## Find the next folder up from input_bil_folder
    parent_folder_input_bil = os.path.dirname(input_bil_folder)

    ## Create `input_mxe` folder
    input_mxe_folder = os.path.join(parent_folder_input_bil, "input_mxe")
    if os.path.isdir(input_mxe_folder) == False:
      os.mkdir(input_mxe_folder)

    ## Call the maxent.jar density.Convert function to convert bil to mxe
    arcpy.AddMessage("Converting rasters to .mxe format. See command window for progress")
    script_path = os.path.dirname(os.path.abspath( __file__ ))
    maxent_path = os.path.join(script_path, "Maxent")
    maxent_jar_path = os.path.join(maxent_path, "maxent.jar")

    subprocess.call(["java", "-Xmx5g", "-cp", maxent_jar_path, "density.Convert",
                     input_bil_folder, "bil", input_mxe_folder, "mxe"])

    arcpy.AddMessage("    Converted rasters to .mxe format")
    
def main():
    # Call the Adh2mxe function with command line parameters
    bil2mxe(input_bil_folder)

if __name__ == "__main__":
    # Get input parameters
    input_bil_folder = arcpy.GetParameterAsText(0)

    main()
