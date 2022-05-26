import requests
import os
from datetime import datetime

GENDER = "Male"
WEIGHT_KG = 60
HEIGHT_CM = "5.6"
AGE = 25


APPLICATION_ID = os.environ.get("APP_ID")
NUTRITIONIX_API_KEY = os.environ.get("API_KEY")
USERNAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")
#TOKEN = os.environ.get("TOKEN")

exercise_end_point = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEET_END_POINT = os.environ.get("SHEET_END_POINT")

exercise_text = input("Tell me which exercise you did: ")

headers = {
    "x-app-id": APPLICATION_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}


response = requests.post(exercise_end_point, json=parameters, headers=headers)
result = response.json()
# print(result)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")


for exercise in result["exercises"]:
    sheets_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }


sheet_response = requests.post(SHEET_END_POINT, json=sheets_inputs,
                               auth=(USERNAME, PASSWORD))
# For Bearer Token Authentication
# bearer_headers = {
# "Authorization": "Bearer YOUR_TOKEN"
# }
# sheet_response = requests.post(
#     sheet_endpoint,
#     json=sheet_inputs,
#     headers=bearer_headers
# )


print(sheet_response)
