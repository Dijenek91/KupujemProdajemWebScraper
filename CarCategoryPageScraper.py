from collections import defaultdict

from ExportModel.CarLinkDTO import CarLinkDTO
from UserInputCollector import UserInputCollector
from bs4 import BeautifulSoup
import requests

class CarCategoryPageScraper:
    def __init__(self, base_url, car_post_scraper):
        self.__base_url = base_url
        self.__car_post_scraper = car_post_scraper

    def get_all_car_data(self):
        """
        Gets all car data for each post

        :return all_car_data:
            List of CarStatistics Objects
        """
        sorted_car_post_tuple_list = self.get_all_car_posts_sorted_by_car_type()
        all_car_data = self.__car_post_scraper.get_cars_data(sorted_car_post_tuple_list)  # list of CarStatistics objects
        return all_car_data

    def get_all_car_posts_sorted_by_car_type(self):
        """
        Gets all car post links from a specific car category
        
        :return sorted_car_post_tuple_list:
            Sorted (by car type name) tuple list of car post links
        """
        categories = self.__get_all_categories_from_kp()
        car_category_url_extension = UserInputCollector.get_user_input_for(categories)
        carLinkDto_list_for_multiple_pages = self.__get_car_post_tuple_list_multiple_pages(car_category_url_extension)
        sorted_car_post_tuple_list = self.__sort_list_by_car_type_name(carLinkDto_list_for_multiple_pages)
        return sorted_car_post_tuple_list


    def __get_all_categories_from_kp(self):
        """
        Gets all car categories on the kupujemprodajem.com/automobili/kategorija/2013 url

        :return category_dict:
            Dictionary where the key is the category name, and the value is the category URL
        """
        category_url_expand = "automobili/kategorija/2013"
        html_text = requests.get(self.__base_url + category_url_expand).text
        soup = BeautifulSoup(html_text, 'lxml')
        div_category_titles = soup.find_all('div', class_='categoryTitle')
        category_dict = {}
        for categoryDiv in div_category_titles:
            div_heading_2 = categoryDiv.h2
            categoryLink = div_heading_2.a['href']
            category_name = div_heading_2.span.text
            category_dict[category_name] = categoryLink[:-1]
        return category_dict

    ###
    def __get_car_post_tuple_list_multiple_pages(self, car_category_url_extension):
        """
        Gets a CarLinkDTO list (car type, url extension for that user post) for multiple pages

        :param car_category_url_extension: Car category url extensions on KupujemProdajem site
        :return carLinkDto_list_for_multiple_pages:
        """
        pageNumberToScrap = UserInputCollector.get_user_input_for_num_of_pages()
        carLinkDto_list_for_multiple_pages = []
        current_page = 1
        while current_page <= pageNumberToScrap:
            car_link_dto_list_for_one_page = self.__get_car_post_tuple_list_for_one_page(car_category_url_extension, current_page)
            carLinkDto_list_for_multiple_pages.extend(car_link_dto_list_for_one_page)
            current_page = current_page + 1
        return carLinkDto_list_for_multiple_pages

    #
    def __get_car_post_tuple_list_for_one_page(self, car_category_url_extension, page_to_scrape):
        """
        Gets a CarLinkDTO list (car type, url extension for that user post) for ONLY one page

        :param car_category_url_extension: Car category url extensions on KupujemProdajem site
        :param page_to_scrape: How many pages to scrape
        :return carLinkDto_list:
            list of CarLinkDTO objects each containing car type name and post url link
        """
        html_request_url = f'{self.__base_url}{car_category_url_extension}{page_to_scrape}'
        html_text = requests.get(html_request_url).text
        soup = BeautifulSoup(html_text, 'lxml')
        car_links = soup.find_all('a', class_='adName')
        carLinkDto_list = []
        for link in car_links:
            post_href_link = link['href']
            car_type = post_href_link.split('/')[3].strip()
            carLinkDto_list.append(CarLinkDTO(car_type, post_href_link))
        return carLinkDto_list


    def __sort_list_by_car_type_name(self, car_link_dto_list):
        """
        Sorts list by car type Name

        :param car_tuple_list:
        :return tuple List:
            Sorted tuple list by car type name example [(car_url, [url_post_link1, url_post_link2]),() ....]
        """


        car_dictionary = defaultdict(list)
        for car_link_dto in car_link_dto_list:
            car_dictionary[car_link_dto.car_type_name].append(car_link_dto.post_url_link)

        print(car_dictionary)
        print(list(car_dictionary.items()))
        return list(car_dictionary.items())
