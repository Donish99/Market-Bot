import requests
from random import randint


class MainClass:
    """Temproary Class for performing task to the function """

    def __init__(self):
        self.categories = {}
        self.products_with_details = {}

    def init_or_refresh_data(self):
        """Gets all the data from the server and puts all the lists to the appropriate data structures"""

        # Calling prods from the server
        all_prods_url = 'http://167.71.60.217:2020/product/all'
        data = requests.get(url=all_prods_url)
        data = data.json()
        data = data['results']
        # It contains id, name, price, image (url of image), unit, caregory keys
        self.products_with_details = data

        category_url = 'http://167.71.60.217:2020/product/categories'
        data = requests.get(url=category_url)
        data = data.json()
        data = data['results']
        self.categories = data  # It contains is, name keys

    def get_category_names(self):
        """Returns a list with category names"""
        category_names = []
        for cat in self.categories:
            category_names.append(cat['name'])
        return category_names

    def get_product_names(self):
        """Returns a list with prduct names"""
        prod_names = []
        for prod in self.products_with_details:
            prod_names.append(prod['name'])
        return prod_names

    def get_prods_in_given_category(self, categ):
        """Returns a list of products in given category"""
        prods = []
        for prod in self.products_with_details:
            if prod['caregory'] == categ:
                prods.append(prod['name'])
        return prods

    def get_product_details(self, prod_name):
        for p in self.products_with_details:
            if p['name'] == prod_name:
                return p


if __name__ == '__main__':
    pass
