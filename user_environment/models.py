from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.urls import reverse


class Ticket(models.Model):

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('env:upd-ticket', kwargs={'pk': self.pk})


class Review(models.Model):

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)

    title_review = models.CharField(max_length=128)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    details = models.TextField(max_length=8192, blank=True)

    time_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('env:upd-review', kwargs={'pk': self.pk})


class Follow(models.Model):

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user',)
