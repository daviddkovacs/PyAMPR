import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import root_mean_squared_error
from sklearn.neighbors import BallTree
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None

def to_radians(df,
               lat = "lat",
               lon = "lon"):
    """

    Parameters
    ----------
    df: pandas dataframe with lat, lon columns as degrees
    lat: name of the latitude column. Default is 'lat'
    lon: name of the longitude column. Default is 'lon'

    Returns
    -------
    df: pandas dataframe with lat, lon columns as radians
    """

    df.loc[:, f"rad_{lat}"] = np.deg2rad(df[lat].values)
    df.loc[:, f"rad_{lon}"] = np.deg2rad(df[lon].values)

    return df


def filter_distance(distance_df,
                    radius = 10):
    """

    Parameters
    ----------
    distance_df: pandas dataframe with nearest distances and ids
    radius: threshold radius for nearest distances. Default is 10

    Returns
    -------
    radius_df: pandas dataframe with nearest distances filtered
    """

    radius_df = distance_df[distance_df["distance"]<radius]

    return radius_df

def nn_loc_search(df1,
                  df2,
                  ):
    """

    Parameters
    ----------
    df1: dataframe to construct BallTree with: the dataset to "search" from
    df2: dataframe to query: the dataset to "reference" from

    Ball Tree NN search (https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.BallTree.html)

    df2 will be the query/reference points, the coords in df1 will be searched against it
    Only works with radians! using the Haversine formula to calculate the distance.

    Returns
    -------
    df_dist_ids: df containing nn dist between df1 and df2, the ids where this happens in df1, and df2 original ids
    """

    df1 = to_radians(df1)
    df2 = to_radians(df2)

    ball = BallTree(df1[["rad_lat", "rad_lon"]].values, metric='haversine')
    distances, indices_nn = ball.query(df2[["rad_lat", "rad_lon"]].values, k=1)

    radius_earth = 6371 # km
    distances = distances.ravel() * radius_earth
    indices_nn = indices_nn.ravel()
    index_ref = df2.index

    df_dist_ids = pd.DataFrame({"distance": distances,"index_nn": indices_nn, "index_ref": index_ref})

    return df_dist_ids


def mpdi(v_freq,
         h_freq):
    """

    Parameters
    ----------
    v_freq: vertical polarized brightness temperature
    h_freq: horizontal polarized brightness temperature

    Returns
    -------
    mpdi: Microwave Polarisation Difference Index
    """

    mpdi = (v_freq-h_freq) / (v_freq + h_freq)

    return mpdi


def statistics(air_mpdi,
               sat_mpdi,):

    r = pd.Series(air_mpdi).corr(pd.Series(sat_mpdi))
    rmse = np.sqrt(np.mean((sat_mpdi-air_mpdi)**2))
    bias = np.mean(air_mpdi) -np.mean(sat_mpdi)
    stats_dict = {"r": np.round(r,2),
                  "rmse": np.round(rmse,3),
                  "bias": np.round(bias,3),}

    return stats_dict


def longitude_combined_plot(air_mpdi,
                            sat_mpdi,
                            air_freq,
                            sat_freq,
                            date,
                   ):

    air_mpdi_array = air_mpdi[f"MPDI {air_freq}"]
    sat_mpdi_array = sat_mpdi[f"MPDI {sat_freq}"]

    stats_dict = statistics(air_mpdi_array,sat_mpdi_array)

    plt.figure(figsize=(8, 4))

    plt.plot(air_mpdi["lon"], air_mpdi_array, label=f"AMPR {air_freq} GHz", color="tab:blue")
    plt.plot(sat_mpdi["lon"], sat_mpdi_array, label=f"AMSR2 {sat_freq} GHz", color="tab:orange")

    plt.xlabel("Longitude")
    plt.ylabel(f"MPDI")
    plt.title(f"{date}\n"
              f"R: {stats_dict['r']}\n"
              f"RMSE: {stats_dict['rmse']}\n"
              f"Bias: {stats_dict['bias']}\n")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



