from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Source, Quote

class AddQuoteForm(forms.Form):
    text = forms.CharField(label='Цитата', widget=forms.Textarea(attrs={'rows': 4}), max_length=5000)
    source_name = forms.CharField(label='Источник (фильм/книга и т.п.)', max_length=255)
    source_type = forms.ChoiceField(label='Тип источника', choices=Source.TYPE_CHOICES)
    weight = forms.IntegerField(label='Вес (чем больше — тем чаще)', min_value=0, max_value=1000, initial=1)

    def clean_text(self):
        text = self.cleaned_data['text'].strip()
        if Quote.objects.filter(text__iexact=text).exists():
            raise ValidationError('Такая цитата уже существует (дубликат).')
        return text

    def save(self) -> Quote:
        text = self.cleaned_data['text'].strip()
        source_name = self.cleaned_data['source_name'].strip()
        source_type = self.cleaned_data['source_type']
        weight = int(self.cleaned_data['weight'])

        with transaction.atomic():
            source, _ = Source.objects.select_for_update().get_or_create(name=source_name, defaults={'type': source_type})
            if source.type != source_type:
                source.type = source_type
                source.save(update_fields=['type'])

            if Quote.objects.filter(source=source).count() >= 3:
                raise ValidationError('У этого источника уже 3 цитаты. Удалите одну или выберите другой источник.')

            q = Quote.objects.create(source=source, text=text, weight=max(weight, 0))
        return q
