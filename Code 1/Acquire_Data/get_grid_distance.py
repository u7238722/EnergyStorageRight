import pandas as pd
from math import sin, cos, sqrt, atan2, radians

# Read the map information
df=pd.read_csv('Energy Grid Data.csv', sep=',',header=None)
my_data=df.values

# This function is used to calculate the distance of two points in the map
# The input is the latitude and longitude of the point, and the output is distance (km)
def distance(arr1, arr2):

    R = 6373.0  # approximate radius of earth in km

    lat1 = radians(arr1[0])
    lon1 = radians(arr1[1])
    lat2 = radians(arr2[0])
    lon2 = radians(arr2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

# Among several points, find out the smallest distance
def findcloestpoint(x,y):
    data=my_data
    dist=100000
    value=0
    for i in range(len(data)):
        cdist=distance([x,y],data[i][1:3])
        if cdist<dist:
            dist=cdist
            value=data[i][3]
    return value
