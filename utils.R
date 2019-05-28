# Utility R functions needed by the Mussel Modeling toolbox. 

#' @title Install and load needed packages
#' 
#' @description Tests if packages are installed and if not installs them. Once
#'     packages are installed it loads them. 
#' 
#' @export
#' @param need_pkgs      A character vector of package names.
#' 
#' @return Installs and loads the requested packages.
#' 
#' @details Replaces the `pacman::p_load` function that requires the latest R 
#'     version. This function uses only base R functions. This function only 
#'     installs packages from the currently set repositories (e.g., CRAN, 
#'     CRANextra). 
#' 
load_packages <- function(need_pkgs) {
  # Determine the uninstalled packages from need_pkgs
  uninst_pkgs <- need_pkgs[!(need_pkgs %in% installed.packages()[, "Package"])]
  # Install uninstalled packages
  if (length(uninst_pkgs)) install.packages(uninst_pkgs, dependencies = TRUE)
  # Load all needed packages
  lapply(need_pkgs, require, character.only = TRUE)
}


load_resri <- function() {
  # Install `resri` from github
  if (!require("resri")) {
    devtools::install_github(repo = "mpdougherty/resri",
                             force = TRUE,
                             upgrade = TRUE,
                             dependencies = TRUE,
                             options(install.packages.check.source = "no"))
    if ("resri" %in% rownames(installed.packages()) == TRUE) {
      message("The `resri` package was installed.")
    }
  } else {
    if ("resri" %in% rownames(installed.packages()) == TRUE) {
      message("The `resri` package was already installed.")
    }
  }
}


load_mcat <- function() {
  # Install `mcat` from github
  if (!require("mcat")) {
    devtools::install_github(repo = "mpdougherty/mcat",
                             force = TRUE,
                             upgrade = TRUE,
                             dependencies = TRUE,
                             options(install.packages.check.source = "no"))
    if ("resri" %in% rownames(installed.packages()) == TRUE) {
      message("The `mcat` package was installed.")
    }
  } else {
    if ("mcat" %in% rownames(installed.packages()) == TRUE) {
      message("The `mcat` package was already installed.")
    }
  }
}