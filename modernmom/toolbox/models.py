from django.db import models
from photologue.models import ImageModel
from fields import UUIDField


class Image(ImageModel):
    uuid = UUIDField()


class Download(models.Model):
    name = models.CharField(max_length=255)
    uuid = UUIDField()
    description = models.TextField()
    file = models.FileField(upload_to='uploads/%Y/%m/%d')
    type = models.CharField(max_length=255)
    image = models.ForeignKey(Image)
    priority = models.IntegerField(default=0)
    
    def get_download_type(self):
        #return type based on file extension...
        #self.file.name.
        pass
    
    