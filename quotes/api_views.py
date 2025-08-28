from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from .models import Quote, Source
from .serializers import QuoteSerializer
from .forms import AddQuoteForm
from .utils import make_fingerprint, wilson_lower_bound


class RandomQuote(APIView):
    def get(self, request):
        q = Quote.pick_weighted_random()
        if q:
            q.inc_view()
            return Response(QuoteSerializer(q).data)
        return Response({'detail': 'no quotes'}, status=204)


class VoteQuote(APIView):
    def post(self, request, pk: int):
        action = (request.data or {}).get('value')
        q = Quote.objects.filter(pk=pk).first()
        if not q or action not in ('like', 'dislike'):
            return Response({'detail': 'bad request'}, status=400)
        fp = make_fingerprint(request)
        q.apply_vote(fp, action == 'like')
        return Response({'likes': q.likes, 'dislikes': q.dislikes})


class AddQuote(APIView):
    def post(self, request):
        form = AddQuoteForm(request.data)
        if form.is_valid():
            try:
                q = form.save()
                return Response(QuoteSerializer(q).data, status=201)
            except Exception as e:
                return Response({'detail': str(e)}, status=400)
        return Response({'errors': form.errors}, status=400)


class TopQuotes(APIView):
    def get(self, request):
        sort = request.query_params.get('sort', 'likes') 
        limit = int(request.query_params.get('limit', 10))
        qs = Quote.objects.all().select_related('source')
        if sort == 'views':
            qs = qs.order_by('-views', '-likes')[:limit]
            return Response(QuoteSerializer(qs, many=True).data)
        elif sort == 'wilson':
            quotes = list(qs)
            for q in quotes:
                q._wilson = wilson_lower_bound(q.likes, q.dislikes)
            quotes.sort(key=lambda x: x._wilson, reverse=True)
            return Response(QuoteSerializer(quotes[:limit], many=True).data)
        else:
            qs = qs.order_by('-likes', '-views', '-created_at')[:limit]
            return Response(QuoteSerializer(qs, many=True).data)
