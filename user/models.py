from django.db import   models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyUser(models.Model):
    class Meta:
        db_table = 'my_user'
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    is_author   = models.BooleanField(default=False)

    def __str__(self):
        return self.id_user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        MyUser.objects.create(id_user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.myuser.save()
