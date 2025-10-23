import os.path
import rioxarray
import matplotlib.pyplot as plt
import pyampr
import xarray as xr
import pandas as pd
import os

class ER2_Flight():

    def __init__(self,
                 path,
                 date,
                 scan_direction,
                 flight_direction,
                 *args,
                 **kwargs):

        self.path = path
        self.date = date
        self.scan_direction = scan_direction
        self.flight_direction =flight_direction


    def to_pandas(self):

        file_name = f"{self.date}_{self.scan_direction}_{self.flight_direction}.mat_data.csv"
        pandas_ampr = pd.read_csv(os.path.join(self.path,file_name), index_col=False)

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


    def save_tiff(self,
                  dataset,
                  variable):
        data_107 = dataset[variable]
        data_107.rio.write_crs(4326, inplace=True)
        data_107.rio.set_spatial_dims("Latitude", "Longitude")
        data_107.rio.to_raster("/home/ddkovacs/Desktop/xxx.tiff")



MyFlight = ER2_Flight(path ="/home/ddkovacs/shares/climers/Projects/CCIplus_Soil_Moisture/07_data/WHYMSIE/data_from_RichDJ",
              date = "22_Oct",
              scan_direction = "1_25",
              flight_direction = "EW",)



MyFlight.save_nc("/home/ddkovacs/Desktop/")



