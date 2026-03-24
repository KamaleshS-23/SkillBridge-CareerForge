# Generated migration for AptitudeTestResult only

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_add_aptitude_test_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='AptitudeTestResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_date', models.DateTimeField(auto_now_add=True)),
                ('quantitative_score', models.IntegerField(default=0)),
                ('verbal_score', models.IntegerField(default=0)),
                ('logical_score', models.IntegerField(default=0)),
                ('data_interpretation_score', models.IntegerField(default=0)),
                ('abstract_reasoning_score', models.IntegerField(default=0)),
                ('total_score', models.IntegerField(default=0)),
                ('max_score', models.IntegerField(default=0)),
                ('percentage', models.FloatField(default=0.0)),
                ('time_taken', models.DurationField(help_text='Time taken to complete the test')),
                ('difficulty_level', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard'), ('mixed', 'Mixed')], default='mixed', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'verbose_name': 'Aptitude Test Result',
                'verbose_name_plural': 'Aptitude Test Results',
                'ordering': ['-test_date'],
            },
        ),
    ]
