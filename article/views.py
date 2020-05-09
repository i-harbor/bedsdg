from django.shortcuts import render
from django.views import View
from django.utils.translation import get_language

from .models import Article


class PubDetailView(View):
    def get(self, request, *args, **kwargs):
        pub_id = kwargs.get('id')

        art = None
        if pub_id and pub_id > 0:
            lang_code = get_language()
            lang = Article.get_lang_value_by_code(lang_code=lang_code)
            art = Article.objects.filter(publication=pub_id, lang=lang).first()

        return render(request, 'pub_detail.html', {'pub_id': pub_id, 'art': art})
