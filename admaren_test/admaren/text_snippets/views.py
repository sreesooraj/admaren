from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Title, Text
from rest_framework.permissions import IsAuthenticated
from . serializers import TextSnippetSerializer, TextUpdateSerializer
from django.conf import settings


class TextSnippetView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):                                   # details related to a single text_snippet using text_id
        params = request.query_params
        try:
            text = Text.objects.get(id=params["text_id"], user=request.user)
            data = {"text": text.text_snippet, "title": text.title.title, "created_at": text.created_at}
            return Response({"status": "success", "data": data})

        except Exception as e:
            return Response({"status": "error", "message": "wrong text id"})

    def post(self, request):                                                    #add title , text by user
        serializer = TextSnippetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        title = Title.objects.filter(title=data["title"])
        if not title:
            title = Title.objects.create(title=data["title"])
        else:
            title = title.first()
        text = Text.objects.create(user=request.user, title=title, text_snippet=data["text"])
        return Response({"status": "success", "message": "text successfully added", "text_id": text.id })

    def put(self, request):                                             #update added text by user
        serializer = TextUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            text = Text.objects.get(id=data["text_id"], user=request.user)
        except Exception as e:
            return Response({"status": "error", "message": "wrong text id"})

        text.text_snippet = data["text"]
        text.save(update_fields=["text_snippet"])
        updated_text_details = {"text": text.text_snippet, "title": text.title.title, "created_at": text.created_at}
        return Response({"status": "success", "message": "success fully updated", "updated_text_details": updated_text_details})

    def delete(self, request):                                         #delete text_snippet by user
        params = request.query_params
        try:
            text = Text.objects.get(id=params["text_id"], user=request.user)
            text.delete()
            return Response({"status": "success", "message": "successfully deleted"})
        except Exception as e:
            return Response({"status": "error", "message": "wrong text id"})


class ListSnippetView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):                                         # list of user text_snippets and total text_snippets count
        text = Text.objects.filter(user=request.user)
        text_snippet_count = text.count()
        snippet_list = [
            {"id": i.id, "title": i.title.title, "text": i.text_snippet, "created_at": i.created_at, "text_details_link": settings.DOMAIN_NAME+"text_snippets/text/?text_id={}".format(i.id)}
            for i in text
        ]
        return Response({"status": "success", "snippet_list": snippet_list, "text_snippet_count": text_snippet_count})


class ListTagView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        params = request.query_params
        tag_id = params.get("tag_id")
        user = request.user
        if tag_id:                                              # returns text_snippets details linked to the selected tag.
            title = Text.objects.filter(user=user, title__id=tag_id).values("text_snippet", "created_at")
            return Response({"status": "success", "tags_details": title})
        else:                                                   #list of user tags
            title = Title.objects.filter(text_title__user=user).values('title', 'id').distinct()
            return Response({"status": "success", "tags_list": title})


