from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Модель пользователя, унаследованная от AbstractUser
    """
    USER_TYPE = [
        ('Author', 'Author'),
        ('Student', 'Student'),
    ]
    user_type = models.CharField(max_length=12, choices=USER_TYPE, 
                                 default='Student', verbose_name="Тип пользователя")
    
    def __str__(self):
        return str(self.username)
    
    class Meta:
        verbose_name = 'Ползователь'
        verbose_name_plural = 'Пользователи'