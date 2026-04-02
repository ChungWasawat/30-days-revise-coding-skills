import requests


def send_request():
    response = requests.get( 
    "https://api.open-meteo.com/v1/forecast",
    
    #payload 
    params={
        "latitude": 13.75,          # Bangkok
        "longitude": 100.52,
        "hourly": "temperature_2m",
        "forecast_days": 3
    },

    timeout=10
    )

    return response

def send_request_post():
    response = requests.post(
    "https://httpbin.org/post",
    headers={
        'accept': 'application/json'
    },
    timeout=10

    )
    return response


response = send_request()
print("url: ", response.url)
#print("text: ", response.text)                             # data 
print("encoding: ", response.encoding)   
print("error status: ", response.raise_for_status())        # raises exception if 4xx/5xx
data = response.json()                                      # parse JSON response
print(data["hourly"]["temperature_2m"])



response2 = send_request_post()
print("post url: ", response2.url)