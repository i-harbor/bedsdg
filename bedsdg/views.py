from django.shortcuts import render, redirect, reverse
from django.utils.translation import get_language
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page

from article.models import Publication, Article


def index(request):
    return redirect(to=reverse('home'))


# @cache_page(60*2)
def home(request):
    limit = 6       # 最多展示数量

    lang_code = get_language()
    lang = Article.get_lang_value_by_code(lang_code=lang_code)
    prefetch = Prefetch('article_set', queryset=Article.objects.filter(
        lang=lang, enable=True).only('id', 'summary', 'title').all(), to_attr='articles')

    highlights = Publication.objects.filter(topic=Publication.TOPIC_HIGHLIGHT_CASES,
                                            enable=True).prefetch_related(prefetch).all()[:limit]
    study_pubs = Publication.objects.filter(topic=Publication.TOPIC_CASE_STUDY,
                                            enable=True).prefetch_related(prefetch).all()[:limit]
    new_pubs = Publication.objects.filter(topic=Publication.TOPIC_NEWS,
                                          enable=True).prefetch_related(prefetch).all()[:limit]
    share_pubs = Publication.objects.filter(topic=Publication.TOPIC_DATA_SHARING,
                                            enable=True).prefetch_related(prefetch).all()[:limit]
    update_pubs = Publication.objects.filter(topic=Publication.TOPIC_UPDATES,
                                             enable=True).prefetch_related(prefetch).all()[:limit]

    return render(request, 'index.html',
                  context={'highlights': highlights, 'study_pubs': study_pubs, 'new_pubs': new_pubs,
                           'share_pubs': share_pubs, 'update_pubs': update_pubs, 'display_limit': limit})
