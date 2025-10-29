import numpy as np
from sklearn.neighbors import BallTree
import pandas as pd
pd.options.mode.chained_assignment = None

def to_radians(df,
               lat = "lat",
               lon = "lon"):

    df.loc[:, f"rad_{lat}"] = np.deg2rad(df[lat].values)
    df.loc[:, f"rad_{lon}"] = np.deg2rad(df[lon].values)

    return df

def nn_loc_search(df1,
                  df2):
    """
    Ball Tree NN search (https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.BallTree.html)

    df2 will be the query/reference points, the coords in df1 will be searched against it
    Only works with radians! using the Haversine formula to calculate the distance.
    """

    df1_rad = to_radians(df1)
    df2_rad = to_radians(df2)

    radius_earth = 6371 # km
    ball = BallTree(df1_rad[["rad_lat", "rad_lon"]].values, metric='haversine')
    distances, indices = ball.query(df2_rad[["rad_lat", "rad_lon"]].values, k=3)

    distances = distances * radius_earth

    return distances, indices



