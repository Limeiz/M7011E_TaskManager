# Generated by Django 4.2.7 on 2023-11-13 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="group_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="groupentry",
            name="groupentry_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="list",
            name="list_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="listentry",
            name="listentry_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="reminder",
            name="reminder_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="sharedlist",
            name="sharedlist_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="task",
            name="deadline",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="file",
            field=models.FileField(blank=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="task",
            name="note",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                blank=True,
                choices=[("l", "Low"), ("m", "Medium"), ("h", "High")],
                help_text="Task priority",
                max_length=1,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="task_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="user_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
