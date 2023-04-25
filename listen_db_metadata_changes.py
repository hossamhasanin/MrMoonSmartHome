import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pickle
import time
from sentence_transformers import SentenceTransformer
# Fetch the service account key JSON file contents
cred = credentials.Certificate('service_key.json')

# Initialize the app with a None auth variable, limiting the server's access
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://voiced-home-assistant-default-rtdb.europe-west1.firebasedatabase.app/',
    'databaseAuthVariableOverride': None
})

# listen to changes in database at /metadata ref
ref = db.reference('/metadata')
model = SentenceTransformer("models/all-MiniLM-L12-v2")

devices_ids_map = {}
devices = {}
rooms = {}

SAVE_PATH = "models/"

def callback(event):
    print(event.event_type)  # can be 'put' or 'patch'
    print(event.path)  # relative to the reference, it seems
    print(event.data)  # new data at /metadata
    # loop through the devices and add them to the current_devices dict
    # [None, {'device_type': 'home front door', 'device_type_id': 1}, {'device_type': 'temperature', 'device_type_id': 2}, {'device_type': 'normal lights', 'device_type_id': 3, 'room_name': 'kitchen'}, {'device_type': 'smart plug', 'device_type_id': 4, 'room_name': 'office'}, {'device_type': 'rgb lights', 'device_type_id': 5, 'room_name': 'office'}, {'device_type': 'gas leak alarm', 'device_type_id': 6, 'room_name': 'kitchen'}, {'device_type': 'people counter', 'device_type_id': 7}, None, {'device_type': 'entered wrong password alarm', 'device_type_id': 9}] 
    if event.path == "/":
        for device in event.data:
            if device is not None:
                devices[device['device_type_id']] = device['device_type']
                if 'room_name' in device:
                    rooms[device["device_type_id"]] = device["room_name"]

                device_room_key = device['device_type'] if 'room_name' not in device else device['room_name'] + "_" + device['device_type']
                devices_ids_map[device_room_key] = device['device_type_id']
                if device['device_type'] not in devices_ids_map:
                    devices_ids_map[device['device_type']] = device['device_type_id']
                else:
                    devices_ids_map.pop(device['device_type'])
    else:
        path = event.path.split("/")
        field = path[-1]
        deivce_id = path[-2]

        rooms[int(deivce_id)] = event.data if field == 'room_name' else rooms[int(deivce_id)]
        devices[int(deivce_id)] = event.data if field == 'device_type' else devices[int(deivce_id)]

        devices_ids_map_copy = devices_ids_map.copy()
        for key , value in devices_ids_map.items():
            if value == int(deivce_id):
                if '_' in key:
                    key_split = key.split('_')
                    if field == 'room_name':
                        devices_ids_map_copy[event.data + "_" + key_split[1]] = devices_ids_map_copy.pop(key)
                    else:
                        devices_ids_map_copy[key_split[0] + "_" + event.data] = devices_ids_map_copy.pop(key)
                else:
                    if field == 'device_type':
                        devices_ids_map_copy[event.data] = devices_ids_map_copy.pop(key)
        devices_ids_map.clear()
        devices_ids_map.update(devices_ids_map_copy)

    #filter devices_list for similar values
    devices_list = list(dict.fromkeys(list(devices.values())).keys())
    rooms_list = list(dict.fromkeys(list(rooms.values())).keys())

    devicesEmbed = model.encode(devices_list)
    roomsEmbed = model.encode(rooms_list)

    print("saving devices_embeddings.pkl")
    with open(SAVE_PATH + 'devices_embeddings.pkl', "wb") as fOut:
        pickle.dump({'sentences': devices_list, 'embeddings': devicesEmbed}, fOut, protocol=pickle.HIGHEST_PROTOCOL)
    print("saving rooms_embeddings.pkl")
    with open(SAVE_PATH + 'rooms_embeddings.pkl', "wb") as fOut:
        pickle.dump({'sentences': rooms_list, 'embeddings': roomsEmbed}, fOut, protocol=pickle.HIGHEST_PROTOCOL)
    print("saved successfully devices_embeddings.pkl and rooms_embeddings.pkl")

    print("devices_ids_map: ")
    print(devices_ids_map)
    print("saving devices_ids_map to devices_ids.pkl")
    with open(SAVE_PATH + 'devices_ids.pkl', "wb") as fOut:
        pickle.dump(devices_ids_map, fOut, protocol=pickle.HIGHEST_PROTOCOL)
    print("saved successfully devices_ids_map to {}".format(SAVE_PATH))

print("Listening to changes in /metadata ref...")
# Listen for changes
my_listener = ref.listen(callback)


try: 
    while True: 
        time.sleep(1)
except KeyboardInterrupt: 
    print('Closing listener wait a bit...')
    my_listener.close()