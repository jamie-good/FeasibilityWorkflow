# Example usage: 
# Open Python Command Prompt (should already be in ArcGIS environment)
# Enter: "python create_dem.py "{path to .gbd/Elev_Contours_fc}" "{field name of contour elevations}" "{path to output DEM}"
# Run and wait! 
# I expect this will take a while to run, so to keep ti running in the background if you need to log off, do the follwoing: 
# Go to the computer's power & batery setings and change it so that it never goes to sleep. 

import arcpy
from arcpy.sa import * 
import argparse 

def create_dem(contour_fc, elevation_field, output_dem):
    """
    Creates a DEM from contours lines via ArcGIS Pro's TopoToRaster (Spatial Analyst)
    
    Parameters: 
    - contour_fc (str): Path to input contour feature class (i.e., .gdb > fc)
    - elevation_field (str): Name of column in fc containing controu elevations 
    - output_dem (str): path to save DEM 
    
    Returns:
    - none 
    """
    # Set up env
    arcpy.env.overwriteOutput = True # overwrite if output file already exists 
    arcpy.CheckOutExtension("Spatial") # make sure Spatial Analyst is active 

    # Set up inputs 
    if not arcpy.Exists(contour_fc):
        raise Exception(f"Input feature class not found.")

    field_names = [f.name for f in arcpy.ListFields(contour_fc)]
    if elevation_field not in field_names:
        raise Exception(f"'{elevation_field}' was not found in {contour_fc}. Available fields are: {field_names}")
    
    # Run TopoToRaster 
    try: 
        dem = TopoToRaster([[contour_fc, elevation_field, 'Contour']])
    except Exception as e: 
        raise Exception(f"Error with TopoToRaster: {str(e)}")
    
    # Save output 
    try: 
        dem.save(output_dem)
    except Exception as e: 
        raise Exception(f"Error saving DEM: {str(e)}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a DEM from contour lines with ArcGIS Pro's TopoToRaster")
    parser.add_argument("contour_fc", help="Path to contour feature class (i.e., .gdb from USGS > Elev_Contours)")
    parser.add_argument("elevation_field", help="Field name for elevations of contour lines (i.e., ContourElevations)")
    parser.add_argument("output_dem", help="Path to save output DEM (i.e., dem.tif)")

    args = parser.parse_args()

    create_dem(args.contour_fc, args.elevation_field, args.output_dem)