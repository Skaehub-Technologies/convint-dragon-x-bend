# Generated by Django 4.0.5 on 2022-06-26 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_alter_user_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(blank=True, upload_to=""),
        ),
    ]
