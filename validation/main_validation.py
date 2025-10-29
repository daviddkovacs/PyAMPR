from validation.ER2_Flight import FlightData
from validation.AMSR2_Observations import SatelliteData
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
                        air_f=a_f,
                        sat_f=s_f,
                        date=d,
                        fig_path=figpath,
                        show_fig = False
                    )


def validate_singular(path_air,
                         path_sat,
                         scan_direction,
                         flight_direction,
                         air_f,
                         sat_f,
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
    ER2_flight = FlightData(path=path_air,
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
                air_f,
                sat_f,
                date)

    Figs.longitude_plot(savedir = fig_path,
                        flight_direction = flight_direction,
                        scan_direction = scan_direction,
                        show_fig = show_fig)

    Figs.scatter_plot(savedir = fig_path,
                        flight_direction = flight_direction,
                        scan_direction = scan_direction,
                      show_fig=show_fig)

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

    # validate_singular(
    #     path_air = path_ampr,
    #     path_sat=path_amsr,
    #     scan_direction=scan_direction,
    #     flight_direction=flight_direction,
    #     air_f =AMPR_f,
    #     sat_f=AMSR2_f,
    #     date=date,
    #     fig_path=figpath,
    # )

    validate_all(path_ampr, path_amsr, figpath)
