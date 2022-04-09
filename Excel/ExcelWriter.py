import tablib
from tablib import Dataset, Databook


class ExcelWriter:
    #def __init__(self):

    def create_report(self, list_of_car_statistics_objects):
        book = self.__get_databook(list_of_car_statistics_objects)

        with open('car_data.xls', 'wb') as f_output:
            f_output.write(book.export('xls'))

        return

    def __get_databook(self, list_of_car_statistics_objects):
        book = Databook()
        for car_statistics_object in list_of_car_statistics_objects:
            sheet_name = car_statistics_object.car_type_name
            data_set = Dataset(title=sheet_name)
            data_set.headers = car_statistics_object.get_header_list()

            for car_data_item_list in car_statistics_object.car_data_item_list_list:
                data_fields = car_data_item_list.get_data_fields_list()
                data_set.append(data_fields)

            book.add_sheet(data_set)
        return book
