from main_validation import (
    validation_processor,
    path_amsr,
    path_ampr,
    figpath)



def validate_all(path_ampr,
                 path_amsr,
                 datelist,
                 flight_direction_list,
                 scan_direction_list,
                 AMPR_f_list,
                 AMSR2_f_list,
                 figpath,
                 show_fig
                 ):

    for d in datelist:
        for f in flight_direction_list:
            for s in scan_direction_list:
                for a_f, s_f in zip(AMPR_f_list, AMSR2_f_list):
                    validation_processor(
                        path_air=path_ampr,
                        path_sat=path_amsr,
                        scan_direction=s,
                        flight_direction=f,
                        air_f=a_f,
                        sat_f=s_f,
                        date=d,
                        fig_path=figpath,
                        show_fig = show_fig
                    )


if __name__ == '__main__':

    datelist = ["2024-10-22","2024-10-25", "2024-10-31"]
    flight_direction_list = ["WE","EW"]
    scan_direction_list = ["1_25","26_50"]
    AMPR_f_list = ["10.7", "19.35", "37.1"]
    AMSR2_f_list = ["10.7", "18.7", " 36.5"]

    validate_all(path_ampr,
                 path_amsr,
                 datelist,
                 flight_direction_list,
                 scan_direction_list,
                 AMPR_f_list,
                 AMSR2_f_list,
                 figpath,
                 show_fig = False)
