import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import pandas as pd
import numpy as np
import os


def statistics(ref,test):

    r = pd.Series(ref).corr(pd.Series(test))
    rmse = np.sqrt(np.mean((test - ref) ** 2))
    bias = np.mean(ref) - np.mean(test)
    precision = np.round(np.sqrt(np.mean(
        (test - ref - np.mean(
            test - ref)) ** 2)),
        2)

    stats_dict = {"r": np.round(r, 2),
                  "rmse": np.round(rmse, 3),
                  "bias": np.round(bias, 3),
                  "precision": np.round(precision, 3),
                  "N": len(ref)}

    return stats_dict



class FigVarBase:


    def __init__(self, air_freq, flight_direction, scan_direction, sat_sensor, overpass, target_res, sat_freq, date):

        self.air_freq = air_freq
        self.flight_direction = flight_direction
        self.scan_direction = scan_direction
        self.sat_sensor = sat_sensor
        self.overpass = overpass
        self.target_res = target_res
        self.sat_freq = sat_freq
        self.date = date


    def longitude_plot(self,
                       ref_x,
                       ref_y,
                       test_x,
                       test_y,
                       savedir = None,
                       show_fig = True
                       ):

        stats_dict = statistics(ref_y,test_y)

        plt.figure(figsize=(8, 4))

        plt.plot(ref_x,
                 ref_y,
                 label=f"AMPR {self.air_freq} GHz",
                 color="tab:blue")

        plt.plot(test_x,
                 test_y,
                 label=f"{self.sat_sensor.upper()} {self.target_res}km {self.sat_freq} GHz",
                 color="tab:orange",
                 marker='x',
                 linestyle='',
                 markersize=6)

        plt.xlabel("Longitude")
        plt.ylabel(f"MPDI")
        plt.title(f"{self.date} {self.flight_direction} {self.scan_direction}\n"
                  f"R: {stats_dict['r']}\n"
                  f"RMSE: {stats_dict['rmse']}\n"
                  f"Bias: {stats_dict['bias']}\n"
                  )

        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        if savedir:
            plt.savefig(os.path.join(savedir,rf"{self.date}_{self.flight_direction}_{self.scan_direction}_{self.air_freq}_long.png"))
        if show_fig:
            plt.show()


    def scatter_plot(self,
                     ref,
                     test,
                     savedir=None,
                     show_fig=True
                     ):

        stats_dict = statistics(ref, test)

        stats_text = (f"R: {stats_dict['r']}\nRMSE: {stats_dict['rmse']}\n"
                      f"Bias: {stats_dict['bias']}\n"
                      f"Precision: {stats_dict['precision']}\n"
                      f"N: {stats_dict['N']}\n")

        min_val = 0
        max_val = 0.08

        mask = np.isfinite(ref) & np.isfinite(test)
        ref = ref[mask]
        test = test[mask]

        xy = np.vstack([ref, test])
        z = gaussian_kde(xy)(xy)

        plt.figure(figsize=(6, 6))

        plt.scatter(ref, test, c=z, s=20, cmap='viridis', )

        plt.plot([min_val, max_val], [min_val, max_val], 'k-', lw=1, )

        plt.text(0.05, 0.95, stats_text, transform=plt.gca().transAxes,
                 verticalalignment='top', horizontalalignment='left', fontsize=14)

        plt.xlabel(f"AMPR MPDI {self.air_freq} GHz")
        plt.ylabel(f"AMSR2 MPDI {self.sat_freq} GHz")
        plt.title(f"{self.date} {self.flight_direction} {self.scan_direction}")
        plt.grid(False)
        plt.xlim([min_val, max_val])
        plt.ylim([min_val, max_val])
        plt.tight_layout()
        if savedir:
            plt.savefig(os.path.join(savedir,
                                     rf"{self.date}_{self.flight_direction}_{self.scan_direction}_{self.air_freq}_scatter.png"))
        if show_fig:
            plt.show()


class FigVarSingular(FigVarBase):
    """
    Class to provide variable names for plots.
    needs to be initiated AirborneData and SatelliteData instances
    """
    def __init__(self, air_instance, sat_instance):

        # Airborne specific variables
        air_freq = air_instance.air_freq
        flight_direction = air_instance.flight_direction
        scan_direction = air_instance.scan_direction

        # Satellite specific variables
        sat_sensor = sat_instance.sat_sensor
        overpass = sat_instance.overpass
        target_res = sat_instance.target_res
        sat_freq = sat_instance.sat_freq

        #Common variables
        date = air_instance.date

        super().__init__(air_freq, flight_direction, scan_direction, sat_sensor, overpass, target_res, sat_freq, date)