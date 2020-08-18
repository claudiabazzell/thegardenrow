# Generated by Django 2.2 on 2020-08-18 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garden_row', '0002_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden_row.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden_row.User')),
            ],
        ),
    ]
