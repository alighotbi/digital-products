from rest_framework import serializers

from .models import Product, Category, File

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'description', 'avatar', 'url')
    
    
class FileSerializer(serializers.ModelSerializer):
    file_type = serializers.SerializerMethodField()
    
    class Meta:
        model = File
        fields = ('id','title', 'file', 'file_type')
        
    def get_file_type(self, obj):
        return obj.get_file_type_display()
        
        
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True)
   
    files = FileSerializer(many=True)
    
    class Meta:
        model = Product
        # adding 'file_set' parameter to feilds in this serializer shows us linked file to our product
        fields = ('id', 'title', 'description', 'avatar', 'categories', 'files', 'url')
        