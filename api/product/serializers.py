from rest_framework import serializers
from product.models import *

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'user_type']

class ProductListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    lessons = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'start_time', 'lessons', 'groups', 'author']

    def get_lessons(self, obj):
        lesson_count = Lesson.objects.filter(product=obj).count()
        return lesson_count
    
    def get_groups(self, obj):
        group_count = Group.objects.filter(product=obj).count()
        return group_count

class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_link']

class ProductDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    lessons = LessonsSerializer(source='product_lesson', many=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'start_time', 'author', 'lessons']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'user_type']

class StudentProductSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()
    group = serializers.CharField(source='group.title')
    class Meta:
        model = StudentLesson
        fields = ['product', 'group']

class PrdouctStatisticsSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()
    groups_percentage = serializers.SerializerMethodField()
    course_percentage = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'start_time', 
                  'students', 'groups_percentage', 'course_percentage']

    # Количество учеников занимающихся на продукте.
    def get_students(self, obj):
        students_count = StudentLesson.objects.filter(product=obj).count()
        return students_count
    
    # На сколько % заполнены группы
    def get_groups_percentage(self, obj):
        groups = Group.objects.filter(product=obj)
        students_count = StudentLesson.objects.filter(product=obj).count()
        groups_avg = students_count/groups.count()
        groups_percentage = round((groups_avg/obj.max_user)*100, 2)
        return groups_percentage
    
    # Процент приобретения продукта
    def get_course_percentage(self, obj):
        students_count = StudentLesson.objects.filter(product=obj).count()
        total_students = User.objects.filter(user_type='Student').count()
        course_percentage = round((students_count/total_students)*100, 2)
        return course_percentage