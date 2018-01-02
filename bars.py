import json
import os
from math import radians, cos, sin, asin, sqrt


def load_data(json_filepath):
    if not os.path.exists(json_filepath):
        return None
    with open(json_filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def get_biggest_bar(bars_list):
    return max(
        bars_list["features"],
        key=lambda feature:
        feature["properties"]["Attributes"]["SeatsCount"]
    )


def get_smallest_bar(bars_list):
    return min(
        bars_list["features"],
        key=lambda feature:
        feature["properties"]["Attributes"]["SeatsCount"]
    )


def get_closest_bar(bars_list, longitude, latitude):
    return min(
        bars_list["features"],
        key=lambda feature:
        get_distance_between_points(
            feature["geometry"]["coordinates"][1],
            feature["geometry"]["coordinates"][0],
            longitude,
            latitude
        )
    )


def print_bar_info(bar, message):
    print("{}\nНазвание: {}\nАдрес: {}\nТелефон: {}\n".format(
        message,
        bar["properties"]["Attributes"]["Name"],
        bar["properties"]["Attributes"]["Address"],
        bar["properties"]["Attributes"]["PublicPhone"][0]["PublicPhone"],
    ))


def get_distance_between_points(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km


def enter_coordinates():
    print("Введите через запятую ваши координаты. Их можно узнать я Яндекс картах")
    user_input = input()
    if user_input != "":
        longitude, latitude = user_input.split(",")
        return float(longitude), float(latitude)
    else:
        print("Для работы программы нужно ввести ваши координаты")
        return None


if __name__ == "__main__":
    longitude, latitude = enter_coordinates()

    bars_list = load_data("bars.json")

    biggest_bar = get_biggest_bar(bars_list)
    smallest_bar = get_smallest_bar(bars_list)
    closest_bar = get_closest_bar(
        bars_list,
        longitude,
        latitude
    )

    print_bar_info(biggest_bar, "Вот самый большой бар:")
    print_bar_info(smallest_bar, "Вот самый маленький бар:")
    print_bar_info(closest_bar, "Вот ближайший к вам бар:")

