# Generated by Django 2.2.12 on 2020-05-12 08:14

from django.db import migrations, models
import django.db.models.deletion
import filebrowser.fields
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.SmallIntegerField(choices=[(1, '中文'), (2, '英文')], default=1, verbose_name='语言')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('summary', models.CharField(blank=True, default='', help_text='可以为空，可用于亮点案例的简介', max_length=255, verbose_name='概述')),
                ('author', models.CharField(default='', max_length=255, verbose_name='编辑')),
                ('content', tinymce.models.HTMLField(default='', verbose_name='正文内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('enable', models.BooleanField(default=False, help_text='是否发布可见，默认不发布可见，一般在文章编辑完成后再发布可见', verbose_name='发布状态')),
            ],
            options={
                'verbose_name': '1_文章',
                'verbose_name_plural': '1_文章',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.SmallIntegerField(choices=[(1, '指标案例'), (2, '最新动态'), (3, '数据共享'), (4, '前沿扫描'), (5, '亮点案例')], default=2, verbose_name='主题')),
                ('cover_image', filebrowser.fields.FileBrowseField(blank=True, default='', help_text='可以不配置，但主题为亮点案例时, 需要配置封面图轮播展示', max_length=1024, verbose_name='封面图片')),
                ('title', models.CharField(help_text='可以用要发布的文章的标题，每个发布内容对应着不同语言版本的文章，各种语言版本的文章需要关联到同一个发布内容，以便各种语言版本文章之间的切换', max_length=255, verbose_name='内容标题')),
                ('enable', models.BooleanField(default=False, help_text='是否发布可见，默认不发布可见，一般在文章编辑完成后再发布可见', verbose_name='发布状态')),
                ('remarks', models.CharField(blank=True, default='', max_length=255, verbose_name='备注')),
            ],
            options={
                'verbose_name': '0_发布内容',
                'verbose_name_plural': '0_发布内容',
                'ordering': ['-id'],
            },
        ),
        migrations.AddIndex(
            model_name='publication',
            index=models.Index(fields=['topic'], name='idx_topic'),
        ),
        migrations.AddField(
            model_name='article',
            name='publication',
            field=models.ForeignKey(help_text='不同语言版本的文章所属发布内容，例如要发布新的内容a，需要先创建发布内容a，中文版a文章和英文版a文章必须关联对应的发布内容a', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_set', to='article.Publication', verbose_name='文章所属发布内容'),
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['title'], name='idx_article_title'),
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['create_time'], name='idx_article_create_time'),
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together={('lang', 'publication')},
        ),
    ]
