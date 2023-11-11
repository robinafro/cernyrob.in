import os
import json
import time

data_dir = os.path.join(os.path.dirname(__file__), "Database")
ids_dir = os.path.join(os.path.dirname(__file__), "IDs")
log_dir = os.path.join(os.path.dirname(__file__), "Logs")

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(ids_dir):
    os.makedirs(ids_dir)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

data_template = {
    "robin_clicker": {
        "clicks": 0,
        "clickmult": 1,
        "upgrades": [],
    },

    "callme": {
        "phone_number": None,
        "name": None,
    },

    "user_data": {
        "username": None,
        "user_id": None,
        "password": None,
        "salt": None,
    }
}

queues = {}
last_data = {}

def recursive_dict_search(dictionary, target_key):
    if target_key in dictionary:
        return dictionary
    for key, value in dictionary.items():
        if isinstance(value, dict):
            result = recursive_dict_search(value, target_key)
            if result is not None:
                return result
    return None

def save_data(key, data):
    if key == 0:
        return
    
    filename = os.path.join(data_dir, f"{key}.json")
    with open(filename, "w") as file:
        json.dump(data, file)

def load_data(key):
    if key == 0 or key is None:
        return data_template
    
    filename = os.path.join(data_dir, f"{key}.json")
    if os.path.exists(filename):
        with open(filename, "r") as file:
            if file is None or file == "":
                return data_template
            
            return json.load(file)
    else:
        return data_template

def load_or_create_data(request):
    cookie = request.cookies.get('id')
    was_none = False

    if cookie is None:
        was_none = True

        cookie = time.time()
    
    data = load_data(cookie)

    if was_none:
        save_data(cookie, data_template)
    
    return data

def increment(key, field, amount=1):
    # Initialize queue
    queue = queues.get(key)
    if queue is None:
        queues[key] = []
        queue = queues[key]
    
    tm = int(time.time_ns() / 1e6)

    # Add to queue
    queue.append(tm)

    # Wait for turn
    while True:
        if queue.index(tm) == 0:
            break
        else:
            time.sleep(0.05)
    
    # Get data
    data = load_data(key)
    table = recursive_dict_search(data, field)
    last_table = None

    if not (last_data.get(key) is None):
        last_table = recursive_dict_search(last_data.get(key), field)

    if isinstance(amount, str):
        amountTable = recursive_dict_search(data, amount)
        amount = amountTable[amount]

    # If previous data exists, ensure it has been updated correctly
    if (not (last_table is None)) and (not (last_table.get(field) is None)):
        while table[field] < last_table.get(field):
            data = load_data(key)
            table = recursive_dict_search(data, field)
            time.sleep(0.05)

    # Increment data
    table[field] += amount
    last_data[key] = data
    save_data(key, data)

    # Remove from queue
    queue.pop(0)

    return data

def get_user_from_user_id(id):
    # iterate through all database files
    for file in os.listdir(data_dir):
        # load the data
        data = load_data(file.replace(".json", ""))
        # check if the user_id matches
        if data["user_data"].get("user_id") is None:
            continue

        if data["user_data"]["user_id"] == id:
            return data["user_data"]["username"]
    
def get_userid_from_username(username):
    return load_data(get_cookie_from_user(username))["user_data"]["user_id"]

def get_user_from_cookie(cookie):
    filename = os.path.join(ids_dir, f"{cookie}.txt")
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return file.read()
    else:
        return None
    
def set_user_to_cookie(cookie, user):
    filename = os.path.join(ids_dir, f"{cookie}.txt")
    with open(filename, "w") as file:
       file.write(user)

def get_cookie_from_user(username):
    for cookie in os.listdir(ids_dir):
        with open(os.path.join(ids_dir, cookie), "r") as file:
            usr = file.read()
            if usr == username:
                return cookie.replace(".txt", "")
    return None