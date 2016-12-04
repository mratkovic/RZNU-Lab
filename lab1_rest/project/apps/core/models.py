from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __unicode__(self):
        return '%s %s' % (self.name, self.email)

class Photo(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="photos/", max_length=255)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

    def __unicode__(self):
        return '%s %s' % (self.title, self.user.name)


    def delete(self,*args,**kwargs):
        import os
        if os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super(Photo, self).delete(*args,**kwargs)





