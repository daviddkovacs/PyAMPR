import pandas as pd
from validation.ER2_Flight import AirborneData
from validation.Satellite_Observations import SatelliteData
from validation.Comparison import FigVarSingular, FigVarBase
from utils import collocate_mpdi
import pandas as pd


def validate_compound(
                    path_air,
                    air_freq,
                    sat_sensor,
                    path_sat,
                    sat_freq,
                    overpass,
                    target_res,
                      ):

    datelist = ["2024-10-22", "2024-10-25", "2024-10-31"]
    flight_direction_list = ["WE", "EW"]
    scan_direction_list = ["1_25", "26_50"]

    air_mpdi_compound = pd.DataFrame({"lat": [], "lon": [], f"MPDI {air_freq}": []})
    sat_mpdi_compound = pd.DataFrame({"lat": [], "lon": [], f"MPDI {sat_freq}": []})

    for d in datelist:
        for f in flight_direction_list:
            for s in scan_direction_list:
                ER2_flight = AirborneData(path=path_air,
                                          date=d,
                                          scan_direction=s,
                                          flight_direction=f,
                                          air_freq=air_freq,
                                          )

                AMSR2_OBS = SatelliteData(path=path_sat,
                                          sat_sensor=sat_sensor,
                                          date=d,
                                          overpass=overpass,
                                          target_res=target_res,
                                          sat_freq=sat_freq,
                                          )

                air_mpdi, sat_mpdi = collocate_mpdi(ER2_flight, AMSR2_OBS)

                air_mpdi_compound = pd.concat([air_mpdi_compound, air_mpdi["filtered"]])  # get filtered AMPR MPDI
                sat_mpdi_compound = pd.concat([sat_mpdi_compound, sat_mpdi["filtered"]])  # get filtered Satellite MPDI

    CompoundVars = FigVarBase(
        air_freq = air_freq,
        flight_direction = "",
        scan_direction= "",
        sat_sensor = sat_sensor,
        overpass = overpass,
        target_res = target_res,
        sat_freq =  sat_freq,
        date = ""
    )

    CompoundVars.scatter_plot(ref = air_mpdi_compound[f"MPDI {air_freq}"],
                              test = sat_mpdi_compound[f"MPDI {sat_freq}"])


def validate_all(path_air,
                 path_sat,
                 figpath):

    datelist = ["2024-10-22", "2024-10-25", "2024-10-31"]
    flight_direction_list = ["WE", "EW"]
    scan_direction_list = ["1_25", "26_50"]
    AMPR_f_list = ["10.7", "19.35", "37.1"]
    AMSR2_f_list = ["10.7", "18.7", "36.5"]

    for d in datelist:
        for f in flight_direction_list:
            for s in scan_direction_list:
                for a_f, s_f in zip(AMPR_f_list, AMSR2_f_list):
                    print(f"{d} {f} {s}")
                    validate_singular(
                        path_air=path_air,
                        path_sat=path_sat,
                        scan_direction=s,
                        flight_direction=f,
                        sat_sensor=sat_sensor,
                        air_freq=a_f,
                        sat_freq=s_f,
                        date=d,
                        overpass=overpass,
                        target_res=target_res,
                        fig_path=figpath,
                        show_fig=False
                    )


def validate_singular(path_air,
                      scan_direction,
                      flight_direction,
                      air_freq,
                      path_sat,
                      sat_sensor,
                      sat_freq,
                      overpass,
                      target_res,
                      date,
                      fig_path=None,
                      show_fig=True):
    """
    Runs validation routine. Collocates Satellite observations to AMPR data, and calculates MPDI for radiometers.

    Parameters
    ----------
    path_air: path for AMPR MPDI .csv files
    path_sat: path for satellite .nc files (daily, on CCI grid)
    scan_direction (str): '1_25', '26_50'
    flight_direction (str): 'WE', 'EW' (ER-2 Flight)
    air_f (str): 10.7, 19.35, 37.1
    sat_f (str): 6.9, 7.3, 10.7, 18.7, 23.8, 36.5, 89.0
    date: YYYY-MM-DD
    fig_path: optional path to save figure

    Returns
    -------

    """
    ER2_flight = AirborneData(path=path_air,
                              date=date,
                              scan_direction=scan_direction,
                              flight_direction=flight_direction,
                              air_freq=air_freq,
                              )

    AMSR2_OBS = SatelliteData(path=path_sat,
                              sat_sensor=sat_sensor,
                              date=date,
                              overpass=overpass,
                              target_res=target_res,
                              sat_freq=sat_freq,
                              )

    air_mpdi, sat_mpdi = collocate_mpdi(ER2_flight, AMSR2_OBS, )

    Figs = FigVarSingular(ER2_flight, AMSR2_OBS)

    ref_x_filter = air_mpdi["filtered"]["lon"]
    ref_y_filter = air_mpdi["filtered"][f"MPDI {air_freq}"]
    ref_x_orig = air_mpdi["original"]["lon"]
    ref_y_orig = air_mpdi["original"][f"MPDI {air_freq}"]

    sat_x_filter = sat_mpdi["filtered"]["lon"]
    sat_y_filter = sat_mpdi["filtered"][f"MPDI {sat_freq}"]


    Figs.longitude_plot(ref_x=ref_x_orig,
                        ref_y=ref_y_orig,
                        test_x=sat_x_filter,
                        test_y=sat_y_filter,
                        savedir=fig_path,
                        show_fig=show_fig)

    Figs.scatter_plot(ref=ref_y_filter,
                      test=sat_y_filter,
                      savedir=fig_path,
                      show_fig=show_fig)

if __name__ == "__main__":
    """
    #### Airborne Setup ####
    Frequencies:
        '10.7', '19.35', '37.1'
    Flight Directions:
        'EW', 'WE'
    Scan directions:
        '1_25', '26_50'


    #### Satellite Setup ####
    Frequencies (AMSR2):
        '6.9', '7.3', '10.7', '18.7', '23.8', '36.5', '89.0'
    Sensor:
        "amsr2" (more to come..)
    Target resolution:
        '10', '25' (kms)
    Overpass:
        'day', 'night'


    #### Common Setup ####
    date:
        '2024-10-22', '2024-10-25', '2024-10-31'
    figpath:
        if defined, saves figs

    """
    # Configure the parameters here ====================================================================================
    # Airborne (AMPR) variables
    path_air = r"/home/ddkovacs/shares/climers/Projects/CCIplus_Soil_Moisture/07_data/WHYMSIE/data_from_RichDJ"
    air_freq = "10.7"
    flight_direction = "EW"
    scan_direction = "1_25"

    # Satellite (AMSR2) variables
    path_sat = r"/home/ddkovacs/shares/climers/Projects/CCIplus_Soil_Moisture/07_data/LPRM/passive_input/coarse_resolution/AMSR2"
    sat_freq = "10.7"
    sat_sensor = "amsr2"
    overpass = "day"
    target_res = "25"

    # Comomn variables
    date = "2024-10-22"
    figpath = "/home/ddkovacs/shares/climers/Projects/CCIplus_Soil_Moisture/07_data/WHYMSIE/figures/25km"

    # Which one to plot?
    plot_single = False
    plot_all = False
    plot_compound = True
    #  =================================================================================================================

    if plot_single:
        # Singular validation with plot
        validate_singular(
            path_air=path_air,
            scan_direction=scan_direction,
            flight_direction=flight_direction,
            air_freq=air_freq,
            sat_sensor=sat_sensor,
            path_sat=path_sat,
            sat_freq=sat_freq,
            overpass=overpass,
            target_res=target_res,
            date=date,
            fig_path=figpath,
        )

    if plot_all:
        # Validate all flights of ER-2 (in loop), parameters hard coded
        validate_all(path_air,
                     path_sat,
                     figpath)

    if plot_compound:
        validate_compound(
            path_air=path_air,
            air_freq=air_freq,
            sat_sensor=sat_sensor,
            path_sat=path_sat,
            sat_freq=sat_freq,
            overpass=overpass,
            target_res=target_res,
                          )
