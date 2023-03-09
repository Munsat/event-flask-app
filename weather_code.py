def get_weather_info(weather_code):
    if weather_code == 0:
        return 'Clear sky'
    elif 1<=weather_code<=3:
       return 'Mainly clear, partly cloudy, and overcast' 
    elif weather_code==45 or weather_code==48:
        return 'Fog and depositing rime fog'
    elif weather_code==51 or weather_code==53 or weather_code==55:
        return 'Drizzle: Light, moderate, and dense intensity'
    elif weather_code==56 or weather_code==57:
        return 'Freezing Drizzle: Light and dense intensity'
    elif weather_code==61 or weather_code==63 or weather_code==65:
        return 'Rain: Slight, moderate and heavy intensity'
    elif weather_code==66 or weather_code==67: 
        return 'Freezing Rain: Light and heavy intensity'
    elif weather_code==71 or weather_code==73 or weather_code==75:
        return 'Snow fall: Slight, moderate, and heavy intensity'
    elif weather_code==77: 
        return 'Snow grains'
    elif 80<=weather_code<=82:
        return 'Rain showers: Slight, moderate, and violent'
    elif weather_code==85 or weather_code==86: 
        return 'Snow showers slight and heavy'
    elif weather_code==95: 
        return 'Thunderstorm: Slight or moderate'
    elif weather_code==96 or weather_code==99: 
        return 'Thunderstorm with slight and heavy hail'

