# Generated by Django 2.2.2 on 2019-06-29 04:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_courseorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorder',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='course_order', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='courseorder',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='course_order', to='course.Course'),
        ),
    ]