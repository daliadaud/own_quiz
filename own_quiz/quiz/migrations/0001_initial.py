# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 16:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionChoiceAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.TextField(blank=True)),
                ('image_answer', models.ImageField(blank=True, null=True, upload_to='quiz_question_answer_images')),
                ('value', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='quiz_featured_images')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='own_quizzes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'quizzes',
            },
        ),
        migrations.CreateModel(
            name='QuizChoiceResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='quiz_result_images')),
                ('low_value', models.IntegerField()),
                ('high_value', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_results', to='quiz.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuizInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_code', models.CharField(max_length=50, unique=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_instances', to='quiz.Quiz')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_quiz_instances', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizInstanceAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_instance_answers', to='quiz.QuestionChoiceAnswer')),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='quiz_question_images')),
                ('question', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_questions', to='quiz.Quiz')),
            ],
        ),
        migrations.AddField(
            model_name='quizinstanceanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_instance_questions', to='quiz.QuizQuestion'),
        ),
        migrations.AddField(
            model_name='quizinstanceanswer',
            name='quiz_instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_instance_answers', to='quiz.QuizInstance'),
        ),
        migrations.AddField(
            model_name='questionchoiceanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_question_choice_answers', to='quiz.QuizQuestion'),
        ),
        migrations.AlterUniqueTogether(
            name='quizinstanceanswer',
            unique_together=set([('question', 'quiz_instance')]),
        ),
    ]
