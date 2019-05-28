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
  source("utils.R")
  # Load required libraries
  load_packages(c("sp", "dplyr", "tigris"))
  
  # gp tool parameters
  individuals_fc  <- in_params[[1]]
  
  
  
  
  # Join `mcat_site_score` table back to individuals feature class 
  
  return(out_params)
}