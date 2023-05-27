from django.contrib import admin

from .models import Product, Category, ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class ProductImageInline(admin.StackedInline):
        model=ProductImage
        extra=1
        verbose_name='Изображение товара'
        verbose_name_plural='Изображения товара'
    
    inlines=(ProductImageInline, )
    readonly_fields=('slug', )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...