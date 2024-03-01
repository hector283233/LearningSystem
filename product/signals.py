from django.dispatch import receiver
from django.db.models.signals import pre_delete

def custom_delete(obj):
    @receiver(pre_delete, sender=obj)
    def decrement_student_count(sender, instance, **kwargs):
        group = instance.group
        group.student_count -= 1
        group.save()