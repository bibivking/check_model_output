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

        input_fname =  "%s/%s/LIS_output/LIS.CABLE.2008120100.d01.nc" % (path, casename)
        #input_fname =  "%s/%s/coupled_run/OUTPUT/SURFACEMODEL/LIS_HIST_200902160000.d01.nc" % (path, casename)
        cable = nc.Dataset(input_fname, 'r')

        landmask  =  cable.variables['Landmask_inst'][29,:,:].filled(-9999.)
        landcover =  cable.variables['Landcover_inst'][29,:,:].filled(-9999.)
        # swnet     =  cable.variables['Swnet_tavg'][:,:].filled(-9999.)
        # lwnet     =  cable.variables['Lwnet_tavg'][:,:].filled(-9999.)
        # rnet      =  cable.variables['Rnet_tavg'][:,:].filled(-9999.)
        # qle       =  cable.variables['Qle_tavg'][:,:].filled(-9999.)
        # qh        =  cable.variables['Qh_tavg'][:,:].filled(-9999.)
        # qg        =  cable.variables['Qg_tavg'][:,:].filled(-9999.)
        # snowf     =  cable.variables['Snowf_tavg'][:,:].filled(-9999.)
        # rainf     =  cable.variables['Rainf_tavg'][:,:].filled(-9999.)
        # evap      =  cable.variables['Evap_tavg'][:,:].filled(-9999.)
        # qs        =  cable.variables['Qs_tavg'][:,:].filled(-9999.)
        # qsb       =  cable.variables['Qsb_tavg'][:,:].filled(-9999.)
        # qle       =  cable.variables['Qle_tavg'][:,:].filled(-9999.)
        # qh        =  cable.variables['Qh_tavg'][:,:].filled(-9999.)
        # vegt      =  cable.variables['VegT_tavg'][:,:].filled(-9999.)
        # baresoilT =  cable.variables['BareSoilT_tavg'][:,:].filled(-9999.)
        # avgsurfT  =  cable.variables['AvgSurfT_tavg'][:,:].filled(-9999.)
        # radT      =  cable.variables['RadT_tavg'][:,:].filled(-9999.)
        # albedo    =  cable.variables['Albedo_inst'][:,:].filled(-9999.)
        # swe       =  cable.variables['SWE_inst'][:,:].filled(-9999.)
        # snowdepth =  cable.variables['SnowDepth_inst'][:,:].filled(-9999.)
        # soiltemp  =  cable.variables['SoilTemp_inst'][:,:].filled(-9999.)
        # ecanop    =  cable.variables['ECanop_tavg'][:,:].filled(-9999.)
        # tveg      =  cable.variables['TVeg_tavg'][:,:].filled(-9999.)
        # watertableD =  cable.variables['WaterTableD_tavg'][:,:].filled(-9999.)
        # snowcover =  cable.variables['SnowCover_inst'][:,:].filled(-9999.)
        # gpp       =  cable.variables['GPP_tavg'][:,:].filled(-9999.)
        # npp       =  cable.variables['NPP_tavg'][:,:].filled(-9999.)
        # nee       =  cable.variables['NEE_tavg'][:,:].filled(-9999.)
        # wind      =  cable.variables['Wind_f_inst'][:,:].filled(-9999.)
        # rainf     =  cable.variables['Rainf_f_inst'][:,:].filled(-9999.)
        # tairf     =  cable.variables['Tair_f_inst'][:,:].filled(-9999.)
        # qair      =  cable.variables['Qair_f_inst'][:,:].filled(-9999.)
        # psurf     =  cable.variables['Psurf_f_inst'][:,:].filled(-9999.)
        # swdown    =  cable.variables['SWdown_f_inst'][:,:].filled(-9999.)
        # lwdown    =  cable.variables['LWdown_f_inst'][:,:].filled(-9999.)
        # soiltype  =  cable.variables['Soiltype_inst'][:,:].filled(-9999.)
        # fwsoil    =  cable.variables['fwsoil_tavg'][:,:].filled(-9999.)
        # gwwb      =  cable.variables['GWwb_tavg'][:,:].filled(-9999.)
        # elevation =  cable.variables['Elevation_inst'][:,:].filled(-9999.)
        # lai       =  cable.variables['LAI_inst'][:,:].filled(-9999.)
        # totalprecip =  cable.variables['TotalPrecip_tavg'][:,:].filled(-9999.)

        soilmoist = cable.variables['SoilMoist_inst'][29,0,:,:].filled(-9999.)
        soiltemp  = cable.variables['SoilTemp_inst'][29,5,:,:].filled(-9999.)
        # esoil     =  cable.variables['ESoil_tavg'][0,:,:].filled(-9999.)
        # canopint  =  cable.variables['CanopInt_inst'][0,:,:].filled(-9999.)
        # watmove   =  cable.variables['watmove_tavg'][0,:,:].filled(-9999.)
        # evapfbl   =  cable.variables['EVAPFBL_tavg'][0,:,:].filled(-9999.)
        # relsmc    =  cable.variables['RelSMC_inst'][0,:,:].filled(-9999.)
        # smliqfrac =  cable.variables['SmLiqFrac_inst'][0,:,:].filled(-9999.)
        # smfroz    =  cable.variables['SmFrozFrac_inst'][0,:,:].filled(-9999.)


        for lat in np.arange(0,149):
            for lon in np.arange(0,169):
                # print(soiltemp[lat,lon])
                # print(landmask[lat,lon])
                if (soiltemp[lat,lon] <= 0.) and (landmask[lat,lon] == 1) :
                    print("lat = "+str(lat)+"; lon = "+str(lon)+"; landcover = "+str(landcover[lat,lon]))
                if (soilmoist[lat,lon] <= 0.) and (landmask[lat,lon] == 1) :
                    print("lat = "+str(lat)+"; lon = "+str(lon)+"; landcover = "+str(landcover[lat,lon]))

        cable.close()

if __name__ == "__main__":
    case_name = ["ERAI_ctl_watmove_new_veg"]
    # ["ERAI_watmove"] #["ERAI_ctl","ERAI_beta_exp","ERAI_gw_off","ERAI_or","ERAI_hyre"] # ["ERAI_watmove"]#
    path = "/g/data/w35/mm3972/model/wrf/NUWRF/LISWRF_configs"
    #  "/scratch/w35/mm3972/model/NUWRF"

    main(case_name, path)
