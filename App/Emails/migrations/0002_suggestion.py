# Generated by Django 4.0 on 2022-04-17 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_profile'),
        ('Emails', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('S', 'Suggestion'), ('B', 'Bug'), ('E', 'Error'), ('O', 'Other')], default='S', max_length=100)),
                ('header', models.CharField(max_length=100, null=True)),
                ('to', models.TextField(null=True)),
                ('sent_date', models.DateTimeField(null=True)),
                ('was_sent', models.BooleanField(default=False, editable=False)),
                ('blocks', models.ManyToManyField(related_name='%(class)s_blocks', to='Emails.Block')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggestion', to='Users.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
