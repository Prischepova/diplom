from django.contrib import admin

from .models import *

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Админ-панель модели профиля
    """
    list_display = ('user', 'photo', 'phone', 'slug')
    list_display_links = ('user', 'slug')


class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'files')
    list_display_links = ('id', 'files')
    # search_fields = ('title', 'tutor_name')


admin.site.register(Documents, DocumentsAdmin)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'team', 'slug', 'date_training', 'start_training', 'finish_training', 'location_name', 'tutor')
    list_display_links = ('id', 'team')
    prepopulated_fields = {"slug": ("team",)}
    # search_fields = ('title', 'tutor_name')


admin.site.register(Schedule, ScheduleAdmin)


class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'description_footer')
    list_display_links = ('id', 'title')
    # search_fields = ('title', 'tutor_name')


admin.site.register(Notifications, NotificationsAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    # search_fields = ('title', 'tutor_name')


admin.site.register(Team, TeamAdmin)


class IndivAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slug', 'tutor', 'child_name', 'datetime', 'location_name')
    list_display_links = ('id', 'datetime')
    prepopulated_fields = {"slug": ("tutor",)}
    # search_fields = ('title', 'tutor_name')


admin.site.register(Indiv, IndivAdmin)


class DateTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime')
    list_display_links = ('id', 'datetime')
    # search_fields = ('title', 'tutor_name')


admin.site.register(DateTime, DateTimeAdmin)


class TutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    # search_fields = ('title', 'tutor_name')


admin.site.register(Tutor, TutorAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'location_name')
    list_display_links = ('id', 'location_name')
    # search_fields = ('title', 'tutor_name')


admin.site.register(Location, LocationAdmin)


# class NewsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'name', 'photo')
#     list_display_links = ('id', 'user')
#     # search_fields = ('title', 'tutor_name')
#
#
# admin.site.register(News, NewsAdmin)
#
#
# class NewsImageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'news', 'image')
#     list_display_links = ('id', 'image')
#     # search_fields = ('title', 'tutor_name')
#
#
# admin.site.register(NewsImage, NewsImageAdmin)


class NewsImageInline(admin.TabularInline):
    fk_name = 'news'
    model = NewsImage


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsImageInline, ]
