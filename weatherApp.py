from datetime import date
import json
import requests
import calendar

# Global Variables
global place_of_search, forecast_type, input_year, input_month, input_day, delta_days
global search_place_geo_code
config_file_obj = open("config.json","r")
config_dict = json.load(config_file_obj)


# Fetching the GeoCodes from Google Map GeoCoding API
def get_dynamic_geoCode(place_of_search):
    # Need to use Google Maps GeoCoding API
    # Currently Not used in this Project to protect Privacy of my Gmail Account.
    pass


# Fetching the GeoCodes from Config.Json
def get_static_geoCode(place_of_search):
    try:
        geo_code = config_dict["geocodes"][place_of_search.lower()]
        return geo_code
    except Exception as e:
        print("Your Input city couldn't be found")
        print("Following are the currently supported cities")
        for x in config_dict["geocodes"].keys():
            print(x.capitalize())
        exit(-1)


# Fetching and validating Inputs from User
def get_and_validate_input():
    
    global place_of_search, search_place_geo_code, forecast_type, input_year, input_month, input_day, delta_days

    current_date = date.today()
    current_date_dmy_format = current_date.strftime("%d-%m-%Y")
    current_day, current_month, current_year = current_date_dmy_format.split("-")
    current_day = int(current_day)
    current_month = int(current_month)
    current_year = int(current_year)

    # Input and Validate the Place from the User
    place_of_search = input("Please Specify the Place : ")
    if len(place_of_search) == 0:
        print("Place cannot be an empty String")
        exit(-1)
    search_place_geo_code = get_static_geoCode(place_of_search)

    # Input forecast type from the user and based on forecast_type input the corresponding date from the user.
    input_type = input("Please Enter \n1 for Daily data [Default]\n2 for Monthly data\n3 for Hourly data\n")

    # For Daily Forecast
    if input_type == "1" or len(input_type) == 0:
        forecast_type = config_dict["forecast_type"]["1"]
        daily_input = input("Enter the date of search. Your date should be between current date and next 14 days. For info beyond 14 days, use Monthly Forecasting.\nBy Default Today's date will be considered.\nSpecify date in dd-mm-yyyy format :  ")
        try:
            if len(daily_input) == 0:
                input_day = current_day
                input_month = current_month
                input_year = current_year
                delta_days = 0
                return
            else:
                input_day, input_month, input_year = daily_input.split("-")        
        
            input_day = int(input_day)
            input_month = int(input_month)
            input_year = int(input_year)

            input_date = date(input_year, input_month, input_day)
            current_date = date(current_year, current_month, current_day)

            delta = input_date - current_date
            delta_days = delta.days

            if delta_days < 0:
                print("Your Input date should be more than current date.")
                exit(-1)
            if delta_days > 14:
                print("Your date exceeds the current date by more than 14 days. Please use monthly forecast for your Query.\n")
                exit(-1)

        except Exception as e:
            print("Exception Obtained : ", e)
            print("Please Enter a valid date")
            exit(-1)

    # For Monthly Forecast
    elif input_type == "2":
        forecast_type = config_dict["forecast_type"]["2"]
        monthly_input = input("Enter month and year of search. Your input should be between current month to previous month of next year. \nSpecify the month and year in mm-yyyy format : ")
        try:
            input_month, input_year = monthly_input.split("-")
            input_month = int(input_month)
            input_year = int(input_year)

            if input_month < 1 or input_month > 12:
                print("Exception Obtained Here")
                print("Please Enter Valid Month Value. It should be between 1 and 12.")
                exit(-1)
            if (input_year==current_year and input_month>=current_month) or (input_year==current_year+1 and input_month<current_month):
                print("Arguments are Proper")
            else:
                print("Please Specifiy the month and Year in Proper Range.")
                exit(-1)

        except Exception as e:
            print("Exception Obtained : ", e)
            print("Please Enter a valid date")
            exit(-1)

    # For Hourly Forecast
    elif input_type == "3":
        print("Currently this functionality is Not Supported.")
        exit(0)

    else:
        print("You have entered an invalid input")
        exit(-1)


# Fetching Data from the Weather.com API
def get_weather_data():
    global place_of_search, search_place_geo_code, forecast_type, input_year, input_month, input_day, delta_days

    if forecast_type == config_dict["forecast_type"]["1"]:
        URL = config_dict["Daily_forecast"]["URL"]
        PARAMS = config_dict["Daily_forecast"]["params"]
        PARAMS["geocode"] = search_place_geo_code
        
        response_obj = requests.get(url = URL, params = PARAMS)
        response_data = response_obj.json()

        print("-------------- Output -------------------")
        print("Sun Rise at                               :     " + str(response_data["vt1dailyForecast"]["sunrise"][delta_days]))
        print("Sun Set at                                :     " + str(response_data["vt1dailyForecast"]["sunset"][delta_days]))
        print("Moon Rise at                              :     " + str(response_data["vt1dailyForecast"]["moonrise"][delta_days]))
        print("Moon Set at                               :     " + str(response_data["vt1dailyForecast"]["moonset"][delta_days]))

        print("--- During Day ---")
        print("Temperature                               :     " + str(response_data["vt1dailyForecast"]["day"]["temperature"][delta_days]))
        print("Humidity Percentage                       :     " + str(response_data["vt1dailyForecast"]["day"]["humidityPct"][delta_days]))
        print("Precipitation Amount                      :     " + str(response_data["vt1dailyForecast"]["day"]["precipAmt"][delta_days]))
        print("Precipitaion Type                         :     " + str(response_data["vt1dailyForecast"]["day"]["precipType"][delta_days]))
        print("Wind Direction                            :     " + str(response_data["vt1dailyForecast"]["day"]["windDirCompass"][delta_days]))
        print("Wind Speed                                :     " + str(response_data["vt1dailyForecast"]["day"]["windSpeed"][delta_days]) + "Km/h")
        print("Short Description of the Day              :     " + str(response_data["vt1dailyForecast"]["day"]["narrative"][delta_days]))

        print("--- During Night ---")
        print("Temperature                               :     " + str(response_data["vt1dailyForecast"]["night"]["temperature"][delta_days]))
        print("Humidity Percentage                       :     " + str(response_data["vt1dailyForecast"]["night"]["humidityPct"][delta_days]))
        print("Precipitation Amount                      :     " + str(response_data["vt1dailyForecast"]["night"]["precipAmt"][delta_days]))
        print("Precipitaion Type                         :     " + str(response_data["vt1dailyForecast"]["night"]["precipType"][delta_days]))
        print("Wind Direction                            :     " + str(response_data["vt1dailyForecast"]["night"]["windDirCompass"][delta_days]))
        print("Wind Speed                                :     " + str(response_data["vt1dailyForecast"]["night"]["windSpeed"][delta_days]) + "Km/h")
        print("Short Description of the night            :     " + str(response_data["vt1dailyForecast"]["night"]["narrative"][delta_days]))


    elif forecast_type == config_dict["forecast_type"]["2"]:
        latitude, longitude = search_place_geo_code.split(",")
        URL = "https://api.weather.com/v1/geocode/" + latitude + "/" + longitude + "/almanac/daily.json"    
        PARAMS = config_dict["Monthly_forecast"]["params"]

        last_day_of_month = str(calendar.monthrange(input_year,input_month)[1])

        input_month = str(input_month)
        if len(input_month) == 1:
            input_month = "0" + input_month

        PARAMS["start"] = input_month + "01" 
        PARAMS["end"] = input_month + last_day_of_month

        response_obj = requests.get(url = URL, params = PARAMS)
        response_data = response_obj.json()
        
        print("-------------- Output -------------------")
        for x in response_data["almanac_summaries"]:
            print("Date                            :       " + x["almanac_dt"][2:] + "-" + x["almanac_dt"][:2])
            print("Average High Temperature        :       " + str(x["avg_hi"]))
            print("Average Low Temperature         :       " + str(x["avg_lo"]))
            print("Mean Temperature                :       " + str(x["mean_temp"]))

            print("----------------------------------------------------------")


# Driver Program    
def main():
    global place_of_search, forecast_type, input_year, input_month, input_day, delta_days

    # Fetching and Validating User Inputs
    get_and_validate_input()
    
    # Displaying User Inputs
    print("-------------- Your Inputs --------------")
    print("Place           :      " + place_of_search.capitalize())
    print("Forecast Type   :      " + forecast_type)
    print("Year of Search  :      " + str(input_year))
    print("Month of Search :      " + str(input_month))

    if forecast_type == config_dict["forecast_type"]["1"]:
        print("Day of Search   :      " + str(input_day))

    # Fetching and Displaying Response Data based on type of Request
    get_weather_data()


main()