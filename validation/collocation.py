import pandas as pd
from validation.ER2_Flight import FlightData
from validation.AMSR2_Observations import SatelliteData
import numpy as np
from utils import (
    nn_loc_search,
    filter_distance,
    mpdi)


def collocate_mpdi(ref_obj,
                    test_obj,
                    freq):
    """

    Parameters
    ----------
    ref_obj: Reference AMPR object, constructed with ER2_flight class
    test_obj: Test Satellite object, constructed with SatelliteData class
    freq: Frequency in GHz
    
    This function collocates ER2 and Satellite observations in space and 

    Returns
    -------

    """

    air_data = ref_obj.to_pandas()
    sat_data = test_obj.to_pandas()

    # Find NN observations to all locs in air_data
    nearest_locs = nn_loc_search(sat_data, air_data)
    # Filter NN to a max radius, i.e.: 15km
    filtered_nearest_locs = filter_distance(nearest_locs)

    # Filter both datasets to NN<15km observations
    sat_data_nn = sat_data.iloc[filtered_nearest_locs["index_nn"]]
    air_data_nn = air_data.iloc[filtered_nearest_locs["index_ref"]]

    # calculate MPDI from satellite data
    sat_data_nn[f" MPDI {freq}"] = mpdi(sat_data_nn[f"bt_{freq}V"],
                                        sat_data_nn[f"bt_{freq}H"])

    sat_mpdi = sat_data_nn.filter(["lat", "lon", "scantime", f"MPDI {freq}"], axis=1).reset_index(drop=True)
    air_mpdi = air_data_nn.filter(["lat", "lon", f"MPDI {freq}"], axis=1).reset_index(drop=True)

    del sat_data_nn
    del air_data_nn

    return sat_mpdi, air_mpdi


if __name__ == "__main__":

    date = "2024-10-25"

    ER2_flight = FlightData(path=r"G:\My Drive\Munka\CLIMERS\ER2_validation\AMPR\data_from_RichDJ",
                            date=date,
                            scan_direction="26_50",
                            flight_direction="WE",
                            )

    AMSR2_OBS = SatelliteData(path=r"G:\My Drive\Munka\CLIMERS\ER2_validation\AMSR2",
                              date=date,
                              overpass="day",
                              )

    sat_mpdi, air_mpdi = collocate_mpdi(ER2_flight,
                                        AMSR2_OBS,
                                        freq="10.7")

