from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import permissions,generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import *
from django.utils import timezone
from rest_framework import status

from decimal import Decimal



# Cart Views
class CartListCreateView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_serializer_context(self):
        return {'request': self.request}


class CartDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        item = Cart.objects.get(id=pk, user=request.user)
        item.delete()
        return Response({"msg": "deleted"})

class CartUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        qty = request.data.get("quantity")
        item = Cart.objects.get(id=pk, user=request.user)
        item.quantity = qty
        item.save()
        return Response({"msg": "updated"})

# Checkout
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        try:
            total_price = sum(Decimal(item.product.price) * item.quantity for item in cart_items)
            order = Order.objects.create(user=user, total_price=total_price)
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            cart_items.delete()
            return Response({"msg": "Order placed successfully!"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
# Direct Order (without cart)
# Direct Order (without cart)

class DirectOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("DIRECT ORDER HIT")  # <-- DEBUG
        print("DATA = ", request.data)  # <-- DEBUG

        user = request.user
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"error": "Product ID required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        total_price = Decimal(product.price) * quantity

        order = Order.objects.create(user=user, total_price=total_price)

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=Decimal(product.price),
        )

        return Response({"msg": "Order placed successfully", "order_id": order.id}, status=200)



# User Orders
class UserOrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
        data = []
        for o in orders:
            items = []
            for i in o.items.all():
                items.append({
                    "id": i.id,
                    "product": {
                        "id": i.product.id,
                        "title": i.product.title,
                        "price": str(i.price),
                        "image": request.build_absolute_uri(i.product.image.url)
                    },
                    "quantity": i.quantity
                })
            data.append({
                "id": o.id,
                "order_at": o.order_at,
                "items": items
            })
        return Response(data)

# Update Order Item
class UpdateOrderItem(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        order_id = request.data.get("order")
        product_id = request.data.get("product")
        qty = request.data.get("quantity")
        item = OrderItem.objects.get(order_id=order_id, product_id=product_id)
        item.quantity = qty
        item.save()
        return Response({"msg": "updated"})

# Remove Order Item
class RemoveOrderItem(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        order_id = request.data.get("order")
        product_id = request.data.get("product")
        OrderItem.objects.filter(order_id=order_id, product_id=product_id).delete()
        return Response({"msg": "item removed"})

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        order_id = request.data.get("order")

        if not order_id:
            return Response({"error": "order id required"}, status=400)

        Order.objects.filter(id=order_id, user=request.user).delete()

        return Response({"msg": "order cancelled"})
