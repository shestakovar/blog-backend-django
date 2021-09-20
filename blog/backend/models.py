from django.db import models
from django.contrib.auth.models import User
from .managers import PostManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


def custom_save_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.id, ext)
    return os.path.join('img/', filename)


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    objects = PostManager.as_manager()

    def __str__(self):
        return "%s %s" % (self.author, self.title)

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    origin = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" % (self.origin, self.author, self.content)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to=custom_save_path)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


# These two auto-delete files from filesystem when they are unneeded:

@receiver(models.signals.post_delete, sender=UserProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `UserProfile` object is deleted.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


@receiver(models.signals.pre_save, sender=UserProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `UserProfile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = UserProfile.objects.get(pk=instance.pk).avatar
        new_file = instance.avatar
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except (UserProfile.DoesNotExist, ValueError) as e:
        return False
