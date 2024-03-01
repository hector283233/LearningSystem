from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('product/', include('api.product.urls')),
]
