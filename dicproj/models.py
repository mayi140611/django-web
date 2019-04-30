from django.db import models


class Dic(models.Model):
    code = models.CharField(max_length=100, blank=True, default='')
    name = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('code',)


class CsvFile(models.Model):

    file = models.FileField()

    class Meta:
        ordering = ('file',)