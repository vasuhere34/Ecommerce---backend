from rest_framework import serializers
from .models import Cart, Order, OrderItem
from products.models import *
from products.serializers import *


class CartSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    class Meta:
        model = Cart
        fields = ['id', 'quantity', 'product']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['product'] = ProductSerializer(instance.product, context=self.context).data
        return rep



class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]

    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "title": obj.product.title,
            "price": str(obj.price),
            "image": self.context['request'].build_absolute_uri(obj.product.image.url)
        }

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ["id", "user", "total_price", "order_at", "items"]
