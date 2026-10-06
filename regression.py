import pandas as pd
from math import sqrt

data = pd.read_csv("wifi_dataset.csv")
x = data["rssi_dbm"].tolist()
y = data["download_mbps"].tolist()

def mean(values):
    return sum(values) / float(len(values))

def sum_squared_deviations(values, mean):
    return sum([(x - mean)**2 for x in values])

def covariance(x, mean_x, y, mean_y):
    covar = 0.0
    for i in range(len(x)):
        covar += (x[i] - mean_x) * (y[i] - mean_y)
    return covar

def coefficients(x, y):
    x_mean, y_mean = mean(x), mean(y)
    b1 = covariance(x, x_mean, y, y_mean) / sum_squared_deviationse(x, x_mean)
    b0 = y_mean - b1 * x_mean
    return [b0, b1]

def simple_linear_regression(x, y):
    predictions = list()
    b0, b1 = coefficients(x, y)
    for row in x:
        yhat = b0 + b1 * row
        predictions.append(yhat)
    return predictions



def rmse_metric(actual, predicted):
    sum_error = 0.0
    for i in range(len(actual)):
        prediction_error = predicted[i] - actual[i]
        sum_error += (prediction_error ** 2)
    mean_error = sum_error / float(len(actual))
    return sqrt(mean_error)

def evaluate_algorithm(x, y, algorithm):
    predicted = algorithm(x, y)
    rmse = rmse_metric(y, predicted)
    return rmse


rmse = evaluate_algorithm(x, y, simple_linear_regression)
print(f"RMSE: {rmse}")
