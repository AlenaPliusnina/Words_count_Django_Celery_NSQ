from django.db import models


class Results(models.Model):
    address = models.CharField(max_length=300, unique=False, null=True)
    words_count = models.IntegerField(unique=False, null=True)
    http_status_code = models.IntegerField(null=True)
    about_error = models.CharField(max_length=256, unique=False, null=True)


class Tasks(models.Model):
    address = models.CharField(max_length=300, unique=False, null=True)
    timestamp = models.DateTimeField()
    http_status = models.IntegerField(default=200)

    NOT_STARTED = 1
    PENDING = 2
    FINISHED = 3

    STATUS_CHOICES = (
        (NOT_STARTED, 'NOT_STARTED'),
        (PENDING, 'PENDING'),
        (FINISHED, 'FINISHED'),
    )

    task_status = models.PositiveBigIntegerField(choices=STATUS_CHOICES, default=NOT_STARTED)

