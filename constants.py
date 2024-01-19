CSV_DELIMITER = ','
CSV_ENCODING = 'utf-8'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
EARTH_RADIUS = 6371
SPEED_CONVERSION = 3.6
KM_TO_M_CONVERSION = 1000
MAX_SPEED = 50
BUS_COUNT_THRESHOLD = 0.15
MAX_DISTANCE = 3000
BUS_OUTPUT1_FILE = 'output/bus_output1.csv'
BUS_OUTPUT2_FILE = 'output/bus_output2.csv'
API_KEY = '44c76d0d-4ca7-456a-a694-3b4dd63dd2d5'
EARLY_RUN_HOURS = {11, 12}
LATE_RUN_HOURS = {17, 18}

BUS_TRACKER_API_URL = 'https://api.um.warszawa.pl/api/action/busestrams_get/'
BUS_TRACKER_API_RESOURCE_ID = 'f2e5503e-927d-4ad3-9500-4ab9e55deb59'

BUS_STATION_API_URL = 'https://api.um.warszawa.pl/api/action/dbstore_get/'
BUS_STATION_API_RESOURCE_ID = '1c08a38c-ae09-46d2-8926-4f9d25cb0630'

BUS_TRACKER_API_PARAMS = {
    'resource_id': BUS_TRACKER_API_RESOURCE_ID,
    'apikey': API_KEY,
    'type': 1,
}

BUS_STATION_API_PARAMS = {
    'resource_id': BUS_STATION_API_RESOURCE_ID,
    'apikey': API_KEY,
}