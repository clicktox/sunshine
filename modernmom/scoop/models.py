from django.db import models
from fields import UUIDField
from photologue.models import ImageModel
from fields import UUIDField

class ScoopImage(ImageModel):
    pass

class ScoopItem(models.Model):
    pass

class ScoopTopic(models.Model):
    name = models.CharField(max_length=255)
    uuid = UUIDField()
    pass

