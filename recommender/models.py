from django.db import models

# Create your models here.
class Similarity(models.Model):
    created = models.DateField()
    source = models.CharField(max_length=16, db_index=True)
    target = models.CharField(max_length=16)
    similarity = models.DecimalField(max_digits=8, decimal_places=7)

    def __str__(self):
        return "[({} => {}) sim = {}]".format(self.source,
                                              self.target,
                                              self.similarity)
    """
    class Meta:
        db_table = 'similarity'
    """