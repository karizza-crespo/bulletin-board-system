from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect
from django.conf.urls.defaults import patterns
from django.core.exceptions import PermissionDenied
from bulletinboard.models import UserProfile, Board, Thread, Post, Topic


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'gender', 'birthdate', 'hometown', 'present_location', 'get_post_count')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_board_number')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'get_thread_number', 'get_post_number', 'rank', 'move')

    def get_urls(self):
        admin_view = self.admin_site.admin_view
        urls = patterns('',
                       (r'^(?P<board_id>\d+)/move_up/$', admin_view(self.move_up)),
                       (r'^(?P<board_id>\d+)/move_down/$', admin_view(self.move_down)),
                        )
        return urls + super(BoardAdmin, self).get_urls()

    def move(self, obj):
        """
        Returns html with links to move_up and move_down views.
        """
        button = u'<a href="%s"> %s</a>'

        link = '%d/move_up/' % obj.pk
        html = button % (link, 'up') + " | "
        link = '%d/move_down/' % obj.pk
        html += button % (link, 'down')
        return html
    move.allow_tags = True

    def move_up(self, request, board_id):
        """
        Decrease rank (change ordering) of the board with
        id=``board_id``.
        """
        if self.has_change_permission(request):
            item = get_object_or_404(Board, pk=board_id)
            item.decrease_rank()
        else:
            raise PermissionDenied
        return redirect('admin:bulletinboard_board_changelist')

    def move_down(self, request, board_id):
        """
        Increase rank (change ordering) of the board with
        id=``board_id``.
        """
        if self.has_change_permission(request):
            item = get_object_or_404(Board, pk=board_id)
            item.increase_rank()
        else:
            raise PermissionDenied
        return redirect('admin:bulletinboard_board_changelist')


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('name', 'board', 'get_post_number', 'thread_type', 'is_locked', 'date_created', 'user')


class PostAdmin(admin.ModelAdmin):
    list_display = ('message_markdown', 'thread', 'user')
    fields = ('user', 'thread', 'message')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
