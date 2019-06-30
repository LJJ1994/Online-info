# Generated by Django 2.2.2 on 2019-06-29 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payinfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayinfoOrder',
            fields=[
                ('uid', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('trade_no', models.CharField(max_length=200)),
                ('amount', models.FloatField()),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('is_type', models.SmallIntegerField(default=1)),
                ('status', models.SmallIntegerField(default=1)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payinfo_buyer', to=settings.AUTH_USER_MODEL)),
                ('payinfo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payinfo_order', to='payinfo.PayInfo')),
            ],
        ),
    ]