# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20260323_2230'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='internship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=200, default='Remote')),
                ('duration', models.CharField(max_length=100, default='3 months')),
                ('stipend', models.CharField(max_length=100, blank=True, default='Unpaid')),
                ('requirements', models.TextField(blank=True)),
                ('skills_required', models.TextField(blank=True)),
                ('application_url', models.URLField(blank=True)),
                ('source', models.CharField(max_length=100, default='Company Website')),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(max_length=20, default='active')),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Internship',
                'verbose_name_plural': 'Internships',
                'ordering': ['-posted_date', '-is_featured'],
            },
        ),
        migrations.CreateModel(
            name='userinternship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='internships', to='accounts.user')),
                ('internship', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='enrollments', to='core.internship')),
                ('status', models.CharField(default='enrolled', max_length=20)),
                ('enrollment_date', models.DateTimeField(auto_now_add=True)),
                ('completion_date', models.DateTimeField(blank=True, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('skills_gained', models.TextField(blank=True)),
                ('experience_rating', models.IntegerField(blank=True, null=True)),
                ('would_recommend', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'User Internship',
                'verbose_name_plural': 'User Internships',
                'ordering': ['-enrollment_date'],
                'unique_together': {('user', 'internship')},
            },
        ),
        migrations.CreateModel(
            name='savedinternship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='saved_internships', to='accounts.user')),
                ('internship', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='saved_by', to='core.internship')),
                ('saved_date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Saved Internship',
                'verbose_name_plural': 'Saved Internships',
                'ordering': ['-saved_date'],
                'unique_together': {('user', 'internship')},
            },
        ),
    ]
