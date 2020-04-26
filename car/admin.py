from django.contrib import admin

#ADMİN İLE İLGİLİ TÜM YÖNETİM İŞLEMLERİ BURADA GERÇEKLEŞECEK.
# Register your models here.#
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from car.models import Category, Car, Images

class CarImageInline(admin.TabularInline):    #extra istersek 5 satır daha açtık
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image']
    list_filter = ['status']
    readonly_fields = ('image_tag',)


class CarAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'image_tag', 'amount', 'capacity', 'model', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status','category']
    inlines = [CarImageInline]          #yeni ürün eklerkende image galerisi ile beraber bize sunuyor.


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'car', 'image_tag']  #bunlar görünsün dedik ama görünmesi için ImageAdmindeki şablona uy dedik.
    readonly_fields = ('image_tag',)

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Car,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Car,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

admin.site.register(Category, CategoryAdmin2)
admin.site.register(Car,CarAdmin)
admin.site.register(Images,ImagesAdmin)