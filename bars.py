import json
import os
from math import radians, cos, sin, asin, sqrt
import sys


def load_data(json_filepath):
    if not os.path.exists(json_filepath):
        return None
    with open(json_filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def get_biggest_bar(bars_list):
    return max(bars_list, key=lambda bar:
        bar["properties"]["Attributes"]["SeatsCount"]
    )


def get_smallest_bar(bars_list):
    return min(bars_list, key=lambda bar:
        bar["properties"]["Attributes"]["SeatsCount"]
    )


def get_closest_bar(bars_list, longitude, latitude):
    return min(
        bars_list,
        key=lambda bar:
        get_distance_between_points(
            bar["geometry"]["coordinates"][1],
            bar["geometry"]["coordinates"][0],
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
    https://stackoverflow.com/questions/15736995/
    how-can-i-quickly-estimate-the-distance-
    between-two-latitude-longitude-points

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    earth_radius = 6371
    distance = earth_radius * c
    return distance


def enter_coordinates():
    longitude = input("Введите ваши координаты.\nДолгота:\n")
    latitude = input("Введите ваши координаты.\nШирота:\n")
    try:
        return float(longitude), float(latitude)
    except ValueError:
        print("Ошибка в переданных координатах, попробуйте еще раз")
        return None, None


if __name__ == "__main__":
    if len(sys.argv) == 2:
        json_data = load_data(sys.argv[1])
        if json_data is not None:
            bars_list = json_data["features"]

            longitude, latitude = enter_coordinates()

            if longitude is not None and latitude is not None:
                biggest_bar = get_biggest_bar(bars_list)
                smallest_bar = get_smallest_bar(bars_list)
                closest_bar = get_closest_bar(
                    bars_list,
                    longitude,
                    latitude
                )

                print_bar_info(biggest_bar, "\nВот самый большой бар:")
                print_bar_info(smallest_bar, "Вот самый маленький бар:")
                print_bar_info(closest_bar, "Вот ближайший к вам бар:")
        else:
            print("Введен неправильный путь к файлу")
    else:
        print("Для работы скрипта нужно указать путь к файлу со списком баров")

