from django.db import models


class Reviews(models.Model):
    # Заглушка, планируется ForeignKey с Title
    title_id = models.IntegerField()
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.PositiveIntegerField(verbose_name="ID автора")
    # Заглушка, реализация рейтинга после создания всех моделей
    score = models.IntegerField()
    pub_date = models.DateTimeField(verbose_name="Дата публикации")

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']

    def __str__(self):
        return f"Отзыв {self.id} на {self.title.name} ({self.score}/10)"
