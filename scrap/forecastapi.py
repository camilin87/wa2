import forecastio
import datetime


def main():
    api_key = "151cfe4d4aed6cd467097090a9250dab"
    lat = -31.967819
    lng = 115.87718

    forecast = forecastio.load_forecast(api_key, lat, lng)

    print(forecast.hourly().data[0].temperature)
    print("===========Hourly Data=========")
    by_hour = forecast.hourly()
    print("Hourly Summary: %s" % (by_hour.summary))

    for hourly_data_point in by_hour.data:
        print(hourly_data_point)

    print("===========Daily Data=========")
    by_day = forecast.daily()
    print("Daily Summary: %s" % (by_day.summary))

    for daily_data_point in by_day.data:
        print(daily_data_point)


if __name__ == "__main__":
    main()
