from rest_framework import serializers


class TextSnippetSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    text = serializers.CharField(required=True)


class TextUpdateSerializer(serializers.Serializer):
    text_id = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True)