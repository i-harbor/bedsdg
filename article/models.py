from django.db import models
from django.utils.translation import gettext_lazy as _

from tinymce import models as tiny_models
from filebrowser.fields import FileBrowseField


class Publication(models.Model):
    """
    发布内容，每个发布内容对应各种不同语言版本的文章
    """
    TOPIC_CASE_STUDY = 1
    TOPIC_NEWS = 2
    TOPIC_DATA_SHARING = 3
    TOPIC_UPDATES = 4
    TOPIC_HIGHLIGHT_CASES = 5
    TOPIC_CHOICES = (
        (TOPIC_CASE_STUDY, _('指标案例')),
        (TOPIC_NEWS, _('最新动态')),
        (TOPIC_DATA_SHARING, _('数据共享')),
        (TOPIC_UPDATES, _('前沿扫描')),
        (TOPIC_HIGHLIGHT_CASES, _('亮点案例')),
    )

    id = models.AutoField(primary_key=True, verbose_name='ID')
    topic = models.SmallIntegerField(choices=TOPIC_CHOICES, default=TOPIC_NEWS, verbose_name=_('主题'))
    cover_image = FileBrowseField(max_length=1024, blank=True, default='', verbose_name=_('封面图片'),
                                  help_text=_('可以不配置，但主题为亮点案例时, 需要配置封面图轮播展示'))
    title = models.CharField(max_length=255, verbose_name=_('内容标题'), help_text=_('可以用要发布的文章的标题，每个发布内容'
                             '对应着不同语言版本的文章，各种语言版本的文章需要关联到同一个发布内容，以便各种语言版本文章之间的切换'))
    remarks = models.CharField(max_length=255, blank=True, default='', verbose_name=_('备注'))

    class Meta:
        ordering = ['-id']
        indexes = [models.Index(fields=('topic',), name='idx_topic')]
        verbose_name = _('0_发布内容')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Publication>{self.title}'


class Article(models.Model):
    """
    文章模型
    """
    LANG_CHINESE = 1
    LANG_ENGLISH = 2
    LANG_CHOICES = (
        (LANG_CHINESE, _('中文')),
        (LANG_ENGLISH, _('英文')),
    )

    id = models.AutoField(primary_key=True, verbose_name='ID')
    lang = models.SmallIntegerField(choices=LANG_CHOICES, default=LANG_CHINESE, verbose_name=_('语言'))
    title = models.CharField(max_length=255, verbose_name=_('标题'))
    summary = models.CharField(max_length=255, default='', blank=True, verbose_name=_('概述'),
                               help_text=_('可以为空，可用于亮点案例的简介'))
    author = models.CharField(max_length=255, default='', verbose_name=_('作者'))
    content = tiny_models.HTMLField(default='', verbose_name=_('正文内容'))
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))
    modify_time = models.DateTimeField(auto_now=True, verbose_name=_('修改时间'))
    publication = models.ForeignKey(to=Publication, related_name='article_set', on_delete=models.SET_NULL,
                                    null=True, verbose_name=_('文章所属发布内容'),
                                    help_text=_('不同语言版本的文章所属发布内容，例如要发布新的内容a，需要'
                                                '先创建发布内容a，中文版a文章和英文版a文章必须关联对应的发布内容a'))

    class Meta:
        indexes = [
            models.Index(fields=('title',), name='idx_article_title'),
            models.Index(fields=('create_time',), name='idx_article_create_time'),
        ]
        unique_together = ['lang', 'publication']
        ordering = ['-id']
        verbose_name = _('1_文章')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Article>{self.title}'



