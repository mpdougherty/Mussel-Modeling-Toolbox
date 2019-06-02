"""____________________________________________________________________________
Script Name:          mxe2bil.py
Description:          Converts a folder of Maxent outputs in .mxe format into 
                      .bil format that can be read by ESRI. 
Date:                 06/02/2019

Usage:
Converts a folder of Maxent outputs in .mxe format into a set of files in .bil 
format that can be read by ESRI. 

This tool assumes that you have created a new folder preferably named 
`output_mxe` into which all of the .mxe ouputs from a particular Maxent model 
run have been copied.  

This tool will create a new folder named `output_bil` in the same root folder 
as the `output_mxe` folder you provided in the first parameter. This folder will 
hold the rasters converted from .mxe format to .bil format. 

You will see a command window opened by the maxent.jar program that will display
progress of the .mxe to .bil conversion process. Do not close this window, it 
will close on its own when the conversion of all rasters is complete. 

Parameters:
output_mxe_folder     -- Path to a folder of .mxe files created by a Maxent 
                         model
mask                  -- Path to the mask raster dataset used to create the 
                         Maxent model input rasters

Outputs:
Creates two new folders: `input_bil` (Adh points interpolated to raster in the 
.bil format, and `input_mxe` (.bil rasters converted to the Maxent .mxe format).
____________________________________________________________________________"""
 
import arcpy
import os
import subprocess

def mxe2bil(output_mxe_folder, mask):
    # Set environment variables
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_mxe_folder
    
    # List parameter values
    arcpy.AddMessage("output_mxe_folder: {}".format(output_mxe_folder))

    # Convert .mxe format to .bil format
    ## Find the next folder up from output_mxe_folder
    parent_folder_output_mxe = os.path.dirname(output_mxe_folder)

    ## Create `output_bil` folder
    output_bil_folder = os.path.join(parent_folder_output_mxe, "output_bil")
    if os.path.isdir(output_bil_folder) == False:
      os.mkdir(output_bil_folder)

    ## Call the maxent.jar density.Convert function to convert mxe to bil
    arcpy.AddMessage("Converting rasters to .mxe format. See command window for progress")
    script_path = os.path.dirname(os.path.abspath( __file__ ))
    maxent_path = os.path.join(script_path, "Maxent")
    maxent_jar_path = os.path.join(maxent_path, "maxent.jar")

    subprocess.call(["java", "-Xmx5g", "-cp", maxent_jar_path, "density.Convert",
                     output_mxe_folder, "mxe", output_bil_folder, "bil"])

    arcpy.AddMessage("    Converted rasters to .mxe format")
    
    # Define spatial reference
    arcpy.AddMessage("Defining projection")
    ## Change output workspace folder
    arcpy.env.workspace = output_bil_folder
    ## Get the spatial reference of the mask
    dsc = arcpy.Describe(mask)
    coord_sys = dsc.spatialReference
    arcpy.AddMessage(coord_sys)
    
    ## list rasters and define projection
    rasters = arcpy.ListRasters("*", "BIL")
    for raster in rasters:
        raster_basename = os.path.splitext(os.path.basename(raster))[0]
        arcpy.DefineProjection_management(raster, coord_sys)
        arcpy.AddMessage("    Defined projection for " + raster_basename)

def main():
    # Call the Adh2mxe function with command line parameters
    mxe2bil(output_mxe_folder, mask)

if __name__ == "__main__":
    # Get input parameters
    output_mxe_folder = arcpy.GetParameterAsText(0)
    mask = arcpy.GetParameterAsText(1)

    main()
