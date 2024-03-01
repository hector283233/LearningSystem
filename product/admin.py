from django.contrib import admin
from .models import Product, Lesson, Group, StudentLesson

class GroupAdmin(admin.ModelAdmin):
    model = Group
    readonly_fields = ('student_count',)

class StudentLessonAdmin(admin.ModelAdmin):
    model = StudentLesson
    readonly_fields = ('group', )

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Group, GroupAdmin)
admin.site.register(StudentLesson, StudentLessonAdmin)