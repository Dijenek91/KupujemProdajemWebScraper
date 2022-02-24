class UserInputCollector:
    @staticmethod
    def get_user_input_for(site_category_dict):
        category_dict_names = {}
        category_names = site_category_dict.keys()
        print("Which Car category do you want to scrape (enter number)")
        index = 0
        for category_name in category_names:
            category_dict_names[index] = category_name
            print(f'{index} : {category_name}')
            index = index + 1;
        chosen_car_manufacturer_index = int(input('>'))
        category_name_from_user = category_dict_names[chosen_car_manufacturer_index]
        return site_category_dict[category_name_from_user]

    @staticmethod
    def get_user_input_for_num_of_pages():
        print(f'Enter the number of pages to scrap from website:')
        return int(input('>'))