import forecastio
import datetime
from datetime import datetime

def call_api(lat, lng):
    api_key = "151cfe4d4aed6cd467097090a9250dab"
    time = datetime.now().replace(minute=0, second=0, microsecond=0)

    # WARNING the time is not being used, thus the first API call is being made
    forecast = forecastio.load_forecast(api_key, lat, lng)

    print("\n=========Current Data=========", lat, ", ", lng)
    datapoint = forecast.currently()

    print("Time:", datapoint.time)

    for k, v in datapoint.__dict__.items():
        if k != "d":
            print(k, " => ", v)

    dict_data = datapoint.__dict__["d"]    
    for k in sorted(dict_data):
        print(str(k).rjust(20), " => ", dict_data[k])

def main():
    # 33012 hialeah
    call_api(25.86, -80.30)

    # 90045 LAX
    call_api(33.96, -118.39)

if __name__ == "__main__":
    main()
