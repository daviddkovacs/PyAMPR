import os.path
import rioxarray
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pyampr
import xarray as xr
import pandas as pd
import os
import geopy

class Satellite:
    def __init__(self,
                 path,
                 date,
                 )