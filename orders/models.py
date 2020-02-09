from django.db import models
from shop.models import Product

class Order(models.Model): # Храним данные о покупателе
	first_name = models.CharField(max_length=50, verbose_name="Имя")
	last_name = models.CharField(max_length=50, verbose_name="Фамилия")
	email = models.EmailField()
	address = models.CharField(max_length=250, verbose_name="Адрес")
	postal_code = models.CharField(max_length=20, verbose_name="Индекс")
	city = models.CharField(max_length=100, verbose_name="Город")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False, verbose_name="Оплачено")

	class Meta:
		ordering = ('-created',)
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'

	def __str__(self):
		return 'Order {}'.format(self.id)

	def get_total_cost(self): # Получаем общую стоимость товаров в заказе
		return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model): # Храним товар, количество и стоимость для каждого элемета корзины
	order = models.ForeignKey(Order,
							  related_name='items',
							  on_delete=models.CASCADE)
	product = models.ForeignKey(Product,
								related_name='items',
								on_delete=models.CASCADE,
							    verbose_name="Продукт")
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
	quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

	def __str__(self):
		return '{}'.format(self.id)

	def get_cons(self): # Получаем общую стоимость позиций в корзине
		return self.price * self.quantity

	class Meta:
		verbose_name = 'Заказанный товар'
		verbose_name_plural = 'Заказанные товары'