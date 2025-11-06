from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response


class SearchProducts(APIView):
    def get(self, request):
        q = request.GET.get("q", "")
        products = Product.objects.filter(title__icontains=q)[:20]   # top 20
        return Response(ProductSerializer(products, many=True).data)

class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({"error":"not found"}, status=404)
        
        # similar products → same category, but not same id
        similar_products = Product.objects.filter(category=product.category).exclude(id=pk)[:4]

        return Response({
            "product": ProductSerializer(product).data,
            "similar": ProductSerializer(similar_products, many=True).data
        })

# Create your views here.
class ProductlistView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(trending=True)

    def get_serializer_context(self):
        return {'request': self.request}
    
class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProductsByCategory(APIView):
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)

        products = category.products.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({
            "category": {"id": category.id, "name": category.name, "slug": category.slug},
            "products": serializer.data
        })