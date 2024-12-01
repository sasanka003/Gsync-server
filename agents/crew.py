from crews.iot_crew.iot_crew import IotAnalystCrew


result = IotAnalystCrew().crew().kickoff(inputs={
    "plant_data": "capscicum, temperature 27 celcius, humidity 66, light intensity 23,000 lux, Co2 levels 500ppm"
})

print(result)