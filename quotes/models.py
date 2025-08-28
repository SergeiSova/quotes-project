from __future__ import annotations
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.db.models import F
import random


class Source(models.Model):
    TYPE_MOVIE = 'movie'
    TYPE_BOOK = 'book'
    TYPE_OTHER = 'other'
    TYPE_CHOICES = [
        (TYPE_MOVIE, 'Фильм'),
        (TYPE_BOOK, 'Книга'),
        (TYPE_OTHER, 'Другое'),
    ]

    name = models.CharField(max_length=255, unique=True, verbose_name='Источник')
    type = models.CharField(max_length=16, choices=TYPE_CHOICES, default=TYPE_OTHER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class QuoteQuerySet(models.QuerySet):
    def popular(self):
        return self.order_by('-likes', '-views', '-created_at')

    def most_viewed(self):
        return self.order_by('-views', '-likes')


class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='quotes')
    text = models.TextField(unique=True, verbose_name='Текст цитаты')
    weight = models.PositiveIntegerField(default=1, help_text='Чем больше, тем чаще показывается')
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuoteQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=['source']),
        ]
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.text[:60]}… — {self.source.name}'

    def clean(self):
        super().clean()
        if self._state.adding and self.source_id:
            count = Quote.objects.filter(source_id=self.source_id).count()
            if count >= 3:
                raise ValidationError({'source': 'У этого источника уже 3 цитаты. Удалите одну или выберите другой источник.'})

    @classmethod
    def pick_weighted_random(cls) -> 'Quote | None':
        items = list(cls.objects.all().values_list('id', 'weight'))
        if not items:
            return None
        weights = [max(int(w) if w is not None else 0, 0) for _, w in items]
        total = sum(weights)
        if total <= 0:
            chosen_id = random.choice([i for i, _ in items])
        else:
            chosen_id = random.choices([i for i, _ in items], weights=weights, k=1)[0]
        return cls.objects.select_related('source').get(pk=chosen_id)

    def inc_view(self):
        Quote.objects.filter(pk=self.pk).update(views=F('views') + 1)
        self.refresh_from_db(fields=['views'])

    def apply_vote(self, fingerprint: str, is_like: bool):
        """Учесть голос от пользователя с fingerprint. Одно голосование на цитату.
        Если пользователь меняет мнение (лайк->дизлайк или наоборот), корректно пересчитать счётчики.
        """
        from .models import Vote 
        with transaction.atomic():
            vote, created = Vote.objects.select_for_update().get_or_create(
                quote=self, fp=fingerprint, defaults={'is_like': is_like}
            )
            if created:
                if is_like:
                    Quote.objects.filter(pk=self.pk).update(likes=F('likes') + 1)
                else:
                    Quote.objects.filter(pk=self.pk).update(dislikes=F('dislikes') + 1)
            else:
                if vote.is_like != is_like:
                    if is_like:
                        Quote.objects.filter(pk=self.pk).update(likes=F('likes') + 1, dislikes=F('dislikes') - 1)
                    else:
                        Quote.objects.filter(pk=self.pk).update(dislikes=F('dislikes') + 1, likes=F('likes') - 1)
                    vote.is_like = is_like
                    vote.save(update_fields=['is_like'])
                # если тот же самый голос — ничего не делаем
            self.refresh_from_db(fields=['likes', 'dislikes'])


class AppStat(models.Model):
    """Простой key/value для счётчиков страниц."""
    key = models.CharField(max_length=64, unique=True)
    value = models.PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = 'Статистика приложения'
        verbose_name_plural = 'Статистика приложения'

    def __str__(self):
        return f'{self.key}={self.value}'

    @classmethod
    def bump(cls, key: str) -> int:
        obj, _ = cls.objects.get_or_create(key=key, defaults={'value': 0})
        cls.objects.filter(pk=obj.pk).update(value=F('value') + 1)
        obj.refresh_from_db(fields=['value'])
        return obj.value


class Vote(models.Model):
    """Голос пользователя за цитату (антидубли).
    fp — SHA‑256 «отпечаток» (сессия+IP+UA). Уникален в связке с цитатой.
    """
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='votes')
    fp = models.CharField(max_length=64)
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('quote', 'fp'),)
        indexes = [
            models.Index(fields=['quote', 'fp']),
        ]

    def __str__(self):
        return f'Vote(q={self.quote_id}, like={self.is_like})'
