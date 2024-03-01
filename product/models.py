from django.db import models
from user.models import User
import math
from django.utils import timezone

from .signals import custom_delete

class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name = 'author_product', verbose_name="Автор")
    title = models.CharField(max_length=255, verbose_name="Название")
    start_time = models.DateTimeField(verbose_name="Дата и время старта")
    price = models.FloatField(verbose_name='Цена')
    min_user = models.IntegerField(verbose_name="Минимальная количество в группе")
    max_user = models.IntegerField(verbose_name="Максимальная количество в группе")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name='product_lesson', verbose_name="Урок")
    title = models.CharField(max_length=255, verbose_name="Название")
    video_link = models.CharField(max_length=255, verbose_name='Ссылка на видео')
    # Если файл находится внутри проекта то:
    # video_link = models.FileField(upload_to='Lessons/')


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name='product_group', verbose_name="Урок")
    title = models.CharField(max_length=255, verbose_name="Название")
    student_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Group, self).save(*args, **kwargs)
            group_create_shuffle(self.product)
        else:
            super(Group, self).save(*args, **kwargs)


class StudentLesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name='product_sl', verbose_name="Урок")
    student = models.ForeignKey(User, on_delete=models.CASCADE, 
                                related_name='student_sl', verbose_name='Студенты')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, 
                              related_name='group_sl', verbose_name='Группа')
    
    def __str__(self):
        return self.student.username + " - " + self.group.title
    
    class Meta:
        verbose_name = 'Студент Продукт'
        verbose_name_plural = 'Студенты Продукты'
        unique_together = ['product', 'student']

    def save(self, *args, **kwargs):
        group = student_group_arrange(self.product)
        if group != -1:
            self.group = group
        # else:
        #     self.group = None
        super(StudentLesson, self).save(*args, **kwargs)

custom_delete(StudentLesson)


def student_group_arrange(product):
    product_groups = Group.objects.filter(product=product)
    min_group = product_groups[0]
    for group in product_groups:
        if min_group.student_count < product.min_user:
            break
        if min_group.student_count > group.student_count:
            min_group = group
    if min_group.student_count < product.max_user:
        min_group.student_count += 1
        min_group.save()
        return min_group
    else:
        return -1

    
def group_create_shuffle(product):
    start_time = product.start_time
    now = timezone.now()
    if now < start_time:
        total_students = 0
        product_groups = Group.objects.filter(product=product)
        for group in product_groups:
            total_students += group.student_count
        avg = math.ceil(total_students / product_groups.count())
        if avg < product.max_user and avg >= product.min_user:
            student_lessons = StudentLesson.objects.filter(product=product)
            for group in product_groups:
                group.student_count = 0
                group.save()
            for student_lesson in student_lessons:
                min_group = product_groups[0]
                for group in product_groups:
                    if min_group.student_count < product.min_user:
                        break
                    if min_group.student_count > group.student_count:
                        min_group = group
                if min_group.student_count < product.max_user:
                    student_lesson.group = group
                    min_group.student_count += 1
                    student_lesson.save()
                    min_group.save()