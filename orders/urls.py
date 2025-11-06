from django.urls import path
from .views import *

urlpatterns = [
    path("cart/", CartListCreateView.as_view(), name="cart"),
    path("cart/<int:pk>/", CartDeleteView.as_view(), name="cart-delete"),
    path("cart/<int:pk>/update/", CartUpdateView.as_view(), name="cart-update"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("direct-order/", DirectOrderView.as_view(), name="direct-order"),
    path("myorders/", UserOrderListView.as_view(), name="my-orders"),
    path("cancel_order/", CancelOrderView.as_view(), name="cancel-order"),
    path("update_item/", UpdateOrderItem.as_view(), name="update-order-item"),
    path("remove_item/", RemoveOrderItem.as_view(), name="remove-order-item"),
]
