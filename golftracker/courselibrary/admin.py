from django.contrib import admin

from .models import Course, Tee, Hole

class HoleInline(admin.TabularInline):
    model = Hole
    extra = 0

class TeeInline(admin.StackedInline):
    model = Tee
    extra = 0

class TeeAdmin(admin.ModelAdmin):
    inlines = [HoleInline]

class CourseAdmin(admin.ModelAdmin):
    inlines = [TeeInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(Tee, TeeAdmin)