# Generated by Django 2.1 on 2019-09-28 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hcat', '0010_auto_20190925_1817'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grant',
            options={'verbose_name': 'x grant'},
        ),
        migrations.AlterModelOptions(
            name='wrangler',
            options={'verbose_name': 'x wrangler'},
        ),
    ]