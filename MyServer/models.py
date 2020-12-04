from django.db import models

# Create your models here.

class Links(models.Model):
	short_url = models.CharField(max_length = 20)
	redirect_url = models.TextField()
	tracking_url = models.CharField(max_length = 20)


class TrackingData(models.Model):
	tracking_url = models.CharField(max_length=20)
	short_url = models.CharField(max_length=20)
	ip_address = models.TextField()
	browser = models.TextField()
	os = models.TextField()
	device_type = models.TextField()
	device = models.TextField()
	time = models.TextField()
