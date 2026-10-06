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
    b1 = covariance(x, x_mean, y, y_mean) / sum_squared_deviations(x, x_mean)
    b0 = y_mean - b1 * x_mean
    return [b0, b1]

def simple_linear_regression(x, y):
    predictions = list()
    b0, b1 = coefficients(x, y)
    for row in x:
        yhat = b0 + b1 * row
        predictions.append(yhat)
    return predictions

def predict(x, b0, b1):
    predictions = []

    for value in x:
        predictions.append(b0 + b1 * value)

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


def cli(b0, b1, x, y, predictions):
    print("WiFi Predictor")
    print(f"Samples:{len(x)}")
    print(f"RMSE: {rmse_metric(y, predictions):.2f} Mbps")
    print("\n type help for help")

    while True:
        command = input("\n> ").strip().split()

        if not command:
            continue

        if command[0] == "predict":

            if len(command) != 2:
                print("Usage: predict <rssi>")
                continue

            rssi = float(command[1])
            
            if rssi < min(x) or rssi > max(x):
                print("Warning: RSSI is outside the training data range.")


            prediction = b0 + b1 * rssi

            print(f"Predicted download speed: {prediction:.2f} Mbps")

        elif command[0] == "stats":
            print(f"Samples: {len(x)}")
            print(f"RSSI min: {min(x):.2f} dBm")
            print(f"RSSI max: {max(x):.2f} dBm")
            print(f"Download min: {min(y):.2f} Mbps")
            print(f"Download max: {max(y):.2f} Mbps")
            print(f"RMSE: {rmse_metric(y, predictions):.2f} Mbps")

        elif command[0] in ["quit", "exit"]:
            break

        elif command[0] == "help":

            print("predict <rssi>       Predict download speed")
            print("coefficients         Show b0 and b1")
            print("stats                Show dataset statistics")
            print("help                 Show commands")
            print("quit                 Exit")

        else:

            print("Unknown command. Type 'help'.")





b0, b1 = coefficients(x, y)
predictions = predict(x, b0, b1)

cli(b0, b1, x, y, predictions)
