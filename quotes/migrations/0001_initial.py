import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64, unique=True)),
                ('value', models.PositiveBigIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Статистика приложения',
                'verbose_name_plural': 'Статистика приложения',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Источник')),
                ('type', models.CharField(choices=[('movie', 'Фильм'), ('book', 'Книга'), ('other', 'Другое')], default='other', max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(unique=True, verbose_name='Текст цитаты')),
                ('weight', models.PositiveIntegerField(default=1, help_text='Чем больше, тем чаще показывается')),
                ('views', models.PositiveIntegerField(default=0)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('dislikes', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='quotes.source')),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['source'], name='quotes_quot_source__85b688_idx')],
            },
        ),
    ]
