# Generated by Django 3.0.5 on 2020-05-10 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20)),
                ('user', models.CharField(default='anonymous', max_length=20)),
                ('date', models.DateTimeField(verbose_name='date when the searching request is submitted')),
            ],
        ),
    ]
