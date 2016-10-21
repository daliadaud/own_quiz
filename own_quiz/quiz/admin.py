from django.contrib import admin
from .models import Quiz, QuizQuestion, QuestionChoiceAnswer, QuizChoiceResult, QuizInstance, QuizInstanceAnswer
import nested_admin

# Register your models here.


class QuestionChoiceAnswerInLine(nested_admin.NestedTabularInline):
    model = QuestionChoiceAnswer
    extra = 0
    fields = ('text_answer', 'image_answer', 'value')
    fk_name = 'question'


class QuizQuestionInLine(nested_admin.NestedTabularInline):
    model = QuizQuestion
    extra = 0
    fields = ('question', 'image')
    fk_name = 'quiz'
    inlines = [QuestionChoiceAnswerInLine]


class QuizAdmin(nested_admin.NestedModelAdmin):
    #form = OrganizationForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'slug', 'owner')
    list_display_links = ('id', 'title', 'slug')
    search_fields = ('slug', 'title')
    inlines = [
        QuizQuestionInLine
    ]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizQuestion)
admin.site.register(QuestionChoiceAnswer)
admin.site.register(QuizChoiceResult)
admin.site.register(QuizInstance)
admin.site.register(QuizInstanceAnswer)

