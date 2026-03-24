# Generated manually to add missing columns

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_internship_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='internship',
            name='duration',
            field=models.CharField(max_length=100, default='3 months'),
        ),
        migrations.AddField(
            model_name='internship',
            name='source',
            field=models.CharField(max_length=100, default='Company Website'),
        ),
        migrations.AddField(
            model_name='internship',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userinternship',
            name='start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userinternship',
            name='end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userinternship',
            name='skills_gained',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userinternship',
            name='experience_rating',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userinternship',
            name='would_recommend',
            field=models.BooleanField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='savedinternship',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
