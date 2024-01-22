from django.contrib import admin

from .models import Round, Score

class ScoreInline(admin.TabularInline):
    model = Score
    extra = 0


class RoundAdmin(admin.ModelAdmin):
    inlines = [ScoreInline]


admin.site.register(Round, RoundAdmin)
