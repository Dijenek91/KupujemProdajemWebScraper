'''Gets data from the specific car data(milage,price,year of production) by post page created from a user'''
import requests
from bs4 import BeautifulSoup

from ExportModel.CarDataItem import CarDataItem
from ExportModel.CarDataItemList import CarDataItemList
from ExportModel.CarStatistics import CarStatistics

class CarPostScraper:

    def __init__(self, base_url):
        self.__base_url = base_url

    '''Gets car data based on TUPLE (CAR_TYPE (POLO4) + list_of_post_URLS)'''
    '''Returns: List of CarStatistics objects'''
    def get_cars_data(self, list_of_tuples_with_list_of_post_urls):
        all_car_data = []
        for tuple in list_of_tuples_with_list_of_post_urls:
            car_type = tuple[0]
            list_of_links = tuple[1]

            one_car_statistics = CarStatistics(car_type)
            for link in list_of_links:
                car_data_item_list = self.__get_car_data(self.__base_url + link)
                one_car_statistics.append_car_data_item_list(car_data_item_list)

            all_car_data.append(one_car_statistics)
        return all_car_data

    '''Get car data for one car post page'''
    def __get_car_data(self, car_post_url):
        html_text = requests.get(car_post_url).text
        soup = BeautifulSoup(html_text, 'lxml')

        #gets all other relevant data
        car_price = self.__get_car_cost_data_item(soup)
        url_data_item = CarDataItem("url", car_post_url)

        #get data from table
        car_data_item_list = self.__get_table_car_stats(soup)

        car_data_item_list.car_data_item_list.append(car_price)
        car_data_item_list.car_data_item_list.append(url_data_item)

        return car_data_item_list

    def __get_car_cost_data_item(self, soup):
        price = soup.find('h2', class_='price-holder').text
        price = self.__format_price_string(price)
        return CarDataItem("Cena", price)

    '''Returns CarDataItemList object containing all car stat data from one post page'''
    '''CarDataItem contains (column_name, data_item)'''
    def __get_table_car_stats(self, soup):
        car_data_item_list = []
        column_names = soup.find_all('div', class_='col-1-6')
        column_datas = soup.find_all('div', class_='col-2-6')

        i=0
        column_number = len(column_names)
        while i < column_number:
            clean_column_name = column_names[i].text.strip('\n').strip('\t')
            clean_data = column_datas[i].text.strip('\n')
            data_item = CarDataItem(clean_column_name, clean_data)
            car_data_item_list.append(data_item)
            i += 1

        return CarDataItemList(car_data_item_list)

    def __format_price_string(self, price_string):
        return price_string.strip('\n').strip('\t').strip('\n').strip('\t').strip('\n')
