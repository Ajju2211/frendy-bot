import requests
from urllib.parse import urljoin
# import os
# DB_BASE_URL = os.environ.get('DB_BASE_URL')
# DB_BASE_URL ='https://frendy123.herokuapp.com/'
class Products:
    # DB_BASE_URL ='https://frendy123.herokuapp.com/'
    def __init__(self,DB_BASE_URL ='https://frendy123.herokuapp.com/'):
        """
        Paramters: DB_BASE_URL
        DefaultSort: -Discount (Descending order)
        """
        
        self.db_base_url = DB_BASE_URL
        
        self.db_products_url = urljoin(DB_BASE_URL, "api/v2/products/")
        self.db_categories_url = urljoin(DB_BASE_URL, "api/v2/allcategories")
        self.categories = requests.get(self.db_categories_url).json()
        self.products = None
      
        
        self.limit = 140
        self.sort = "-Discount"
        #limit=140 
        #sort = "-Discount"

    
    def getCategories(self):
        """
        Returns list of categories
        """
        self.db_categories_url = urljoin(self.db_base_url, "api/v2/allcategories")
        self.categories = requests.get(self.db_categories_url).json()
        return self.categories[0:10]

    def getProducts(self):
        """
        returns default limit number
        of products based on any sort applied.
        :
        list of dicts
        """
        params = {
            "limit":self.limit,
            "sort":self.sort
        }
        self.products = requests.get(self.db_products_url,params = params).json()
        return self.products

    def getProductById(self, p_id):
        """
        Parameter: product Id
        Returns: Specific Product
        type: Dict
        """
        product_url = urljoin(self.db_base_url,"api/v2/products/"+p_id)
        product = requests.get(product_url).json()
        return product

    
    def getProductsByCat(self, cat):
        """
        parameter: category
        Returns: Products of same category
        type: list of dicts
        """
        # Temp implementation
        products = requests.get(self.db_products_url).json()
        def checkCat(x):
            return x["Category"].lower() == cat.lower()
        
        filteredProducts = list(filter(checkCat, products))
        return filteredProducts