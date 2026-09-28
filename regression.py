import matplotlib.pyplot as pyplot
import pandas as pd

data = pd.read_csv("wifi_dataset.csv")
x = data["rssi_dbm"]
y = data["download_mbps"]

def mean(values):
    return sum(values) / float(len(values))

def variance(values, mean):
    return sum([(x - mean)**2 for x in values])

def covariance(x, mean_x, y, mean_y):
    covar = 0.0
    for i in range(len(x)):
        covar += (x[i] - mean_x) * (y[i] - mean_y)
    return covar

def coefficients(x, y):
    x_mean, y_mean = mean(x), mean(y)
    b1 = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
    b0 = y_mean - b1 * x_mean
    return [b0, b1]

b0, b1 = coefficients(x, y)
print(f"coefficients: b0: {b0} b1: {b1}")
