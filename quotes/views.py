from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import models
from .models import Quote, AppStat
from .forms import AddQuoteForm
from .utils import make_fingerprint, wilson_lower_bound

HOME_STAT_KEY = 'home_page_views'


def home(request):
    page_views = AppStat.bump(HOME_STAT_KEY)
    quote = Quote.pick_weighted_random()
    if quote:
        quote.inc_view()
    context = {
        'page_views': page_views,
        'quote': quote,
    }
    return render(request, 'quotes/home.html', context)


def add_quote(request):
    if request.method == 'POST':
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Цитата добавлена!')
                return redirect('quotes:home')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = AddQuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})


def top_quotes(request):
    qs = Quote.objects.all().select_related('source')

    t = request.GET.get('type')
    if t:
        qs = qs.filter(source__type=t)
    s = request.GET.get('source')
    if s:
        qs = qs.filter(source__name__icontains=s)

    top10 = qs.order_by('-likes', '-views', '-created_at')[:10]

    with_scores = []
    for q in qs:
        score = wilson_lower_bound(q.likes, q.dislikes)
        q.wilson = score
        with_scores.append(q)
    top_wilson = sorted(with_scores, key=lambda x: x.wilson, reverse=True)[:10]

    most_viewed = qs.order_by('-views', '-likes')[:10]

    by_sources = (
        qs.values('source__name')
          .order_by('source__name')
          .annotate(total_likes=models.Sum('likes'), total_dislikes=models.Sum('dislikes'), total_views=models.Sum('views'), cnt=models.Count('id'))
    )

    return render(request, 'quotes/top.html', {
        'top10': top10,
        'top_wilson': top_wilson,
        'most_viewed': most_viewed,
        'by_sources': by_sources,
        'filter_type': t or '',
        'filter_source': s or '',
    })


@require_POST
def like_quote(request, pk: int):
    quote = Quote.objects.filter(pk=pk).first()
    if not quote:
        raise Http404
    fp = make_fingerprint(request)
    quote.apply_vote(fp, True)
    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})


@require_POST
def dislike_quote(request, pk: int):
    quote = Quote.objects.filter(pk=pk).first()
    if not quote:
        raise Http404
    fp = make_fingerprint(request)
    quote.apply_vote(fp, False)
    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})
