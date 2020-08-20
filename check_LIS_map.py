#!/usr/bin/env python

"""
Use LIS-CABLE half-hour met output to make met file for offline CABLE

Source: generate_CABLE_netcdf_met_imp.py

Includes:

That's all folks.
"""

__author__    = "MU Mengyuan"
__email__     = "mu.mengyuan815@gmail.com"

import os
import sys
import glob
import pandas as pd
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import datetime
from scipy.interpolate import interp1d
from scipy.interpolate import griddata

def main(case_name, path):

    for casename in case_name:
        print(casename)
        input_fname =  "%s/%s/LIS_output/LIS.CABLE.2018100100.d01.nc" % (path, casename)
        cable = nc.Dataset(input_fname, 'r')
        landmask = cable.variables['Landmask_inst'][0,:,:].filled(-9999.)
        landcover= cable.variables['Landcover_inst'][0,:,:].filled(-9999.)
        soilmoist = cable.variables['SoilMoist_tavg'][29,0,:,:].filled(-9999.)
        soiltemp  = cable.variables['SoilTemp_tavg'][29,5,:,:].filled(-9999.)

        print(soilmoist[62,53])
        print(soiltemp[62,53])
        for lat in np.arange(0,149):
            for lon in np.arange(0,169):
                if (np.isnan(soilmoist[lat,lon])) : # and (landmask[lat,lon] == 1)
                    print("lat = "+str(lat)+"; lon = "+str(lon)+"; landcover = "+str(landcover[lat,lon]))

        cable.close()

if __name__ == "__main__":

    case_name = ["ERAI_ctl","ERAI_beta_exp","ERAI_gw_off","ERAI_or","ERAI_hyre"]
    path = "/g/data/w35/mm3972/model/wrf/NUWRF/LISWRF_configs"

    main(case_name, path)
