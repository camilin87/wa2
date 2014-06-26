import forecastio

api_key = "151cfe4d4aed6cd467097090a9250dab"
lat = 25.57
lng = -80.35

forecast = forecastio.load_forecast(api_key, lat, lng)
print(str(forecast))

# class A(object):
#     pass
# print(A())
