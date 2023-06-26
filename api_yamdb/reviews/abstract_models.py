from django.db import models


class PubDateAbstractModel(models.Model):
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True,
        db_index=True, blank=True
    )

    class Meta:
        abstract = True
