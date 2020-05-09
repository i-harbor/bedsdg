from django.urls import path, include, re_path

from . import views


app_name = 'article'


urlpatterns = [
    path('pub/<int:id>', views.PubDetailView.as_view(), name='pub-detail'),
]
