# Generated by Django 3.1 on 2020-08-06 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('miner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.PositiveIntegerField()),
                ('reposts', models.PositiveIntegerField()),
                ('likes', models.PositiveIntegerField()),
                ('creationDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tweeter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=15)),
                ('company', models.CharField(max_length=48)),
                ('active', models.BooleanField()),
                ('records', models.PositiveIntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Miner',
        ),
        migrations.AddField(
            model_name='tweet',
            name='tweeter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miner.tweeter'),
        ),
    ]
