import pandas as pd
from validation.ER2_Flight import FlightData
from validation.AMSR2_Observations import SatelliteData
from validation.Comparison import CompareData
import numpy as np
from utils import (
    nn_loc_search,
    filter_distance,
    mpdi,
    )


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


def validation_processor(path_ampr,
                         path_sat,
                         scan_direction,
                         flight_direction,
                         air_f,
                         sat_f,
                         date,
                         fig_path = None):
    """
    Runs validation routine. Collocates Satellite observations to AMPR data, and calculates MPDI for radiometers.

    Parameters
    ----------
    path_ampr: path for AMPR MPDI .csv
    path_sat: path for satellite .nc files (daily, on CCI grid)
    scan_direction: 1_25, 26_50
    flight_direction: WE, EW (ER-2 Flight)
    air_f: 10.7, 19.35, 37.1
    sat_f: 6.9, 7.3, 10.7, 18.7, 23.8, 36.5, 89.0
    date: YYYY-MM-DD
    fig_path: optional path to save figure

    Returns
    -------

    """
    ER2_flight = FlightData(path=path_ampr,
                            date=date,
                            scan_direction=scan_direction,
                            flight_direction=flight_direction,
                            frequency= air_f,
                            )

    AMSR2_OBS = SatelliteData(path=path_sat,
                              date=date,
                              overpass="night",
                              frequency= sat_f,
                              )

    air_mpdi, sat_mpdi = collocate_mpdi(ER2_flight, AMSR2_OBS,)

    Figs = CompareData(air_mpdi,
                sat_mpdi,
                AMPR_f,
                AMSR2_f,
                date)

    Figs.longitude_plot(savedir = fig_path,
                        flight_direction = flight_direction,
                        scan_direction = scan_direction )

    Figs.scatter_plot(savedir = fig_path,
                        flight_direction = flight_direction,
                        scan_direction = scan_direction )


if __name__ == "__main__":
    """
    Setup:
    Available frequencies: 
        FlightData (AMPR) : 10.7, 19.35, 37.1
        SatelliteData (AMSR2) : 6.9, 7.3, 10.7, 18.7, 23.8, 36.5, 89.0
    """
    path_ampr = r"G:\My Drive\Munka\CLIMERS\ER2_validation\AMPR\data_from_RichDJ"
    path_amsr = r"G:\My Drive\Munka\CLIMERS\ER2_validation\AMSR2"
    date = "2024-10-31"
    flight_direction = "EW"
    scan_direction = "1_25"
    AMPR_f = "37.1"
    AMSR2_f = "36.5"
    figpath = rf"G:\My Drive\Munka\CLIMERS\ER2_validation\figures"

    validation_processor(
        path_ampr = path_ampr,
        path_sat=path_amsr,
        scan_direction=scan_direction,
        flight_direction=flight_direction,
        air_f =AMPR_f,
        sat_f=AMSR2_f,
        date=date,
        fig_path=figpath,
    )


