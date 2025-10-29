import numpy as np
from sklearn.neighbors import BallTree
import pandas as pd
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

def nn_loc_search(df1,
                  df2):
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
    disances, ids: smallest distances between points in df1 and df2 and its index
    """

    df1 = to_radians(df1)
    df2 = to_radians(df2)

    radius_earth = 6371 # km
    ball = BallTree(df1[["rad_lat", "rad_lon"]].values, metric='haversine')
    distances, indices = ball.query(df2[["rad_lat", "rad_lon"]].values, k=1)

    distances = distances * radius_earth

    return distances, indices



