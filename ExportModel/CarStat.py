from ExportModel.CarDataItemList import CarDataItemList

class CarStatistics:
    '''car_type = example Golf 5'''
    def __init__(self, car_type_name):
        self.car_type_name = car_type_name
        '''car_data_item_list = aray of CarDataItemList objects'''
        self.car_data_item_list_list = []

    '''Populates the List object with a new CarDataItemList object'''
    def append_car_data_item_list(self, new_car_data_Item_list):
        self.car_data_item_list_list.append(new_car_data_Item_list)