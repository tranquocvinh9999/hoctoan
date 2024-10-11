import json
import os

# Load the existing data from the JSON file or initialize it if it doesn't exist
if os.path.exists("lectures.json"):
    with open("lectures.json", "r", encoding="utf-8") as f:
        lectures_data = json.load(f)
else:
    lectures_data = {"count": 0}

# Function to generate the next file name and update the count
def get_next_file_name():
    lectures_data["count"] += 1
    return f'lecture{lectures_data["count"]}'

# Get the user input
k = input("Enter the lecture content: ")

# Create the info dictionary with the new lecture entry
info = {
    get_next_file_name(): k
}

# Update the existing lectures data with the new lecture entry
lectures_data.update(info)

# Write the updated data back to the JSON file
with open("lectures.json", "w", encoding="utf-8") as f:
    json.dump(lectures_data, f, ensure_ascii=False, indent=4)
