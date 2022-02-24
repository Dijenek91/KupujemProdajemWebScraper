from collections import defaultdict
from UserInputCollector import UserInputCollector
from CarPostScraper import CarPostScraper
from bs4 import BeautifulSoup
import requests

class CarCategoryPageScraper:
    __base_url = ""
    __car_post_scraper = CarPostScraper(__base_url)

    def __init__(self, base_url, car_post_scraper):
        self.__base_url = base_url
        self.__car_post_scraper = car_post_scraper

    #returns tuple list sorted by key (car type) example volkswagen polo 1
    def get_all_car_posts_sorted_by_car_type(self):
        categories = self.__get_all_categories_from_kp()
        car_category_url_extension = UserInputCollector.get_user_input_for(categories)
        car_tuple_list = self.__get_car_post_tuple_list_multiple_pages(car_category_url_extension)
        sorted_car_tuple_list = self.__sort_tuple_by_key(car_tuple_list)

        self.__car_post_scraper.get_cars_data(sorted_car_tuple_list)

    def __get_all_categories_from_kp(self):
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

    ###Gets a tuple list (car type, url extension for that user post) for multiple pages
    def __get_car_post_tuple_list_multiple_pages(self, car_category_url_extension):
        pageNumberToScrap = UserInputCollector.get_user_input_for_num_of_pages()
        car_tuple_list = []
        current_page = 1
        while current_page <= pageNumberToScrap:
            one_page_car_links = self.__get_car_post_tuple_list_for_one_page(car_category_url_extension, current_page)
            car_tuple_list.extend(one_page_car_links)
            current_page = current_page + 1
        return car_tuple_list

    ##returns all tuples from one page containing (car_type, link_to_user_post) Ex:(vw polo, wwww.vwPoloPost1.com)
    def __get_car_post_tuple_list_for_one_page(self, car_category_url_extension, page_to_scrape):
        html_request_url = f'{self.__base_url}{car_category_url_extension}{page_to_scrape}'
        html_text = requests.get(html_request_url).text
        soup = BeautifulSoup(html_text, 'lxml')
        car_links = soup.find_all('a', class_='adName')
        car_posts_tuple_list = []
        for link in car_links:
            post_href_link = link['href']
            car_type = post_href_link.split('/')[3].strip()
            car_posts_tuple_list.append((car_type, post_href_link))
        return car_posts_tuple_list


    """
    returns list of tuples (car_type, [list of car_type user_post links)
    example [(vw passat 5, [url_post_link1, url_post_link2]), ....]
    """
    def __sort_tuple_by_key(self, car_tuple_list):
        car_dictionary = defaultdict(list)
        for key, *link in car_tuple_list:
            car_dictionary[key].append(link[0])

        print(car_tuple_list)
        print(list(car_dictionary.items()))
        return list(car_dictionary.items())
