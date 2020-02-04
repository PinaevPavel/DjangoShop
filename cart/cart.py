#from decimal import Decimal
#from django.conf import settings
#from shop.models import Product#

#class Cart(object):#

#	def __init__(self, request): # иницилизация объекта корзины
#		self.session = request.session # запоминаем текущую сессию в атрибуте, что бы иметь к ней доступ в других методах класса
#		cart = self.session.get(settings.CART_SESSION_ID) # пытаемся получить данные корзины
#		if not cart: # Если корзина пустая, то создаем пустую корзину
#			cart = self.session[settings.CART_SESSION_ID] = {} # сохраняем в сессии пустую карзину
#		self.cart = cart	#

#	def __iter__(self): # проходим по товарам корзиныы и получаем соотвествующие объекты Product
#		product_ids = self.cart.keys() # keys() возвращает ключи в словаре
#		products = Product.objects.filter(id__in=product_ids) # фильтруем продукты по наличии ключей в product_ids#

#	def __len__(self):# возвращаем общее количество товаров в корзине#

#		return sum(item['quantity'] for item in self.cart.values())
#		
#		cart = self.cart.copy()
#		for product in products:
#			cart[str(product.id)]['product'] = product#

#		for item in cart.values(): # values() возвращает коллекцию значений словаря cart
#			item['price'] = Decimal(item['price']) # Decimal позволяет хранить значения цены с высокой точностью
#			item['total_price'] = item['price'] * item['quantity'] # получаем сумму 
#			yield item#

#	def add(self, product, quantity=1, update_quantity=False): # Добавление товаров в корзину или обновление его количества
#		product_id = str(product.id) # Добавляем строковое значение id продукта
#		if product_id not in self.cart:  # Если продукт не был добавлен в корзину, заносим его количесво и цену в корзину
#			self.cart[product_id] = {'quantity': 0, 'price': str(product.price), 'name': str(product.name)}
#		if update_quantity: # Если количество продукта в корзине было изменино, то переписывает значение количества продукта
#			self.cart[product_id]['quantity'] = quantity 
#		else:
#			self.cart[product_id]['quantity'] += quantity
#		self.save()	#

#	def save(self): # Метод помечает сессию как измененную, так мы говорим Джанго о том, что редактировали данные сессии и теперь их необходимо сохранить
#		self.session.modified = True	#

#	def remove(self, product): # Удаляем товары из корзины
#		product_id = str(product.id)
#		if product_id in self.cart: # если указанный id продукта есть к корзине, то
#			del self.cart[product_id] # удаляем указанный продукт из корзины
#			self.save()#
#

#	def get_total_price(self):
#		return sum(
#				Decimal(item['price']) * item['quantity']
#				for item in self.cart.values()
#			)#

#	def clear(self): # Удаляем данные из корзины
#		del self.session[settings.CART_SESSION_ID]
#		self.save()

from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    def __init__(self, request): # иницилизация объекта корзины
        self.session = request.session # запоминаем текущую сессию в атрибуте, что бы иметь к ней доступ в других методах класса
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products 
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()