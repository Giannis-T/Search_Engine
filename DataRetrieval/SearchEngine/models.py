from django.db import models


class Query(models.Model):
    query = models.CharField(max_length = 64)
    field = models.CharField(max_length = 20)
    
    def __str__(self):
        return f"Query: {self.query}  for Field: {self.field}"
