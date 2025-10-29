import pandas as pd

from validation.ER2_Flight import FlightData
from validation.AMSR2_Observations import SatelliteData
import numpy as np
from utils import (to_radians
                   ,nn_loc_search)

date = "2024-10-25"

ER2_flight = FlightData(path =r"G:\My Drive\Munka\CLIMERS\ER2_validation\AMPR\data_from_RichDJ",
                      date = date,
                      scan_direction = "26_50",
                      flight_direction = "WE", )



AMSR2_OBS = SatelliteData(path = r"G:\My Drive\Munka\CLIMERS\ER2_validation\AMSR2",
                          date = date,
                          overpass="day",
                          )

air_data = ER2_flight.to_pandas()
sat_data  = AMSR2_OBS.to_pandas()


test1 = pd.DataFrame({"lat" : [30,40,50],
                      "lon": [30,40,50]})

test2 = pd.DataFrame({"lat" : [31,29],
                      "lon": [31,29]})

distances, idx = nn_loc_search(sat_data,air_data)











