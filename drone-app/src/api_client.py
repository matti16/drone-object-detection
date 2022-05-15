import requests
import base64
import json
import shutil
import os


class ApiClient:
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def make_api_post(self, endpoint, payload):
        url = f"{self.url}/{endpoint}"
        headers = {
            'x-api-key': self.token,
            'Content-Type': 'application/json'
        }
        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        return response
    
    def upload_trip_img(self, img_path, vechicle_id, trip_id):
        print(f"Uploading image {img_path}...")
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            img_data = encoded_string.decode('utf-8')

        filename = img_path.split("/")[-1]
        payload = {
            "vehicle_id": vechicle_id,
            "trip_id": trip_id,
            "filename": filename,
            "data": img_data
        }
        return self.make_api_post("trip_img", payload) 

    def upload_trip_json(self, filepath):
        print(f"Uploading json trip {filepath}...")
        trip = json.load(open(filepath))
        return self.make_api_post("trip", trip)

    
    def upload_trips(self, input_dir, output_dir):
        for vechicle_id in os.listdir(input_dir):
            vechicle_path = os.path.join(input_dir, vechicle_id)
            for trip_id in os.listdir(vechicle_path):
                # Upload Trip
                trip_path = os.path.join(vechicle_path, trip_id)
                target_dir = os.path.join(output_dir, vechicle_id, trip_id)
                os.makedirs(target_dir, exist_ok=True)

                for f in os.listdir(trip_path):
                    filepath = os.path.join(trip_path, f)
                    if f.endswith(".jpg"):
                        r = self.upload_trip_img(filepath, vechicle_id, trip_id)
                    elif f.endswith(".json"):
                        r = self.upload_trip_json(filepath)
                    else:
                        continue
                
                    # Move to uploaded
                    if r.status_code == 200:
                        shutil.move(filepath, target_dir)
                    else:
                        print(f"Status code not 200: {r.status_code}")


