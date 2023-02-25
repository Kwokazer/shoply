from django.contrib import admin
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

from .models import *

# Register your models here.

User.add_to_class('__str__', lambda self: f"{self.username} ({self.first_name} {self.last_name})")


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'preview', 'price', 'count')
    list_display_links = ('id', 'name', 'price')
    search_fields = ('id', 'name', 'description', 'price')
    filter_horizontal = ('structure', 'category')
    readonly_fields = ('preview',)

    def preview(self, obj):
        url = reverse("admin:shop_product_change", args=(obj.id,))
        return mark_safe(f'<a href="{url}"><img width="150px" src="/media/{obj.photo}"/></a>')

    preview.short_description = 'Превью'


class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_products_count')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    readonly_fields = ('get_products_count',)

    def get_products_count(self, obj):
        count = obj.product_set.count()
        url = (
                reverse("admin:shop_product_changelist")
                + "?"
                + urlencode({"structure__id__exact": f"{obj.id}"})
        )

        return mark_safe(f'{count} <a href="{url}" target="_blank">(просмотреть все)</a>')

    get_products_count.short_description = 'Количество товаров'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_products_count')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    readonly_fields = ('get_products_count',)

    def get_products_count(self, obj):
        count = obj.product_set.count()
        url = (
                reverse("admin:shop_product_changelist")
                + "?"
                + urlencode({"category__id__exact": f"{obj.id}"})
        )

        return mark_safe(f'{count} <a href="{url}" target="_blank">(просмотреть все)</a>')

    get_products_count.short_description = 'Количество товаров'


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'products_count', 'rating', 'preview', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'description')
    readonly_fields = ('preview', 'created_at')
    list_filter = ('created_at',)
    filter_horizontal = ('products', 'user')

    def preview(self, obj):
        url = reverse("admin:shop_character_change", args=(obj.id,))
        return mark_safe(f'<a href="{url}"><img width="150px" src="/media/{obj.photo}"/></a>')

    preview.short_description = 'Превью'


class CharacterUserRelationshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'get_character', 'rate')
    list_display_links = ('id', 'rate')
    list_filter = ('created_at', 'rate')
    autocomplete_fields = ('user', 'character')

    def author(self, obj):
        if obj.user:
            url = reverse("admin:auth_user_change", args=(obj.user.id,))
            return mark_safe(f'<a href="{url}" target="_blank">{obj.user}</a>')
        return 'Без пользователя'

    author.short_description = 'Пользователь'

    def get_character(self, obj):
        url = reverse("admin:shop_character_change", args=(obj.character.id,))
        return mark_safe(f'{obj.character} <a href="{url}" target="_blank">(просмотреть образ)</a>')

    get_character.short_description = 'Образ'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total', 'author', 'products_count', 'created_at')
    list_display_links = ('id', 'total', 'created_at')
    list_filter = ('created_at',)
    filter_horizontal = ('products',)
    autocomplete_fields = ['user']

    def author(self, obj):
        if obj.user:
            url = reverse("admin:auth_user_change", args=(obj.user.id,))
            return mark_safe(f'<a href="{url}" target="_blank">{obj.user}</a>')
        return 'Без пользователя'

    author.short_description = 'Пользователь'


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_author', 'preview', 'started_at', 'archive_at')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'description', 'link')
    list_filter = ('started_at', 'archive_at')
    readonly_fields = ('preview', 'created_at')
    autocomplete_fields = ('author',)

    def get_author(self, obj):
        if obj.author:
            url = reverse("admin:auth_user_change", args=(obj.author.id,))
            return mark_safe(f'<a href="{url}" target="_blank">{obj.author}</a>')
        return 'Без автора'

    get_author.short_description = 'Автор'

    def preview(self, obj):
        url = reverse("admin:shop_advertisement_change", args=(obj.id,))
        return mark_safe(f'<a href="{url}"><img width="150px" src="/media/{obj.photo}"/></a>')

    preview.short_description = 'Превью'


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'count', 'total', 'author')
    list_display_links = ('id', 'product', 'count')
    readonly_fields = ('total',)
    autocomplete_fields = ['product', 'user']

    def author(self, obj):
        if obj.user:
            url = reverse("admin:auth_user_change", args=(obj.user.id,))
            return mark_safe(f'<a href="{url}" target="_blank">{obj.user}</a>')
        return 'Без пользователя'

    author.short_description = 'Пользователь'


admin.site.register(Cart, CartAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CharacterUserRelationship, CharacterUserRelationshipAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Product, ProductAdmin)
