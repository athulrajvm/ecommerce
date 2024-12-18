# Generated by Django 5.1.3 on 2024-11-22 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_app', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productname', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField(null=True)),
                ('image', models.FileField(null=True, upload_to='image/')),
            ],
        ),
    ]
