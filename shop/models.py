from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from simple_history.models import HistoricalRecords


class Product(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    description = models.CharField(max_length=256, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    count = models.IntegerField(verbose_name='Количество')
    category = models.ManyToManyField('Category', verbose_name='Категория')
    structure = models.ManyToManyField('Component', verbose_name='Составляющие')
    photo = models.ImageField(verbose_name='Изображение')
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name} ({self.price})'

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_id': self.pk})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Component(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Составляющее'
        verbose_name_plural = 'Составляющие'


class Character(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    description = models.CharField(max_length=256, verbose_name='Описание')
    products = models.ManyToManyField('Product', verbose_name='Товары в образе')
    photo = models.ImageField(verbose_name='Изображение')
    user = models.ManyToManyField(User, through='CharacterUserRelationship')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name} (товаров: {self.products_count})'

    @property
    def products_count(self):
        return self.products.count()

    products_count.fget.short_description = 'Количество товаров'

    @property
    def rating(self):
        return self.characteruserrelationship_set.aggregate(Avg('rate'))['rate__avg'] or 'Без оценки'

    rating.fget.short_description = 'Средняя оценка'

    class Meta:
        verbose_name = 'Образ'
        verbose_name_plural = 'Образы'


class CharacterUserRelationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    character = models.ForeignKey('Character', on_delete=models.CASCADE, verbose_name='Образ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления')
    rate = models.IntegerField(verbose_name='Оценка')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Оценка пользователя'
        verbose_name_plural = 'Оценки пользователей'


class Order(models.Model):
    products = models.ManyToManyField('Product', verbose_name='Товары в заказе')
    total = models.IntegerField(verbose_name='Сумма')
    status = models.CharField(max_length=32, verbose_name='Статус', null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    history = HistoricalRecords()

    def __str__(self):
        return f'Заказ #{self.pk} (товары: {self.products_count} шт, сумма: {self.total})'

    def get_absolute_url(self):
        return reverse('order', kwargs={'order_id': self.pk})

    @property
    def products_count(self):
        return self.products.count()

    products_count.fget.short_description = 'Количество товаров'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    count = models.IntegerField(verbose_name='Количество')
    history = HistoricalRecords()

    @property
    def total(self):
        return self.product.price * self.count

    total.fget.short_description = 'Итоговая сумма'

    class Meta:
        verbose_name = 'Лот'
        verbose_name_plural = 'Корзина'


class Advertisement(models.Model):
    title = models.CharField(max_length=64, verbose_name='Заголовок')
    description = models.CharField(max_length=256, verbose_name='Описание')
    photo = models.ImageField(verbose_name='Изображение')
    link = models.CharField(max_length=256, verbose_name='Ссылка на источник')
    author = models.ForeignKey(User, verbose_name='Автор', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    started_at = models.DateTimeField(verbose_name='Дата публикации', null=True)
    archive_at = models.DateTimeField(verbose_name='Дата окончания публикации', null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.title} (Дата истечения: {self.archive_at})'

    class Meta:
        verbose_name = 'Рекламное объявление'
        verbose_name_plural = 'Рекламные объявления'
