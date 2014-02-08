from django.conf.urls import patterns, url
from bulletinboard import views


urlpatterns = patterns(
    '',
    url(r'^$', views.home, name="home"),
    url(r'^(?P<board_id>\d+)/delete/$', views.delete_board, name="delete_board"),
    url(r'^(?P<board_id>\d+)/moveup/$', views.move_up, name="move_up"),
    url(r'^(?P<board_id>\d+)/movedown/$', views.move_down, name="move_down"),
    url(r'^(?P<board_id>\d+)/$', views.board, name="board"),
    url(r'^(?P<board_id>\d+)/thread/(?P<thread_id>\d+)/$', views.thread, name="thread"),
    url(r'^userprofile/$', views.user_profile, name="user_profile"),
    url(r'^editprofile/$', views.edit_user_profile, name="edit_user_profile"),
    url(r'^editprofile/submit/$', views.submit_user_profile, name="submit_user_profile"),
    url(r'^profiles/(?P<user_id>\d+)/$', views.other_profile, name="other_profile"),
    url(r'^profiles/(?P<user_id>\d+)/ban/$', views.ban_user, name="ban_user"),
    url(r'^(?P<board_id>\d+)/thread/(?P<thread_id>\d+)/lockunlock/$', views.lock_unlock_thread, name="lock_unlock_thread"),
    url(r'^(?P<board_id>\d+)/thread/(?P<thread_id>\d+)/sticky/$', views.sticky_not_sticky, name="sticky_not_sticky"),
    url(r'^(?P<board_id>\d+)/thread/(?P<thread_id>\d+)/post/(?P<post_id>\d+)/$', views.edit_post, name="edit_post"),
    url(r'^(?P<board_id>\d+)/thread/(?P<thread_id>\d+)/post/(?P<post_id>\d+)/submit/$', views.submit_post, name="submit_post"),
    url(r'^(?P<board_id>\d+)/thread/(?P<thread_id>\d+)/delete/$', views.delete_thread, name="delete_thread"),
)
