class CarDataItemList:
    def __init__(self, new_car_data_item_list):
        self.car_data_item_list = new_car_data_item_list
        
    def get_header_list(self):
        header_list = []
        for car_data_item in self.car_data_item_list:
            header_list.append(car_data_item.column_name)
        return header_list

    def get_data_fields_list(self):
        data_field_list = []
        for car_data_item in self.car_data_item_list:
            data_field_list.append(car_data_item.data_field)
        return data_field_list