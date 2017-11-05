from __future__ import print_function, division
import os
# import numpy as np
# import pandas as pd
import sys


# Manipulate path names to load the correct version of NB, and also to save the
# output files in the NebulaBayes/docs subdirectory.
DOCS_PATH = os.path.dirname(os.path.realpath(__file__))
NB_PARENT_DIR = os.path.split(DOCS_PATH)[0]
sys.path.insert(1, NB_PARENT_DIR)

from NebulaBayes import NB_Model



"""
An example of how to run NebulaBayes.  NebulaBayes works in python 2 and python 3.

For documentation, see the docstrings of the __init__ and __call__ methods of
the NB_Model class in the module NebulaBayes/src/NB0_Main.py

General information for using NebulaBayes for the first time:
 -  NebulaBayes compares a set of observed line fluxes from a single spectrum
    to a grid of 1D photoionization models.  The assumptions used in the
    photoionization models need to be compatible with the observations.  E.g.
    Emission line diagnostics might be used to ensure that e.g. a HII region
    spectrum is being compared to a HII model grid.
 -  Configure the inputs using this example script and the documentation, with
    a uniform prior at first.
 -  Manually inspect the initial NebulaBayes results to see if they are
    reasonable.  Are parameter estimates physical, and if they're at the edge of
    the parameter space is this plausible?  What's the shape of the posterior?
 -  The question "Is there a good fit to the data anywhere in the parameter
    space?" cannot be answered by the NebulaBayes parameter estimates or plots
    of the posterior PDF.  Inspect the "best model" table to see if observed
    emission line fluxes are well fit, and which fluxes are inconsistent with
    the "best" model.
 -  It may be helpful to iterate to gain a sense of how different choices affect
    the results, for example by choosing a different set of emission lines, a 
    different line for normalisation, or a different systematic grid error.
 -  Once the results are reasonable, consider using a non-uniform prior.  There
    might be particular diagnostic line ratios that could help constrain the
    posterior further.  Is it necessary to depend heavily on a prior to
    constrain the parameter space?


Adam D. Thomas 2017
"""


proj_dir = "/Users/.../"
grid_file = "/Users/.../MAPPINGS_HII_Grid_DN_GridPP_line_fluxes.csv"
in_obs_flux = proj_dir + "Obs_data/....csv"
out_corner_plot_dir = proj_dir + "Plot_results/"
out_table_dir = out_corner_plot_dir



# Metadata to use when loading/interpolating the model grid:
# HII grid
grid_params  = ["log_P/k", "log_UH", "log_OH"] # Parameter names from grid file header
interp_shape = [80, 80, 80] # Corresponding number of interpolated pts in each dimension
# # AGN grid
# grid_params = ["E_peak", "UH_at_r_inner", "Press_P/k", "log_OH"]
# interp_shape = [40]*4
# Only the following lines will have model grids interpolated for them:
lines_1 = ['OII3726', 'OII3729', 'Hbeta', 'OIII5007', 'HeI5876', 'Halpha',
              'NII6583', 'SII6716', 'SII6731'] # Must match line names in model grid file header


# Load observed fluxes, errors and wavelengths here...
obs_line_names = [] # Must match line names in model grid file header
obs_fluxes = [] # Normalised to F_Hbeta == 1
obs_flux_errors = [] # Normalised to F_Hbeta == 1
line_lambdas = None #[] # Angstrom.  Only required if you do dereddening in NB (to match
                        # the Balmer decrement at every point in interpolated grid)





# Initialise NB_Model:
NB_Model_1 = NB_Model(grid_file, grid_params, lines_1, interpd_grid_shape=interp_shape)

# Configure options for the NB run:
prior_plot_name      = "{0}_0_prior_corner_plot.pdf".format(out_corner_plot_dir)
# likelihood_plot_name = "{0}_1_likelihood_corner_plot.pdf".format(out_corner_plot_dir)
posterior_plot_name  = "{0}_2_posterior_corner_plot.pdf".format(out_corner_plot_dir)
estimate_table_name  = "{0}_parameter_estimates.csv".format(out_table_dir)
best_model_table = estimate_table_name.replace("parameter_estimates", "best_model")
kwargs = {"posterior_plot":posterior_plot_name, "prior_plot":prior_plot_name,
          "estimate_table":estimate_table_name, "best_model_table":best_model_table,
          "prior":"Uniform", "deredden":False, "obs_wavelengths":line_lambdas,
          "norm_line":"Hbeta"}

# Run the model
Result = NB_Model_1(obs_fluxes, obs_flux_errors, obs_line_names, **kwargs)
# The NB_Model instance can be called repeatedly to do Bayesian parameter
# estimation on different sets of observed fluxes with the same grid (which
# only needs to be interpolated once).
# You can access all the NebulaBayes internal data, PDFs, results, etc. on the
# Result object.



print("Done.")

