# Generated by Django 5.1.2 on 2024-10-27 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0002_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="comment",
            name="rate_and_comment_not_null",
        ),
        migrations.AlterUniqueTogether(
            name="comment",
            unique_together=set(),
        ),
    ]
