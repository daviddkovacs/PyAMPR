import os.path
import rioxarray
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from datetime import datetime
import xarray as xr
import pandas as pd
import os

class FlightData:

    def __init__(self,
                 path,
                 date,
                 scan_direction,
                 flight_direction,
                 *args,
                 **kwargs):

        self.path = path
        self.date = datetime.strptime(date, "%Y-%m-%d").strftime("%d_%b")
        self.scan_direction = scan_direction
        self.flight_direction =flight_direction


    def to_pandas(self):

        file_name = f"{self.date}_{self.scan_direction}_{self.flight_direction}.mat_data.csv"
        pandas_ampr = pd.read_csv(os.path.join(self.path,file_name), index_col=False)
        pandas_ampr = pandas_ampr.rename(columns={"Longitude": "lon", "Latitude": "lat"})

        return pandas_ampr


    def to_xarray(self):

        dataset = self.to_pandas()
        indexed_dataset =  dataset.set_index(["Longitude", "Latitude"])
        xarray_ampr = indexed_dataset.to_xarray()

        return xarray_ampr


    def save_nc(self,
                outpath,):

        fname = f"{self.date}_{self.scan_direction}_{self.flight_direction}.nc"
        dataset = self.to_xarray()
        comp = {var: {"zlib": True, "complevel": 4} for var in dataset.data_vars}
        dataset.to_netcdf(os.path.join(outpath, fname), encoding=comp)


    def longitude_plot(self,frequency):

        lon = self.to_pandas()["Longitude"]
        freq_vals = self.to_pandas()[f"MPDI {frequency}"]

        plt.figure(figsize=(8,4))
        plt.plot(lon, freq_vals, linewidth=1)
        plt.xlabel("Longitude")
        plt.ylabel(f"MPDI {frequency}")
        plt.title(f" Flight: {self.date}\n Direction: {self.flight_direction}\n scan: {self.scan_direction}")
        plt.grid(True)
        plt.tight_layout()
        plt.show(block=True)
