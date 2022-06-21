from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="user")
    city = models.CharField(max_length=36, null=True, verbose_name="city")
    about = models.TextField(max_length=10000, null=True, verbose_name="about")
    birthday = models.DateField(verbose_name="birthday")
    verify = models.BooleanField(default=False, verbose_name="verification")

    class Meta:
        permissions = (
            ("verified", "Верифицирован"),
        )
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def get_absolute_url(self):
        return f"/user/{self.id}"


class ProfileIcon(models.Model):
    icon = models.ImageField(upload_to="users")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_icon"
