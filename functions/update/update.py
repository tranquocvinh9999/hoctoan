import json


def update_json(field, new_value, filename=""):
    try:
        with open(filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        data[field] = new_value
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    except FileNotFoundError:
        print("File not found.")
    except KeyError:
        print("Key not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
