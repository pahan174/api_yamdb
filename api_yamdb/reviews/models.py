from django.db import models
from users.models import CustomUser


class Titles(models.Model):
    pass


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews'
    )


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments')
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
