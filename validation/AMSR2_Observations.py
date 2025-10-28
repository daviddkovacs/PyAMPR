import os.path
import rioxarray
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from datetime import datetime

import xarray as xr
import pandas as pd
import os
import geopy

class SatelliteData:

    def __init__(self,
                 path,
                 date,
                 overpass,
                 *args,
                 **kwargs):

        self.path = path
        self.date = date
        self.overpass = overpass

        year_month = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m")
        date_fmt = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")
        pattern = f"amsr2_l1bt_day_{date_fmt}_10km.nc"
        self.bt_file = os.path.join(path,overpass,year_month,pattern)

    def to_pandas(self):

        dataset = self.to_xarray()
        pandas = dataset.to_dataframe().reset_index()

        return pandas


    def to_xarray(self,
                  ):

        dataset = xr.open_dataset(self.bt_file, decode_timedelta=False)
        dataset = dataset.squeeze("time", drop=True)
        return dataset

AMSR2_OBS = SatelliteData(r"G:\My Drive\Munka\CLIMERS\ER2_validation\AMSR2",
                          "2024-10-25",
                          "day",
                          )

dataset  = AMSR2_OBS.to_pandas()


dataset["bt_10.7V"]
