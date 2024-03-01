from django.urls import path

from . views import Products, ProductDetail, ProductStatistics, StudentProductList

urlpatterns = [
    path('list/', Products.as_view(), name='products'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('student-products/', StudentProductList.as_view(), name='student-products'),
    path('statistics/', ProductStatistics.as_view(), name='product-statistics'),
]