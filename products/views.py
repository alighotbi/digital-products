from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Category, Product, File
from .serializers import ProductSerializer, CategorySerializer, FileSerializer

class ProductListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        products = Product.objects.all()
        # adding context to view, makes an absolute path for the media 
        serializer = ProductSerializer(products, many=True, context ={'request':request})
        return Response(serializer.data)

class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # adding context to view, makes an absolute path for the media 
        serializer = ProductSerializer(product, context={'request':request})
        return Response(serializer.data)
    

class CategoryListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request':request})
        return Response(serializer.data)
    

class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category, context={'request':request})
        return  Response(serializer.data)
    

class FileListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, product_id):
        files = File.objects.filter(product_id=product_id)
        serializer = FileSerializer(files, many=True, context={'request':request})
        return Response(serializer.data)
    

class FileDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk, product_id):
        try:
            files = File.objects.get(pk=pk, product_id=product_id)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FileSerializer(files, context={'request':request})
        return Response(serializer.data)
        
# Create your views here.
