import os.path
import rioxarray
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from datetime import datetime
import xarray as xr
import pandas as pd
import os

class SatelliteData:
    """
    Class to read in Satellite data from (currently from AMSR2)

    path: location of .nc files
    sensor: satellite sensor used (currently amsr2)
    date: in format YYYY-MM-DD
    overpass: day, night
    target_res: pixel resolution 10 or 25 (km)
    frequency: 6.9, 7.3, 10.7, 18.7, 23.8, 36.5, 89.0
    """
    def __init__(self,
                 path,
                 sensor,
                 date,
                 overpass,
                 target_res,
                 frequency,
                 *args,
                 **kwargs):

        self.frequency = frequency

        year_month = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m")
        date_fmt = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")

        pattern = f"{sensor}_l1bt_{overpass}_{date_fmt}_{target_res}km.nc"
        self.bt_file = os.path.join(path,overpass,year_month,pattern)


    def to_pandas(self):

        dataset = self.to_xarray()
        pandas = dataset.to_dataframe()
        pandas = pandas.dropna(subset=['scantime']).reset_index()
        pandas = pandas[["lon","lat","scantime", f"bt_{self.frequency}V", f"bt_{self.frequency}H"]]

        return pandas


    def to_xarray(self,
                  ):

        dataset = xr.open_dataset(self.bt_file, decode_timedelta=False)
        dataset = dataset.squeeze("time", drop=True)

        return dataset