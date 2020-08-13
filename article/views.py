from django.shortcuts import render, redirect, reverse
from django.views import View
from django.utils.translation import get_language
from django.db.models import Prefetch

from utils.paginators import NumsPaginator
from .models import Article, Publication


class PubDetailView(View):
    def get(self, request, *args, **kwargs):
        pub_id = kwargs.get('id')

        art = None
        if pub_id and pub_id > 0:
            lang_code = get_language()
            lang = Article.get_lang_value_by_code(lang_code=lang_code)
            art = Article.objects.filter(publication=pub_id, lang=lang).first()

        return render(request, 'pub_detail.html', {'pub_id': pub_id, 'art': art})


class PubListView(View):
    NUM_PER_PAGE = 20  # Show num per page

    def get(self, request, *args, **kwargs):
        topic = request.GET.get('topic', None)

        lang_code = get_language()
        lang = Article.get_lang_value_by_code(lang_code=lang_code)
        prefetch = Prefetch('article_set', queryset=Article.objects.filter(
            lang=lang, enable=True).only('id', 'summary', 'title').all(), to_attr='articles')

        if topic is not None:
            try:
                topic = int(topic)
                if topic not in Publication.TOPIC_INVALID_VALUES:
                    raise ValueError
            except ValueError:
                return redirect(to=reverse('article:pub-list'))

            pub_queryset = Publication.objects.filter(topic=topic, enable=True).prefetch_related(prefetch).all()
        else:
            pub_queryset = Publication.objects.filter(enable=True).prefetch_related(prefetch).all()

        # 分页显示
        paginator = NumsPaginator(request, pub_queryset, self.NUM_PER_PAGE)
        page_num = request.GET.get('page', 1)  # 获取页码参数，没有参数默认为1
        pubs_page = paginator.get_page(page_num)
        page_nav = paginator.get_page_nav(pubs_page)

        context = {
            'publications': pubs_page,
            'topics': Publication.TOPIC_CHOICES,
            'active': topic,
            'page_nav': page_nav,
            'count': paginator.count
        }

        return render(request, 'pub_list.html', context=context)

