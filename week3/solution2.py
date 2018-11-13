import csv
import os
import pprint
import re


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand, self.photo_file_name, self.carrying = brand, photo_file_name, carrying

    def get_photo_file_ext(self):
        _, extension = os.path.splitext(self.photo_file_name)
        return extension

    def _base_repr(self):
        return f'{self.__class__.__name__}({self.brand}, {self.photo_file_name}, {self.carrying}'


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count

    def __repr__(self):
        return self._base_repr() + f', {self.passenger_seats_count})'


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_length, self.body_width, self.body_height = self._split_size(body_whl)

    @staticmethod
    def _split_size(size):
        result = re.search(r'(.+)x(.+)x(.+)', size)
        if result:
            size = result.groups()
            return [float(dim) for dim in size]
        else:
            return 0.0, 0.0, 0.0

    def __repr__(self):
        return self._base_repr() + f', {self.body_length}, {self.body_width}, {self.body_height})'

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

    def __repr__(self):
        return self._base_repr() + f', {self.extra})'


def _parse_row(row):
    if len(row) != 7:
        return None
    car_type, brand, passenger_seats_count, photo_file_name, body_whl, carrying, extra = row
    carrying = float(carrying)
    if car_type == Car.car_type:
        passenger_seats_count = int(passenger_seats_count)
        return Car(brand, photo_file_name, carrying, passenger_seats_count)
    elif car_type == Truck.car_type:
        return Truck(brand, photo_file_name, carrying, body_whl)
    elif car_type == SpecMachine.car_type:
        return SpecMachine(brand, photo_file_name, carrying, extra)


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader)
        for row in reader:
            car = _parse_row(row)
            if car:
                car_list.append(car)
    return car_list


if __name__ == '__main__':
    pprint.pprint(get_car_list('test_data2.csv'))
