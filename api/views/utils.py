class Operations:
    def __init__(self, cache, cache_key):
        self.cache = cache
        self.cache_key = cache_key

    def cart_information(self, products_list, Product):
        products_cart = []
        total = 0
        total_quantity=0
        product_quantity = {}
        for id in products_list:
            product = Product.query.filter_by(id=int(id)).first()
            total+=product.price
            total_quantity+=1
            if product:
                products_cart.append(product)
            
        products_cart = set(products_cart)
        total = round(total,2)
        return float(total), products_cart,total_quantity
    
    def get_product_quantity(self,products):
        aux=[]
        product_quantity = {}
        for product in products:
            if product not in aux:
                product_quantity[product] = products.count(product)
                aux.append(product)
        return product_quantity

    def get_products(self):
        products_list = self.cache.get(self.cache_key) or []
        return products_list

    def add_product(self, product_id):
        products_list = self.cache.get(self.cache_key) or []
        products_list.append(product_id)
        self.cache.set(self.cache_key, products_list)
        return products_list

    def delete_product(self, product_id):
        products_list = self.cache.get(self.cache_key) or []
        try:
            products_list.remove(product_id)
        except ValueError:
            pass
        self.cache.set(self.cache_key, products_list)
        return products_list
