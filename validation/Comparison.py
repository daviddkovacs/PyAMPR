import matplotlib

from validation.ER2_Flight import AirborneData
from validation.Satellite_Observations import SatelliteData

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import pandas as pd
import numpy as np
import os

class CompareData:
    """
    Class to provide methods for comparison of sat and airborne MPDIs
    needs to be initiated with MPDIs as calulcated by collocate_mpdi(), AirborneData and SatelliteData instances
    """
    def __init__(self, air_mpdi, sat_mpdi, air_instance, sat_instance, *args):

        # MPDI dataframes
        self.air_mpdi = air_mpdi
        self.sat_mpdi = sat_mpdi

        # MPDI arrays
        self.air_mpdi_array_filtered = air_mpdi["filtered"][f"MPDI {air_instance.air_freq}"]
        self.air_mpdi_array_original = air_mpdi["original"][f"MPDI {air_instance.air_freq}"]
        self.sat_mpdi_array = sat_mpdi[f"MPDI {sat_instance.sat_freq}"]

        # Airborne specific variables
        self.air_freq = air_instance.air_freq
        self.flight_direction = air_instance.flight_direction
        self.scan_direction = air_instance.scan_direction

        # Satellite specific variables
        self.sat_sensor = sat_instance.sat_sensor
        self.overpass = sat_instance.overpass
        self.target_res = sat_instance.target_res
        self.sat_freq = sat_instance.sat_freq

        #Common variables
        self.date = air_instance.date


    def statistics(self,):

        r = pd.Series(self.air_mpdi_array_filtered).corr(pd.Series(self.sat_mpdi_array))
        rmse = np.sqrt(np.mean((self.sat_mpdi_array - self.air_mpdi_array_filtered) ** 2))
        bias = np.mean(self.air_mpdi_array_filtered) - np.mean(self.sat_mpdi_array)
        precision = np.round(np.sqrt(np.mean(
            (self.sat_mpdi_array - self.air_mpdi_array_filtered - np.mean(self.sat_mpdi_array - self.air_mpdi_array_filtered)) ** 2)),
                 2)

        stats_dict = {"r": np.round(r, 2),
                      "rmse": np.round(rmse, 3),
                      "bias": np.round(bias, 3),
                      "precision" : np.round(precision, 3),
                      "N": len(self.air_mpdi_array_filtered)}

        return stats_dict


    def longitude_plot(self,
                       savedir = None,
                       show_fig = True
                       ):

        stats_dict = self.statistics()

        plt.figure(figsize=(8, 4))

        plt.plot(self.air_mpdi["original"]["lon"],
                 self.air_mpdi_array_original,
                 label=f"AMPR {self.air_freq} GHz",
                 color="tab:blue")

        plt.plot(self.sat_mpdi["lon"],
                 self.sat_mpdi_array,
                 label=f"{self.sat_sensor} {self.target_res}km {self.sat_freq} GHz",
                 color="tab:orange")

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
                     savedir = None,
                     show_fig=True
                     ):

        stats_dict = self.statistics()
        stats_text = (f"R: {stats_dict['r']}\nRMSE: {stats_dict['rmse']}\n"
                      f"Bias: {stats_dict['bias']}\n"
                      f"Precision: {stats_dict['precision']}\n"
                      f"N: {stats_dict['N']}\n")

        x = self.air_mpdi_array_filtered
        y = self.sat_mpdi_array

        min_val =0
        max_val = 0.08

        mask = np.isfinite(x) & np.isfinite(y)
        x = x[mask]
        y = y[mask]

        xy = np.vstack([x, y])
        z = gaussian_kde(xy)(xy)

        plt.figure(figsize=(6, 6))

        plt.scatter(x, y, c=z, s=20, cmap='viridis', )

        plt.plot([min_val, max_val], [min_val, max_val], 'k-', lw=1,)

        plt.text(0.05, 0.95, stats_text, transform=plt.gca().transAxes,
                 verticalalignment='top', horizontalalignment='left', fontsize=14)

        plt.xlabel(f"AMPR MPDI {self.air_freq} GHz")
        plt.ylabel(f"AMSR2 MPDI {self.sat_freq} GHz")
        plt.title(f"{self.date} {self.flight_direction} {self.scan_direction}")
        plt.grid(False)
        plt.xlim([min_val, max_val])
        plt.ylim([min_val,max_val])
        plt.tight_layout()
        if savedir:
            plt.savefig(os.path.join(savedir,rf"{self.date}_{self.flight_direction}_{self.scan_direction}_{self.air_freq}_scatter.png"))
        if show_fig:
            plt.show()