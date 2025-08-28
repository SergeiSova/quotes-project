import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fp', models.CharField(max_length=64)),
                ('is_like', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='quotes.quote')),
            ],
            options={
                'indexes': [models.Index(fields=['quote', 'fp'], name='quotes_vote_quote_i_91994e_idx')],
                'unique_together': {('quote', 'fp')},
            },
        ),
    ]
