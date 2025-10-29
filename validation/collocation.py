import pandas as pd
from validation.ER2_Flight import FlightData
from validation.AMSR2_Observations import SatelliteData
import numpy as np
from utils import (
    nn_loc_search,
    filter_distance,
    mpdi,
    longitude_combined_plot)


def collocate_mpdi(ref_obj,
                    test_obj,
                    ):
    """

    Parameters
    ----------
    ref_obj: Reference AMPR object, constructed with ER2_flight class
    test_obj: Test Satellite object, constructed with SatelliteData class

    This function collocates ER2 and Satellite observations in space and calculates MPDI for a band

    Returns
    -------
    sat_mpdi, air_mpdi
    """

    air_data = ref_obj.to_pandas()
    sat_data = test_obj.to_pandas()

    ampr_freq = ref_obj.frequency
    sat_freq = test_obj.frequency


    # Find NN observations to all locs in air_data
    nearest_locs = nn_loc_search(sat_data, air_data)
    # Filter NN to a max radius, i.e.: 15km
    filtered_nearest_locs = filter_distance(nearest_locs)

    # Filter both datasets to NN<15km observations
    sat_data_nn = sat_data.iloc[filtered_nearest_locs["index_nn"]]
    air_data_nn = air_data.iloc[filtered_nearest_locs["index_ref"]]

    # calculate MPDI from satellite data
    sat_data_nn[f"MPDI {sat_freq}"] = mpdi(sat_data_nn[f"bt_{sat_freq}V"],
                                        sat_data_nn[f"bt_{sat_freq}H"])

    sat_mpdi = sat_data_nn.filter(["lat", "lon", "scantime", f"MPDI {sat_freq}"], axis=1).reset_index(drop=True)
    air_mpdi = air_data_nn.filter(["lat", "lon", f"MPDI {ampr_freq}"], axis=1).reset_index(drop=True)

    del sat_data_nn
    del air_data_nn

    return air_mpdi,sat_mpdi


if __name__ == "__main__":
    """
    Available frequencies: 
        AMPR : 10.7, 19.35, 37.1
        AMSR2 : 6.9, 7.3, 10.7, 18.7, 23.8, 36.5, 89.0
    """
    date = "2024-10-25"
    AMPR_f = "10.7"
    AMSR2_f = "10.7"

    ER2_flight = FlightData(path=r"G:\My Drive\Munka\CLIMERS\ER2_validation\AMPR\data_from_RichDJ",
                            date=date,
                            scan_direction="26_50",
                            flight_direction="WE",
                            frequency= AMPR_f
                            )

    AMSR2_OBS = SatelliteData(path=r"G:\My Drive\Munka\CLIMERS\ER2_validation\AMSR2",
                              date=date,
                              overpass="night",
                              frequency= AMSR2_f
                              )

    air_mpdi, sat_mpdi = collocate_mpdi(ER2_flight,
                                        AMSR2_OBS,
                                        )

    longitude_combined_plot(air_mpdi,
                            sat_mpdi,
                            AMPR_f,
                            AMSR2_f,
                            date)

