from validation.ER2_Flight import AirborneData
from validation.Satellite_Observations import SatelliteData
from validation.Comparison import CompareData
from utils import collocate_mpdi


def validate_all(path_ampr,
                 path_amsr,
                 figpath):

    datelist = ["2024-10-22","2024-10-25", "2024-10-31"]
    flight_direction_list = ["WE","EW"]
    scan_direction_list = ["1_25","26_50"]
    AMPR_f_list = ["10.7", "19.35", "37.1"]
    AMSR2_f_list = ["10.7", "18.7", "36.5"]

    for d in datelist:
        for f in flight_direction_list:
            for s in scan_direction_list:
                for a_f, s_f in zip(AMPR_f_list, AMSR2_f_list):
                    print(f"{d} {f} {s}")
                    validate_singular(
                        path_air=path_ampr,
                        path_sat=path_amsr,
                        scan_direction=s,
                        flight_direction=f,
                        air_freq=a_f,
                        sat_freq=s_f,
                        date=d,
                        fig_path=figpath,
                        show_fig = False
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
                      fig_path = None,
                      show_fig = True):
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
                              air_freq= air_freq,
                              )

    AMSR2_OBS = SatelliteData(path=path_sat,
                              sat_sensor=sat_sensor,
                              date=date,
                              overpass=overpass,
                              target_res=target_res,
                              sat_freq= sat_freq,
                              )

    air_mpdi, sat_mpdi = collocate_mpdi(ER2_flight, AMSR2_OBS,)

    Figs = CompareData(air_mpdi,
                       sat_mpdi,
                       ER2_flight,
                       AMSR2_OBS)

    Figs.longitude_plot(savedir = fig_path,
                        show_fig = show_fig)

    Figs.scatter_plot(savedir = fig_path,
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
    # Airborne (AMPR) variables
    path_air = r"/home/ddkovacs/shares/climers/Projects/CCIplus_Soil_Moisture/07_data/WHYMSIE/data_from_RichDJ"
    air_freq = "10.7"
    flight_direction = "EW"
    scan_direction = "1_25"

    # Satellite (AMSR2) variables
    path_sat = r"/home/ddkovacs/shares/climers/Projects/CCIplus_Soil_Moisture/07_data/LPRM/passive_input/coarse_resolution/AMSR2"
    sat_freq = "10.7"
    sat_sensor = "amsr2"
    overpass = "night"
    target_res = "25"

    # Comomn variables
    date = "2024-10-25"
    figpath = None

    # Singular validation with plot
    validate_singular(
        path_air = path_air,
        scan_direction=scan_direction,
        flight_direction=flight_direction,
        air_freq =air_freq,
        sat_sensor=sat_sensor,
        path_sat=path_sat,
        sat_freq=sat_freq,
        overpass=overpass,
        target_res=target_res,
        date=date,
        fig_path=figpath,
    )

    # Validate all flights of ER-2 (in loop), parameters hard coded
    # validate_all(path_ampr, path_amsr, figpath)
