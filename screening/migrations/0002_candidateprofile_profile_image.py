from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('screening', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/default.png', upload_to='profile_images/'),
        ),
    ] 