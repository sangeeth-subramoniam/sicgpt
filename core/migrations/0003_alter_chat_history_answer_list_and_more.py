# Generated by Django 5.0 on 2024-01-10 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_chat_history_items_chat_history_answer_list_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat_history',
            name='answer_list',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='chat_history',
            name='question_list',
            field=models.TextField(blank=True),
        ),
    ]
