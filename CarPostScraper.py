import requests
from bs4 import BeautifulSoup

class CarPostScraper:
    __base_url = ""
    def __init__(self, base_url):
        self.__base_url = base_url

    '''Gets car data based on TUPLE (CAR_TYPE (POLO4) + list_of_post_URLS)'''
    def get_cars_data(self, list_of_tuples_with_list_of_post_urls):
        for tuple in list_of_tuples_with_list_of_post_urls:
            car_type = tuple[0]
            list_of_links = tuple[1]

            for link in list_of_links:
                self.__get_car_data(self.__base_url + link)

    def __get_car_data(self, car_post_url):
        html_text = requests.get(car_post_url).text
        soup = BeautifulSoup(html_text, 'lxml')
        result = self.__get_table_car_stats(soup)
        return ""

    def __get_table_car_stats(self, soup):
        table_rows = soup.find_all('div', class_='row vertical-padding')
        '''Filtering of data from the table to a list of tuples (item:value)'''

        return table_rows
