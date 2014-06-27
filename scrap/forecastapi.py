import forecastio
import datetime
from datetime import datetime


def main():
    api_key = "151cfe4d4aed6cd467097090a9250dab"
    # zipcode 33012
    # 323|25.86|-80.3|25.86,-80.3|25.86%2C-80.3|-5|1
    lat = 25.86
    lng = -80.30
    time = datetime.now().replace(minute=0, second=0, microsecond=0)

    forecast = forecastio.load_forecast(api_key, lat, lng)

    # print(forecast.hourly().data[0].temperature)
    # print("===========Hourly Data=========")
    # by_hour = forecast.hourly()
    # print("Hourly Summary: %s" % (by_hour.summary))

    # for hourly_data_point in by_hour.data:
    #     print(hourly_data_point)

    # print("===========Daily Data=========")
    # by_day = forecast.daily()
    # print("Daily Summary: %s" % (by_day.summary))

    # for daily_data_point in by_day.data:
    #     print(daily_data_point)

    print("=========Current Data=========")
    datapoint = forecast.currently()
    for k, v in datapoint.__dict__["d"].items():
        print(str(k).rjust(20), " => ", v)

if __name__ == "__main__":
    main()
