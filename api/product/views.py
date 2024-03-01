from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (ProductListSerializer, ProductDetailSerializer, 
                          PrdouctStatisticsSerializer, StudentProductSerializer)
from product.models import Product, StudentLesson

def has_permission(user, product):
    """
    Функция принятия решения о том, имеет ли студент доступ к курсу
    """
    student_lesson = StudentLesson.objects.filter(product=product, student=user)
    if student_lesson:
        return True
    return False

class Products(APIView):
    @swagger_auto_schema(
            operation_summary='Все доступные продукты',
            responses={200: ProductListSerializer}
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response({"response": "success", "data": serializer.data},
                        status=status.HTTP_200_OK)
    
class ProductDetail(APIView):
    permission_classes = [IsAuthenticated] # Проверка подлинности пользователя
    @swagger_auto_schema(
            operation_summary='Сведения о продукте, к которым у учащегося есть доступ',
            responses={200: ProductDetailSerializer}
    )
    def get(self, request, pk):
        user = request.user
        if Product.objects.filter(pk=pk).exists(): # Проверяем, существует ли продукт
            product = Product.objects.get(pk=pk)
            if has_permission(user, product):
                serializer = ProductDetailSerializer(product)
                return Response({"response":"success", "data": serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({"response":"error", "message": "Вы не имеете права доступа к этой информации"}, 
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"response":"error", "message": "Объект не существует"},
                            status=status.HTTP_404_NOT_FOUND)
        
# Я не до конца понял задачу, поэтому решил сделать и ту, что ниже  
# Список всех продуктов, к которым у учащегося есть доступ, 
# и название группы, к которой принадлежит учащийся.         
class StudentProductList(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            operation_summary='Список всех продуктов, к которым у учащегося есть доступ',
            responses={200: StudentProductSerializer}
    )
    def get(self, request):
        user = request.user
        user_products = StudentLesson.objects.filter(student=user)
        serializer = StudentProductSerializer(user_products, many=True)
        return Response({"response":"success", "data": serializer.data}, 
                        status=status.HTTP_200_OK)
        
class ProductStatistics(APIView):
    @swagger_auto_schema(
            operation_summary='Статистика продукта',
            responses={200: PrdouctStatisticsSerializer}
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = PrdouctStatisticsSerializer(products, many=True)
        return Response({"response":"success", "data": serializer.data},
                        status=status.HTTP_200_OK)