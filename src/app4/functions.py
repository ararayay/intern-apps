import requests


def get_coordinates(address, api_key):
    try:
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            'apikey': api_key,
            'geocode': address,
            'format': 'json'
        }

        response = requests.get(url, params=params)
        data = response.json()

        geo_objects = data['response']['GeoObjectCollection']['featureMember']
        if geo_objects:
            coords = geo_objects[0]['GeoObject']['Point']['pos'].split(' ')
            # Формат [широта, долгота] для Yandex Maps
            return [float(coords[1]), float(coords[0])]
    except Exception as e:
        print(f"Ошибка: {e}")

    return None