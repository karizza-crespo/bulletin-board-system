from django.forms import ModelForm
from bulletinboard.models import UserProfile, Board, Thread, Post, Topic


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'user_type', 'is_banned')


class TopicForm(ModelForm):
    class Meta:
        model = Topic


class BoardForm(ModelForm):
    class Meta:
        model = Board
        exclude = ('rank',)


class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        exclude = ('is_locked', 'user', 'board', 'thread_type', 'date_created')


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'date_posted', 'thread', 'message')
