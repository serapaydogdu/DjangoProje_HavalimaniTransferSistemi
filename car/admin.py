from django.contrib import admin

#ADMİN İLE İLGİLİ TÜM YÖNETİM İŞLEMLERİ BURADA GERÇEKLEŞECEK.
# Register your models here.
from car.models import Category, Car, Images

class CarImageInline(admin.TabularInline):    #extra istersek 5 satır daha açtık
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','status','image']
    list_filter = ['status']
    readonly_fields = ('image_tag',)


class CarAdmin(admin.ModelAdmin):
    list_display = ['title','category','price','image_tag','amount','capacity','model', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status','category']
    inlines = [CarImageInline]          #yeni ürün eklerkende image galerisi ile beraber bize sunuyor.


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','car','image_tag']  #bunlar görünsün dedik ama görünmesi için ImageAdmindeki şablona uy dedik.
    readonly_fields = ('image_tag',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Car,CarAdmin)
admin.site.register(Images,ImagesAdmin)