from CarCategoryPageScraper import CarCategoryPageScraper
from CarPostScraper import CarPostScraper

if __name__ == '__main__':
    #initialize
    base_car_url = "https://www.kupujemprodajem.com/"
    car_post_scraper = CarPostScraper(base_car_url)
    car_category_page = CarCategoryPageScraper(base_car_url, car_post_scraper)
    #call processing
    car_category_page.get_all_car_posts_sorted_by_car_type()

    #scrape post individually
    #save csv file for excel spreadsheet

   # print(categories)
   # print(car_category_url_extension)
   # print(car_tuple_list)
