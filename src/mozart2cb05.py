import numpy as np
import pandas as pd
import xarray as xr

def open_wrfchemis(wrfchemi_path):
    wrfchemi = xr.open_dataset(wrfchemi_path)
    return wrfchemi

def get_emiss_list(wrfchemi):
    wrfchemi_vars = list(wrfchemi.var())
    emiss_list = [emiss for emiss in wrfchemi_vars 
                  if emiss.startswith("E_")]
    return emiss_list

def emiss_mozart_to_cb05(wrfchemi_moz, E_MOZ, factor):
    wrfchemi_cb05_E = wrfchemi_moz[E_MOZ] * factor
    wrfchemi_cb05_E.attrs = wrfchemi_moz[E_MOZ].attrs
    return wrfchemi_cb05_E

def mozart_cb05_mapping():
    # E_CB05 : (E_MOZ, frac)
    moz2cb05 = {
        "E_ALD2": ("E_CH3CHO", .5),
        "E_ALDX": ("E_CH3CHO", .5),
        "E_BENZENE": ("E_BENZENE", 1.),
        "E_CO": ("E_CO", 1.),
        "E_ETHA": ("E_C2H6", 1.),
        "E_ETH": ("E_C2H4", 1.),
        "E_ETOH": ("E_C2H5OH", 1.),
        "E_FORM": ("E_CH2O", 1.),
        "E_ISOP": ("E_ISOP", 1.),
        "E_MEOH": ("E_CH3OH", 1.),
        "E_NH3" : ("E_NH3", 1.),
        "E_NO2" : ("E_NO2", 1.),
        "E_NO": ("E_NO", 1.),
        "E_HONO": ("E_HONO", 1.),
        "E_SO2": ("E_SO2", 1.),
        "E_TERP": ("E_C10H16", 1.),
        "E_TOL": ("E_TOLUENE", 1.),
        "E_XYL": ("E_XYLENE", 1.),
        "E_OLE": ("E_C3H6", .5),
        "E_PAR": ("E_C3H6", .5),
        "E_IOLE": ("E_BIGENE", .3),
        "E_PM25I": ("E_PM25I", 1.),
        "E_PM25J": ("E_PM25J", 1.),
        "E_NAI": ("E_NAI", 1.),
        "E_NAJ": ("E_NAJ", 1.),
        "E_CLI": ("E_CLI", 1.),
        "E_CLJ": ("E_CLJ", 1.),
        "E_ORGI": ("E_ORGI", 1.),
        "E_ORGJ": ("E_ORGJ", 1.),
        "E_ECI": ("E_ECI", 1.),
        "E_ECJ": ("E_ECJ", 1.),
        "E_SO4I": ("E_SO4I", 1.),
        "E_SO4J": ("E_SO4J", 1.),
        "E_NO3I": ("E_NO3I", 1.),
        "E_NO3J": ("E_NO3J", 1.),
        "E_NH4I": ("E_NH4I", 1.),
        "E_NH4J": ("E_NH4J", 1.),
        "E_PM_10": ("E_PM_10", 1.),
    }
    return moz2cb05

def creating_wrfchemi_cb05(wrfchemi_moz_path):
    wrfchemi = open_wrfchemis(wrfchemi_moz_path)
    emiss_list = get_emiss_list(wrfchemi)
    wrfchemi_cb05 = xr.Dataset()
    wrfchemi_cb05["Time"] = wrfchemi["Time"]
    wrfchemi_cb05["Times"] = wrfchemi["Times"]
    moz2cb05 = mozart_cb05_mapping()

    for E_CB05 in moz2cb05.keys():
        wrfchemi_cb05[E_CB05] = emiss_mozart_to_cb05(wrfchemi,
                                                     moz2cb05[E_CB05][0],
                                                     moz2cb05[E_CB05][1])
    wrfchemi_cb05.attrs = wrfchemi.attrs
    return wrfchemi_cb05


def writting_netcdf(wrfchemi_cb05, file_name, path="../results/"):
    full_name = path + file_name
    wrfchemi_cb05.to_netcdf(full_name,
                            encoding={
                                "Times": {
                                    "char_dim_name": "DateStrLen"
                                }
                            },
                            unlimited_dims={"Time": True},
                            format="NETCDF3_64BIT")

if __name__ == "__main__":
    wrfchemi_moz_path_00z = "../data/wrfchemi_00z_d01"
    wrfchemi_moz_path_12z = "../data/wrfchemi_12z_d01"
    wrfchemi00z = xr.open_dataset(wrfchemi_moz_path_00z)
    wrfchemi12z = xr.open_dataset(wrfchemi_moz_path_12z)
    wrfchemi_cb05_00z = creating_wrfchemi_cb05(wrfchemi_moz_path_00z)
    wrfchemi_cb05_12z = creating_wrfchemi_cb05(wrfchemi_moz_path_12z)

    writting_netcdf(wrfchemi_cb05_00z, "wrfchemi_00z_d01_cb05")
    writting_netcdf(wrfchemi_cb05_12z, "wrfchemi_12z_d01_cb05")
    








    
