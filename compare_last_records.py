import datetime
import requests
import json
import datetime 

def main():
    url = ' https://atviras.vplanas.lt/arcgis/rest/services/Aplinkosauga/Oro_tarsa/MapServer/3/query'
    get_time(url)

def get_time(url):
    result_set = {} 
    query_to_get_no_of_sensors = { 
    'where':'sensor_index > 0',
    'outFields':'sensor_index', 
    'returnIdsOnly':'false',
    'returngeometry':'false',
    'returnDistinctValues':'true',
    'f':'pjson'}
    
    response = requests.get(url, params=query_to_get_no_of_sensors)
    data = json.loads(json.dumps(response.json()))
    
    for sensor in data['features']:
        get_sensor_info = { 
        'where':'sensor_index = ' + str(sensor['attributes']['sensor_index']),
        'outFields':'*', 
        'returnIdsOnly':'false',
        'returngeometry':'false',
        'orderByFields':'last_seen DESC',
        'resultRecordCount':'2',
        'f':'pjson'}
        sensor_the_same = True
        sensor_response = requests.get(url, params=get_sensor_info)
        sensor_data = json.loads(json.dumps(sensor_response.json()))
        #print(datetime.datetime.fromtimestamp(sensor_data['features'][0]['attributes']['last_seen'] / 1e3))
        #print(datetime.datetime.fromtimestamp(sensor_data['features'][1]['attributes']['last_seen'] / 1e3))
        #print()
        for attribute in sensor_data['features'][0]['attributes']:
            if attribute != 'last_seen':
                if not sensor_data['features'][0]['attributes'][attribute] == sensor_data['features'][1]['attributes'][attribute]:
                    sensor_the_same = False
                    break
        result_set[str(sensor['attributes']['sensor_index'])] = sensor_the_same
    
    print(result_set)
    return result_set

if __name__ == "__main__":
    main()