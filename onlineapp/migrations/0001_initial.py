# Generated by Django 2.2.1 on 2019-06-06 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('location', models.CharField(max_length=64)),
                ('acronym', models.TextField(max_length=8)),
                ('contact', models.EmailField(max_length=64)),
            ],
        ),
    ]
