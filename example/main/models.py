import os

from django.db import models
from django.contrib.auth.models import User


def generate_path(instance, filename):
	return os.path.join(
		"perfiles", "perfil_" + str(instance.iduser_id), filename
	)


class Perfil(models.Model):

	idprofile = models.AutoField(primary_key=True)
	iduser = models.ForeignKey(User, db_index=True)
	photo = models.FileField(
				upload_to=generate_path, null=True, blank=True,
			)
	location = models.CharField(max_length=200, null=True)
	company = models.CharField(max_length=150, null=True)
	about = models.TextField(blank=True, null=True)