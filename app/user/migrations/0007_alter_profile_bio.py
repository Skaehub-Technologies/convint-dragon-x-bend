# Generated by Django 4.0.6 on 2022-07-20 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0006_alter_profile_bio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
