from django.db import models
from django.urls import reverse

class Category(models.Model):
	name = models.CharField(max_length=200, db_index=True, verbose_name='Наименование категории')
	names = models.CharField(max_length=200, db_index=True, verbose_name='Наименоване категории во множественном числе')
	slug = models.SlugField(max_length=200, unique=True)

	class Meta:
		ordering = ['name',]
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	name = models.CharField(max_length=200, db_index=True, verbose_name='Наименование товара')
	slug = models.SlugField(max_length=200, db_index=True)
	image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
	description = models.TextField(blank=True, verbose_name='Описание')
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
	available = models.BooleanField(default=True, verbose_name='Наличие товара')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
	updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

	class Meta:
		verbose_name_plural = 'Товары' #Название модели во множественном числе
		verbose_name = 'Товар' #Название модели в единственном числе
		ordering = ['name',]
		index_together = (('id', 'slug'),) # Определяем идекс по двум полям
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_detail', args=[self.id, self.slug])