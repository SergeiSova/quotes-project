from rest_framework import serializers
from .models import Quote, Source

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', 'type']

class QuoteSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)

    class Meta:
        model = Quote
        fields = ['id', 'text', 'weight', 'views', 'likes', 'dislikes', 'source', 'created_at']
