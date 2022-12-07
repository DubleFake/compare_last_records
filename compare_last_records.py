import datetime
import requests
import json
import datetime 

def main():
    url = ' https://atviras.vplanas.lt/arcgis/rest/services/Aplinkosauga/Oro_tarsa/MapServer/3/query'
    date = datetime.datetime.fromtimestamp(1669680000000 / 1e3)
    print(date)

def get_time(url):
    query_to_get_no_of_sensors = { 
    'where':'sensor_index > 0',
    'outFields':'sensor_index' 
    'returnIdsOnly':'false',
    'returngeometry':'false',
    'returnDistinctValues':'true',
    'f':'pjson'}
    
    response = requests.get(url, params=query_to_get_no_of_sensors)

    data_json = response.json()
    attributes = json.dumps(data_json['features'])
    timestamp = json.loads(attributes)[0]['attributes']['timestamp']

    dt = datetime.datetime.fromtimestamp(timestamp / 1000)
    formatted_time = dt.strftime('%Y-%m-%d %H:%M')
    return formatted_time

if __name__ == "__main__":
    main()