from django.urls import path
from .views import *

urlpatterns = [
 
    path('trending/',ProductlistView.as_view(),name='trending'),
    path("product/<int:pk>/", ProductDetailView.as_view()),
    path("products/search/", SearchProducts.as_view()),
path("categories/", CategoryList.as_view()),
path("categories/<str:slug>/", ProductsByCategory.as_view()),

]
