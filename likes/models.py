from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models


# Create your models here
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        index_together = ('content_type', 'object_id')
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user} likes {self.content_object}'
