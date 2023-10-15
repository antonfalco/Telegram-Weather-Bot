# %%
from datetime import datetime
import requests
import telebot

#name: GlobalWeather. username: OntarioWeather3Bot
ONTARIO_BOT_API_KEY = '[YOUR KEY HERE]'
bot = telebot.TeleBot(ONTARIO_BOT_API_KEY)
NEW_WEATHER_API_KEY = '[YOUR OTHER KEY HERE]'


#MAKING SURE MESSAGE LENGTH STAYS UNDER 4096 MAX CHARACTER LIMIT. IF EXCEEDED, SPLIT

def send_message_with_length_check(chat_id, message_text):
    max_message_length = 4096 

    if len(message_text) <= max_message_length:
        bot.send_message(chat_id, message_text)
    else:
        parts = [message_text[i:i + max_message_length] for i in range(0, len(message_text), max_message_length)]
        for part in parts:
            bot.send_message(chat_id, part)
            


@bot.message_handler(commands=['current', 'forecast', 'hour', 'help'])      #example:  /current Hamilton, CA   &  /forecast Hamilton, CA for 3 Day   &   /hour Hamilton, CA    &    /help Hamilton, CA
def send_api_info(message):
    command, user_input = message.text.split(' ', 1) 
    
    #CURRENT CITY CONDITIONS
    try:
        if command == '/current':     
            CURRENT_WEATHER_API = requests.get(f"https://api.weatherapi.com/v1/current.json?key={NEW_WEATHER_API_KEY}&q={user_input}&aqi=yes").json()
            last_updated = CURRENT_WEATHER_API['current']['last_updated']
            current_temp_c = CURRENT_WEATHER_API['current']['temp_c']
            current_temp_f = CURRENT_WEATHER_API['current']['temp_f']
            humidity = CURRENT_WEATHER_API['current']['humidity']
            feels_like_now_c = CURRENT_WEATHER_API['current']['feelslike_c']
            feels_like_now_f = CURRENT_WEATHER_API['current']['feelslike_f']
            current_condition = CURRENT_WEATHER_API['current']['condition']['text']
            current_condition_icon = CURRENT_WEATHER_API['current']['condition']['icon']
            wind_speed_km = CURRENT_WEATHER_API['current']['wind_kph']
            wind_speed_mph = CURRENT_WEATHER_API['current']['wind_mph']
            wind_gusts_kph = CURRENT_WEATHER_API['current']['gust_kph']
            wind_gusts_mph = CURRENT_WEATHER_API['current']['gust_mph']
            wind_degree = CURRENT_WEATHER_API['current']['wind_degree']
            wind_direction = CURRENT_WEATHER_API['current']['wind_dir']
            pressure_mb = CURRENT_WEATHER_API['current']['pressure_mb']
            precipitation_mm = CURRENT_WEATHER_API['current']['precip_mm']
            precipitation_in = CURRENT_WEATHER_API['current']['precip_in']
            clouds = CURRENT_WEATHER_API['current']['cloud']
            uv_index = CURRENT_WEATHER_API['current']['uv']
            air_quality = CURRENT_WEATHER_API['current']['air_quality']['us-epa-index']

            #For Telegram
            current_info = f"Last Updated: {last_updated} \n\n" \
                        f"Current Temp: {current_temp_c}°C or {current_temp_f}°F \n" \
                        f"Humidity: {humidity}% \n" \
                        f"Feels Like: {feels_like_now_c}°C or {feels_like_now_f}°F \n" \
                        f"Current Condition: {current_condition} \n"\
                        f"Wind Speed: {wind_speed_km} km/h or {wind_speed_mph} mph \n" \
                        f"Max Gusts: {wind_gusts_kph} km/h or {wind_gusts_mph} mph \n" \
                        f"Wind Direction: {wind_degree}° or {wind_direction} \n"  \
                        f"Barometric Pressure: {pressure_mb:.0f} mb \n" \
                        f"Precipitation: {precipitation_mm} mm or {precipitation_in} in \n" \
                        f"Cloud Cover: {clouds}% \n\n" \
                        f"UV Index: {uv_index}. \n[Legend: 0 = Low Risk. 10 = High Risk] \n\n" \
                        f"Air Quality Index: {air_quality}. \nLegend: [1 = Good. 3 = Moderate. 5+ = Very Poor]\n\n" \
                        
            #Alerts
            FORECAST_WEATHER_API = requests.get(f"https://api.weatherapi.com/v1/forecast.json?key={NEW_WEATHER_API_KEY}&q={user_input}&days=3&aqi=yes&alerts=yes").json()
            alerts = FORECAST_WEATHER_API.get('alerts', {}).get('alert', [])

            if alerts:
                alert_info_list = ["Active Alerts:\n"]

                for alert in alerts:
                    event_title = alert['event']
                    headline = alert['headline']
                    severity = alert['severity']
                    certainty = alert['certainty']
                    time_effective = alert['effective']
                    time_expires = alert['expires']
                    alert_description = alert['desc']
                    key_instruction = alert['instruction']

                    alert_info = f"Headline: {headline}\n\n" \
                                 f"Certainty: {certainty}\n" \
                                 f"Severity: {severity}\n\n" \
                                 f"Effective Time: {time_effective}\n" \
                                 f"Expiration Time: {time_expires}\n\n" \
                                 f"Description: {alert_description}\n\n" \
                                 #f"Instruction: {key_instruction}\n\n" \
                                 #f"Event: {event_title}\n" \

                    alert_info_list.append(alert_info)

                alert_info = "\n".join(alert_info_list)
                send_message_with_length_check(message.chat.id, current_info + alert_info)
            
            else:
                send_message_with_length_check(message.chat.id, current_info + "\nNo Active Alerts.")
                                      
                
    
        #FIVE DAY FORECAST
    
        elif command == '/forecast':    
            FORECAST_WEATHER_API = requests.get(f"https://api.weatherapi.com/v1/forecast.json?key={NEW_WEATHER_API_KEY}&q={user_input}&days=3&aqi=yes&alerts=yes").json()  

            forecast_info_list = []

            for forecast_day in FORECAST_WEATHER_API['forecast']['forecastday']:
                #Day
                date = forecast_day['date'] 
                max_temp_c = forecast_day['day']['maxtemp_c']
                max_temp_f = forecast_day['day']['maxtemp_f']
                min_temp_c = forecast_day['day']['mintemp_c']
                min_temp_f = forecast_day['day']['mintemp_f']
                avg_humidity_day = forecast_day['day']['avghumidity']
                max_wind_mph = forecast_day['day']['maxwind_mph']
                max_wind_kph = forecast_day['day']['maxwind_kph']
                total_mm = forecast_day['day']['totalprecip_mm']
                total_in = forecast_day['day']['totalprecip_in']
                visibility_km = forecast_day['day']['avgvis_km']
                visibility_mi = forecast_day['day']['avgvis_miles']
                will_it_rain =  forecast_day['day']['daily_chance_of_rain']
                general_text = forecast_day['day']['condition']['text']
                general_icon = forecast_day['day']['condition']['icon']
                forecast_uv_index = forecast_day['day']['uv']
                #us_forecast_aqi_index = forecast_day['day']['air_quality'].get('us-epa-index', 'N/A')
                #gb_forecast_aqi_index = forecast_day['day']['air_quality'].get('gb-defra-index', 'GB Cities Only')

                #Astro
                sunrise_time = forecast_day['astro']['sunrise']
                sunset_time = forecast_day['astro']['sunset']
                moonrise_time = forecast_day['astro']['moonrise']
                moonset_time = forecast_day['astro']['moonset']
                moonset_bright = forecast_day['astro']['moon_illumination']
                moon_phase_stage = forecast_day['astro']['moon_phase']

                #Tides
                #time_of_tides = forecast_day['tide']['tide_time']
                #tide_height = forecast_day['tide']['tide_height_mt']
                #tide_low_high = forecast_day['tide']['tide_type']

                #For Telegram
                day_info = f"Forecast for {date}:\n\n" \
                                f"Max Temperature: {max_temp_c}°C or {max_temp_f}°F\n" \
                                f"Min Temperature: {min_temp_c}°C or {min_temp_f}°F\n" \
                                f"Average Humidity: {avg_humidity_day}%\n" \
                                f"Max Wind: {max_wind_kph} km/h or {max_wind_mph} mph\n" \
                                f"Probability of Precipitation: {will_it_rain}%\n" \
                                f"Precip Expected: {total_mm} mm or {total_in} in\n" \
                                f"Visibility: {visibility_km} kms or {visibility_mi} miles\n"\
                                f"Expected Conditions: {general_text}\n" \
                                f"Highest Expected UV Index: {forecast_uv_index}.\n[Legend: Low Risk = 0. High Risk = 10]\n\n"\
                                f"Sun & Moon:\n\n"\
                                f"Sunrise: {sunrise_time}\n"\
                                f"Sunset: {sunset_time}\n"\
                                f"Moonrise: {moonrise_time}\n"\
                                f"Moonset: {moonset_time}\n"\
                                f"Moon Phase: {moon_phase_stage}\n" \
                                f"Moon Illumination: {moonset_bright}%\n\n"\
                                #f"Air Quality Index: {us_forecast_aqi_index}. \n[Legend: Good = 1. Moderate = 3. Very Poor = 5+]\n\n" \


                forecast_info_list.append(day_info)

            forecast_info = "\n".join(forecast_info_list)

            bot.reply_to(message, forecast_info)    
    
    
    
        #HOURLY CONDITIONS
    
        elif command == '/hour':    
            FORECAST_WEATHER_API = requests.get(f"https://api.weatherapi.com/v1/forecast.json?key={NEW_WEATHER_API_KEY}&q={user_input}&days=3&aqi=yes&alerts=yes").json()
                        
            #TO START AT CURRENT TIME
            current_time_str = FORECAST_WEATHER_API['location']['localtime']
            current_time = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M')
            
            hour_info_list = []
            hours_displayed = 0

            for forecast_day in FORECAST_WEATHER_API['forecast']['forecastday']:
                #date_day = forecast_day['date']

                for forecast_hour in forecast_day['hour']:
                    #Hour
                    time = forecast_hour['time'] 
                    time_temp_c = forecast_hour['temp_c']
                    time_temp_f = forecast_hour['temp_f']
                    dew_point_c = forecast_hour['dewpoint_c']
                    dew_point_f = forecast_hour['dewpoint_f']
                    humidity_hour = forecast_hour['humidity']
                    feels_like_c = forecast_hour['feelslike_c']
                    feels_like_f = forecast_hour['feelslike_f']
                    #heat_index_c = forecast_hour['heatindex_c']
                    #heat_index_f = forecast_hour['heatindex_f']
                    #wind_chill_c = forecast_hour['windchill_c']
                    #wind_chill_f = forecast_hour['windchill_f']
                    time_wind_mph = forecast_hour['wind_mph']
                    time_wind_kph = forecast_hour['wind_kph']
                    gusts_kph = forecast_hour['gust_kph']
                    gusts_mph = forecast_hour['gust_mph']
                    wind_degrees = forecast_hour['wind_degree']
                    wind_direction = forecast_hour['wind_dir']
                    baro_pressure_mb = forecast_hour['pressure_mb']
                    precip_hour_mm = forecast_hour['precip_mm']
                    precip_hour_in = forecast_hour['precip_in']
                    visibility_km_hr = forecast_hour['vis_km']
                    visibility_mi_hr = forecast_hour['vis_miles']
                    cloud_cover = forecast_hour['cloud']
                    will_it_rain =  forecast_hour['chance_of_rain']
                    #will_it_snow =  forecast_hour['chance_of_snow']
                    general_text = forecast_hour['condition']['text']
                    general_icon = forecast_hour['condition']['icon']
                    forecast_uv_index_hr = forecast_hour['uv']
                    #us_forecast_aqi_index = forecast_day['day']['air_quality']['us-epa-index']   #.get('us-epa-index', 'N/A')

                    forecast_time = datetime.strptime(time, '%Y-%m-%d %H:%M')

                    #For Telegram
                    if forecast_time >= current_time:
                        hourly_info = f"Forecast for {time}:\n\n" \
                                    f"Temperature: {time_temp_c}°C or {time_temp_f}°F\n"\
                                    f"Humidity: {humidity_hour}%\n"\
                                    f"Feels Like: {feels_like_c}°C / {feels_like_f}°F\n"\
                                    f"Wind Speed: {time_wind_kph} km/h or {time_wind_mph} mph\n"\
                                    f"Max Gusts: {gusts_kph} km/h or {gusts_mph} mph\n"\
                                    f"Wind Direction: {wind_degrees}° or {wind_direction}\n"\
                                    f"Cloud Coverage: {cloud_cover}%\n"\
                                    f"Probability of Rain: {will_it_rain}%\n"\
                                    f"Rain Expected: {precip_hour_mm} mm or {precip_hour_in} in\n"\
                                    f"Expected Conditions: {general_text}\n"\
                                    f"UV Index: {forecast_uv_index_hr}.\n[Legend: Low Risk = 0. High Risk = 10]\n\n"\
                                    #f"Air Quality Index: {us_forecast_aqi_index}. \n[Legend: Good = 1. Moderate = 3. Very Poor = 5+]\n\n" \
                                    #f"Dew Point: {dew_point_c}°C / {dew_point_f}°F\n"\        
                                    #f"Barometric Pressure: {baro_pressure_mb} mb\n"\
                                    #f"Visibility: {visibility_km_hr} kms or {visibility_mi_hr} miles\n" \
                                    #f"Will it Rain?: {chance_of_rain}%\n"\
                                    #f"Will it Snow?: {chance_of_snow}%\n"\

                        hour_info_list.append(hourly_info)
                        hours_displayed += 1

                        if hours_displayed >= 6:
                            break
                        
                if hours_displayed >= 6:
                    break
                
                
            hour_info = "\n".join(hour_info_list)

            bot.reply_to(message, hour_info)  

        elif command == '/help':
            help_text = f"Here are the available commands:\n\n" \
                        "/current [city name here] - Get the current weather for your city.\n\n" \
                        "/forecast [city name here] - Get the 3-day weather forecast for your city.\n\n" \
                        "/hour [city name here] - Get the next 6 hour weather forecast for your city.\n\n" \
                        "/help - Show this help message."         

            bot.reply_to(message, help_text)
            
           
    except KeyError:
            bot.reply_to(message, "Sorry, city not found. Try adding a country, state or province after city name.")       
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            bot.reply_to(message, "An error has occurred. Please try again later.")
   
bot.polling()




# %%
