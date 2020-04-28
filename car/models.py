from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=100,unique=True)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True,upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    parent = TreeForeignKey('self',blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' >> '.join(full_path[::-1])

    def image_tag(self):    #image ı gösterebilmek için yaptık.urls ede ekleme yaptık.<img src="{}" height="50"/> bu yapı image_tag adında html oluşturuyor.
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Car(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #relation with Category table.
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    marka = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    capacity = models.CharField(max_length=30)
    detail = RichTextUploadingField()
    slug = models.SlugField(blank=True, max_length=150)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):    #image ı gösterebilmek için yaptık.urls ede ekleme yaptık.<img src="{}" height="50"/> bu yapı image_tag adında html oluşturuyor.
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Images(models.Model):
    car=models.ForeignKey(Car,on_delete=models.CASCADE)  #biz product yani car dedik kendisi gidip birincil anahtarı oluşturuyor car_id yi.
    title = models.CharField(max_length=50,blank=True)   #etiket title zorunlu değil blank=True ilr yapıyoruz.
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title   #bu fonksiyon title ın adını döndürüyor. save edilince kayıta.

    def image_tag(self):    #image ı gösterebilmek için yaptık.urls ede ekleme yaptık.<img src="{}" height="50"/> bu yapı image_tag adında html oluşturuyor.
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    car = models.ForeignKey(Car,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=200, blank=True)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment','rate']