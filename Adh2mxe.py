"""____________________________________________________________________________
Script Name:          Adh2mxe.py
Description:          Converts a .csv file of Adh outputs to the Maxent .mxe 
                      format. 
Date:                 05/30/2019

Usage:
Converts a .csv file of Adh outputs for multiple variables to the .bil format 
using IDW interpolation. It then converts the folder of .bil rasters to the 
Maxent .mxe raster format. 

This tool assumes that the following fields iare present in the Adh outputs 
file: X, Y, Z, Depth, Velocity, Bed_Shear_Stress, Froude_Number, and 
Reynolds_Number. Edit the input .csv file to ensure these field names are used. 

Two output folders will be created in the adh_file base folder. One folder
named `input_bil` will hold the interpolated Adh rasters created from the 
adh_file in the ESRI readable .bil format. The second folder named `input_mxe` 
will hold the rasters in the `input_bil` folder converted to the Maxent readable 
.mxe format. The .mxe format can only be read by Maxent, but allows it to run 
much more efficiently. 

You will see a command window opened by the maxent.jar program that will display
progress of the .bil to .mxe conversion process. Do not close this window, it 
will close on its own when the conversion of all rasters is complete. 

Parameters:
adh_file              -- Path to the AdH output .csv file
coordinate_system     -- Coordinate system of the adh_file
mask                  -- Path to the mask raster dataset
flow_prefix           -- String used to denote the flow level of the Adh model

Outputs:
Creates two new folders: `input_bil` (Adh points interpolated to raster in the 
.bil format, and `input_mxe` (.bil rasters converted to the Maxent .mxe format).
____________________________________________________________________________"""
 
import arcpy
import os
import subprocess

from bil2mxe import bil2mxe

def Adh2mxe(adh_file, coordinate_system, mask, flow_prefix):
    # Set environment variables
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(adh_file)
    arcpy.env.scratchWorkspace = os.path.dirname(adh_file)
    
    # List parameter values
    arcpy.AddMessage("Adh_file: {}".format(adh_file))

    # Import adh_file as table into scratch.gdb
    fieldmap = 'X "X" true true false 8 Double 0 0 ,First,#,{0},X,-1,-1;Y "Y" true true false 8 Double 0 0 ,First,#,{0},Y,-1,-1;Z "Z" true true false 8 Double 0 0 ,First,#,{0},Z,-1,-1;Depth "Depth" true true false 8 Double 0 0 ,First,#,{0},Depth,-1,-1;Velocity "Velocity" true true false 4 Double 0 0 ,First,#,{0},Velocity,-1,-1;Bed_Shear_Stress "Bed_Shear_Stress" true true false 4 Double 0 0 ,First,#,{0},Bed_Shear_Stress,-1,-1;Froude_Number "Froude_Number" true true false 4 Double 0 0 ,First,#,{0},Froude_Number,-1,-1;Reynolds_Number "Reynolds_Number" true true false 4 Double 0 0 ,First,#,{0},Reynolds_Number,-1,-1'.format(adh_file)
    adh_file_name = os.path.splitext(os.path.basename(adh_file))[0]
    arcpy.TableToTable_conversion(in_rows = adh_file,
                                  out_path = arcpy.env.scratchGDB,
                                  out_name = adh_file_name,
                                  field_mapping = fieldmap)

    # Adh mesh node to XY Event Layer
    in_table = os.path.join(arcpy.env.workspace, "scratch.gdb", adh_file_name)
    arcpy.MakeXYEventLayer_management(table = in_table,
                                      in_x_field = "X",
                                      in_y_field = "Y",
                                      out_layer = "adh_events",
                                      spatial_reference = coordinate_system)

    # Set mask environments
    arcpy.env.mask = mask
    arcpy.env.extent = mask
    arcpy.env.cellSize = mask
    arcpy.env.snapRaster = mask
    arcpy.env.outputCoordinateSystem = mask

    # Convert Adh mesh nodes to points
    arcpy.AddMessage("Interpolating Adh mesh nodes to raster")

    ## depth
    depth = arcpy.sa.Idw(in_point_features = "adh_events",
                         z_field = "Depth")
    depth.save(os.path.join(flow_prefix + "_depth.tif"))
    arcpy.AddMessage("    Interpolated depth")

    ## velocity
    velocity = arcpy.sa.Idw(in_point_features = "adh_events",
                            z_field = "Velocity")
    velocity.save(os.path.join(flow_prefix + "_velocity.tif"))
    arcpy.AddMessage("    Interpolated velocity")

    ## shear_stress
    shear_stress = arcpy.sa.Idw(in_point_features = "adh_events",
                                z_field = "Bed_Shear_Stress")
    shear_stress.save(os.path.join(flow_prefix + "_ss.tif"))
    arcpy.AddMessage("    Interpolated shear stress")

    ## froude_number
    froude_number = arcpy.sa.Idw(in_point_features = "adh_events",
                                 z_field = "Froude_Number")
    froude_number.save(os.path.join(flow_prefix + "_froude.tif"))
    arcpy.AddMessage("    Interpolated Froude number")

    ## reynolds_number
    reynolds_number = arcpy.sa.Idw(in_point_features = "adh_events",
                                   z_field = "Reynolds_Number")
    reynolds_number.save(os.path.join(flow_prefix + "_reynolds.tif"))
    arcpy.AddMessage("    Interpolated Reynolds number")

    ## slope
    slope = arcpy.sa.Slope(in_raster = depth,
                           output_measurement = "DEGREE",
                           z_unit = "FOOT")
    slope.save(os.path.join(flow_prefix + "_slope.tif"))
    arcpy.AddMessage("    Calculated slope")

    # Convert to .bil format
    arcpy.AddMessage("Converting rasters to .bil format")

    ## Create `input_bil` folder
    input_bil_folder = os.path.join(arcpy.env.workspace, "input_bil")
    if os.path.isdir(input_bil_folder) == False:
      os.mkdir(input_bil_folder)

    ## list rasters and convert to .bil format
    rasters = arcpy.ListRasters()
    for raster in rasters:
        raster_basename = os.path.splitext(os.path.basename(raster))[0]
        bil_raster = os.path.join(input_bil_folder, raster_basename + ".bil")
        arcpy.CopyRaster_management(in_raster = raster,
                                    out_rasterdataset = bil_raster)
        arcpy.Delete_management(raster)
        arcpy.AddMessage("    Converted " + raster_basename + " to .bil format")
    
    # # Convert .bil format to .mxe format
    bil2mxe(input_bil_folder)
    
    
def main():
    # Call the Adh2mxe function with command line parameters
    Adh2mxe(adh_file, coordinate_system, mask, flow_prefix)

if __name__ == "__main__":
    # Get input parameters
    adh_file = arcpy.GetParameterAsText(0)
    coordinate_system = arcpy.GetParameterAsText(1)
    mask = arcpy.GetParameterAsText(2)
    flow_prefix = arcpy.GetParameterAsText(3)

    main()
