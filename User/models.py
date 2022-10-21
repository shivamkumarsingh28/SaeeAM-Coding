from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from PIL import Image


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    resume = models.FileField(upload_to="Resume", null=True)
    describe = RichTextField(default='Describe About Your Self ', config_name='awesome_ckeditor')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, ** kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
