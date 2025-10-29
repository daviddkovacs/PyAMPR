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

    def __init__(self,
                 path,
                 date,
                 overpass,
                 frequency,
                 *args,
                 **kwargs):

        self.path = path
        self.date = date
        self.overpass = overpass
        self.frequency = frequency

        year_month = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m")
        date_fmt = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")
        pattern = f"amsr2_l1bt_day_{date_fmt}_10km.nc"
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