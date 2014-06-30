import forecastio
import datetime
from datetime import datetime


def call_api(lat, lng):
    padding = 30
    api_key = "151cfe4d4aed6cd467097090a9250dab"

    forecast = forecastio.load_forecast(api_key, lat, lng)

    print("\n=========Current Data=========", lat, ", ", lng)
    datapoint = forecast.currently()

    for k, v in datapoint.__dict__.items():
        if k != "d":
            print(k.rjust(padding), " => ", v)

    print("========Data inside d=========")
    dict_data = datapoint.__dict__["d"]
    for k in sorted(dict_data):
        print(str(k).rjust(padding), " => ", dict_data[k])

    print("======Data read directly======")
    print((datapoint.summary.__class__.__name__ + " summary => ").rjust(padding), datapoint.summary)
    print(
        (datapoint.precipIntensity.__class__.__name__ + " precipIntensity => ").rjust(padding),
        datapoint.precipIntensity
    )
    print(
        (datapoint.precipProbability.__class__.__name__ + " precipProbability => ").rjust(padding),
        datapoint.precipProbability
    )


def main():
    # 33012 hialeah
    call_api(25.86, -80.30)

    # 90045 LAX
    call_api(33.96, -118.39)

if __name__ == "__main__":
    main()
