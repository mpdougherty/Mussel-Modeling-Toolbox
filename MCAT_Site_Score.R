#' Calculates the Mussel Community Assessment Tool (MCAT) metrics for the input
#' mussel individuals feature class.
#'
#' Args:
#'    individuals_fc:     character; the full path to an ESRI mussel individuals 
#'                        points feature class
#'
#' Returns:
#'    A new feature class called `mcat_site_score` with the values of each MCAT
#'    metric and the overall MCAT site score. 
#'
tool_exec <- function(in_params, out_params) {
  # Load utility R functions
  dir_name <- getSrcDirectory(function(x) {x})
  source(file.path(dir_name, "utils.R"))
  # Load required libraries
  # Load required libraries
  load_packages(c("devtools", "sf", "dplyr", "vegan"))
  
  # Load the resri package
  load_resri()
  
  # gp tool parameters
  individuals_fc  <- in_params[[1]]
  
  # Variable for testing in RStudio
  # library(arcgisbinding)
  # arc.check_product()
  # individuals_fc = "//mvrdfs.mvr.ds.usace.army.mil/EGIS/Work/EMP/HREP_Projects/SteamboatSlough/Mussels/Mussel-Modeling-Toolbox/tests/data/mussels.gdb/cordova_individuals"
  
  # Import fc to sf
  individuals_sf <- resri::arc2sf(individuals_fc)
  
  # Convert sf to data frame
  individuals <- st_drop_geometry(individuals_sf)
  
  # Calculate the MCAT site score 
  mcat <- mcat::mcat_site_score(individuals)
  
  # Create the sample feature class
  sample <- 
    individuals_sf %>%
    group_by(SampleID) %>%
    summarize()
  
  # Join `mcat_site_score` table back to individuals feature class 
  mcat_site_score <- merge(sample, mcat, 
                           by.x = "SampleID", 
                           by.y = "SampleID")
  
  # Write the output back to the file system
  output_workspace <- dirname(individuals_fc)
  sf2arc(sf_obj = mcat_site_score, 
         fc_path = paste0(output_workspace, "/mcat_site_score"))
  
  return(out_params)
}