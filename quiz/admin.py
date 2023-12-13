from django.contrib import admin

from .models import Quiz, Question, AnswerOption, UserAnswer, QuizResult

class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    # extra = 2

class QuestionInline(admin.StackedInline):
    model = Question
    # extra = 3
    inlines = [AnswerOptionInline]

class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["quiz_text", "description"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [QuestionInline]
    readonly_fields = ["pub_date"]
    list_display = ["quiz_text", "description", "pub_date"]

class AnswerAdmin(admin.ModelAdmin):
    list_display = ["question", "option_text", "is_correct"]
    list_filter = ["question"]

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ["user", "question", "selected_answer", "submitted_at"]
    list_filter = ["user", "question"]

class QuizResultAdmin(admin.ModelAdmin):
    list_display = ["user", "quiz", "score", "completed_at"]
    list_filter = ["user", "quiz"]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(AnswerOption, AnswerAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
