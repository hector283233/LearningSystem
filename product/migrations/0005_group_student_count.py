# Generated by Django 5.0.2 on 2024-02-29 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_studentlesson_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='student_count',
            field=models.IntegerField(default=0),
        ),
    ]