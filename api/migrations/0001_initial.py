from django.db import migrations
from api.user.models import CustomUser

class Migration(migrations.Migration):
    def seed_data(apps, scheme_editor):
        user = CustomUser(name="Zayidu", email="zayidu11@gmail.com", is_staff=True, is_superuser=True, phone="9003765148", gender="Male")
        user.set_password("ZAID1234")
        user.save()

    dependencies = [
    ]

    operations = [
        migrations.RunPython(seed_data), 
    ]