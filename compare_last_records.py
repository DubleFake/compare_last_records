import datetime
import requests
import json
import datetime 

def main():
    # Create variable to store target URL
    url = ' https://atviras.vplanas.lt/arcgis/rest/services/Aplinkosauga/Oro_tarsa/MapServer/3/query'
    
    # Execute the function with the URL created. 
    get_time(url)

def get_time(url):
    
    """
    Compare the attributes of two sensors with the same index.
    
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
    
    
    # Loop through the list of sensors in data
    for sensor in data['features']:
        
        # Construct a dictionary of parameters for the request to the URL
        get_sensor_info = { 
        'where':'sensor_index = ' + str(sensor['attributes']['sensor_index']),
        'outFields':'*', 
        'returnIdsOnly':'false',
        'returngeometry':'false',
        'orderByFields':'last_seen DESC',
        'resultRecordCount':'2',
        'f':'pjson'}
        
        # Flag to store whether the two sensors are the same or not
        sensor_the_same = True
        
        # Make the request to the URL using the parameters in get_sensor_info
        sensor_response = requests.get(url, params=get_sensor_info)
        
        # Load the response data as JSON
        sensor_data = json.loads(json.dumps(sensor_response.json()))
        
        # Loop through the attributes of the first sensor
        for attribute in sensor_data['features'][0]['attributes']:
            # Skip the 'last_seen' attribute, as it is expected to be different
            if attribute != 'last_seen':
                 # If any other attribute is different between the two sensors, set sensor_the_same to False and break the loop
                if not sensor_data['features'][0]['attributes'][attribute] == sensor_data['features'][1]['attributes'][attribute]:
                    sensor_the_same = False
                    break
                
        # Add an entry to the result_set dictionary with the sensor index as the key and the value of sensor_the_same
        result_set[str(sensor['attributes']['sensor_index'])] = sensor_the_same
        
    # Return the result_set dictionary
    return result_set

if __name__ == "__main__":
    main()