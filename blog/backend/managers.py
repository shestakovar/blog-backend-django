from django.db import models


class PostManager(models.QuerySet):
    def author(self, user):
        return self.filter(author=user)
