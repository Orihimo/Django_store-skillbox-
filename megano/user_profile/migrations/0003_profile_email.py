# Generated by Django 4.2.2 on 2023-07-02 04:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_profile", "0002_alter_profile_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, null=True, verbose_name="Email"
            ),
        ),
    ]