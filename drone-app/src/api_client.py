import requests
from hashlib import sha256


def upload_img(endpoint, json_data, img_path):
    filename = img_path.split("/")[-1]
    files = {'img': (filename, open(img_path, 'rb'))}

    h = sha256()
    h.update(open(img_path, 'rb').read())
    aux = h.hexdigest()
    print(aux)

    response = requests.post(
        endpoint,
        files=files,
        data=json_data
    )
    return response.json()



if __name__=="__main__":
    r = upload_img(
        "https://rggnnhjz9k.execute-api.eu-west-1.amazonaws.com/dev/api/trip_img",
        {"vehicle_id": "1", "trip_id": "20220513134921"},
        "drone-app/data_log/1/20220513134921/20220513134921.jpg"
    )
    print(r)