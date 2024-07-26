from django.contrib.auth.models import models


# abstract model
class BaseModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def filter_objects(cls, **kwargs):
        return cls.objects.filter(**kwargs)

    @classmethod
    def get_first(cls, **kwargs):
        return cls.objects.filter(**kwargs).first()
