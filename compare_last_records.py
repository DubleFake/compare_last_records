import datetime
import requests
import json
from datetime import date
from datetime import timedelta
from datetime import datetime

def main():
    # Create variable to store target URL
    url = ' https://atviras.vplanas.lt/arcgis/rest/services/Aplinkosauga/Oro_tarsa/MapServer/3/query'
    
    # Execute the function with the URL created. 
    compare_records(url)

def compare_records(url):
    
    """
    Check if sensor's reading were from yesterday.
    
    Parameters:
        data (dict): A dictionary containing a list of sensors in the 'features' key. Each sensor is represented as a dictionary with an 'attributes' key containing sensor metadata.
    
    Returns:
        result_set (dict): A dictionary with sensor indexes as keys and a boolean value indicating whether the attributes of the two sensors with that index are the same or not.
        
    """
    
    result_set = {}
    
    # Construct a dictionary of parameters for the request to the URL to get the amount of sensors. 
    query_to_get_no_of_sensors = { 
    'where':'sensor_index > 0',
    'outFields':'sensor_index', 
    'returnIdsOnly':'false',
    'returngeometry':'false',
    'returnDistinctValues':'true',
    'f':'pjson'}
    
    response = requests.get(url, params=query_to_get_no_of_sensors)
    data = json.loads(json.dumps(response.json())) 
    yesterday = date.today() - timedelta(days = 1)

    # Loop through the list of sensors in data
    for sensor in data['features']:
        
        # Construct a dictionary of parameters for the request to the URL
        get_sensor_info = { 
        'where':'sensor_index = ' + str(sensor['attributes']['sensor_index']),
        'outFields':'*', 
        'returnIdsOnly':'false',
        'returngeometry':'false',
        'orderByFields':'last_seen DESC',
        'resultRecordCount':'1',
        'f':'pjson'}
        
        # Flag to store whether the two sensors are the same or not
        sensor_the_same = True
        
        # Make the request to the URL using the parameters in get_sensor_info
        sensor_response = requests.get(url, params=get_sensor_info)
        
        # Load the response data as JSON
        sensor_data = json.loads(json.dumps(sensor_response.json()))

        # Compare date of the sensor and yesterday
        if str(datetime.fromtimestamp(sensor_data['features'][0]['attributes']['last_seen'] / 1000).strftime('%Y-%m-%d')) == str(yesterday):

            # If true, mark that the most recent readings are from yesterday
            result_set[str(sensor['attributes']['sensor_index'])] = True
        else:

            # If false, mark that the most recent readings are from some other date
            result_set[str(sensor['attributes']['sensor_index'])] = False
        
    # Return the result_set dictionary
    return result_set

if __name__ == "__main__":
    main()