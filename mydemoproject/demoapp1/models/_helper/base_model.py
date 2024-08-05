from django.contrib.auth.models import models


# abstract model
class BaseModel(models.Model):
    class Meta:
        abstract = True
