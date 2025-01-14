from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    # category and sub category
    # when the null is true it means its a parent category
    parent = models.ForeignKey('self', verbose_name=('parent'),  blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=50)
    description = models.TextField(_("description"), blank=True)
    avatar = models.ImageField("Coverpic", blank=True, upload_to="categories/")
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.title
    


class Product(models.Model):
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_("description"), blank=True)
    avatar = models.ImageField("avatar", blank=True, upload_to="products/")
    is_enable = models.BooleanField(_('is enable'), default=True)
    categories = models.ManyToManyField('Category', verbose_name=_('categories'), blank=True)
    created_time = models.DateTimeField(_('created time') ,auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time') ,auto_now=True)
    
    def __str__(self):
        return self.title


class Meta:
    db_table = 'products'
    verbose_name = 'product'
    verbose_name_plural = 'products'


class File(models.Model):
    FILE_AUDIO = 1
    FILE_VIDEO = 2
    FILE_PDF = 3
    FILE_TYPES = (
        (FILE_AUDIO, 'audio'),
        (FILE_VIDEO, 'video'),
        (FILE_PDF, 'pdf')
    )
    
    # adding related_name to product field will show us linked files to our product
    product = models.ForeignKey('Product', related_name='files', verbose_name=_('product'), on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    file_type = models.SmallIntegerField('file_type', choices=FILE_TYPES)
    # upload to: creates directories
    file = models.FileField(_('file'), upload_to='files/%Y/%m/%d/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created time') ,auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time') ,auto_now=True)


class Meta:
    db_table = 'files'
    verbose_name = 'file'
    verbose_name_plural = 'files'
    
    def __str__(self):
        return self.title
    
    

# Create your models here.
