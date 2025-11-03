from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    points = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name}'s profile"

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    image = models.ImageField(upload_to='report_images/', blank=False, null=False)
    description = models.TextField(blank=False)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    water_classification = models.CharField(max_length=50, choices=[
        ('Air_bersih', 'Air Bersih'),
        ('Air_kotor', 'Air Kotor')
    ], blank=True, null=True)
    forest_classification = models.CharField(max_length=50, choices=[
        ('fire', 'Fire'),
        ('non_fire', 'Non Fire')
    ], blank=True, null=True)
    public_fire_classification = models.CharField(max_length=50, choices=[
        ('fire', 'Fire'),
        ('no_fire', 'No Fire')
    ], blank=True, null=True)
    trash_classification = models.CharField(max_length=50, choices=[
        ('banyak_sampah', 'Banyak Sampah'),
        ('sedikit_sampah', 'Sedikit Sampah')
    ], blank=True, null=True)
    illegal_logging_classification = models.CharField(max_length=50, choices=[
        ('penebangan_liar', 'Penebangan Liar'),
        ('tidak_penebangan_liar', 'Tidak Penebangan Liar')
    ], blank=True, null=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report by {self.user.name} - {self.description[:50]}"
