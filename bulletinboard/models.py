from django.db import models
from django.contrib.auth.models import User, Permission

import markdown

MAX_LENGTH_CHAR = 50
MAX_LENGTH_TYPE = 1


class UserProfile(models.Model):
    USER_TYPES = [
        [1, 'Poster'],
        [2, 'Moderator'],
        [3, 'Administrator'],
    ]

    GENDER_CHOICES = [
        [1, 'Female'],
        [2, 'Male'],
    ]

    user = models.ForeignKey(User, unique=True)
    user_type = models.IntegerField(max_length=MAX_LENGTH_TYPE, choices=USER_TYPES, default=1)
    is_banned = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True)
    about_me = models.TextField()
    birthdate = models.DateField()
    hometown = models.CharField(max_length=MAX_LENGTH_CHAR)
    present_location = models.CharField(max_length=MAX_LENGTH_CHAR)
    skype = models.CharField(max_length=MAX_LENGTH_CHAR, blank=True)
    ym = models.CharField(max_length=MAX_LENGTH_CHAR, blank=True)
    website = models.CharField(max_length=MAX_LENGTH_CHAR, blank=True)
    gender = models.IntegerField(max_length=MAX_LENGTH_TYPE, choices=GENDER_CHOICES, default=1)
    interests = models.TextField(blank=True)

    class Meta:
        permissions = (
            ("ban_user", "Can ban user"),
        )

    def save(self):
        add_post = Permission.objects.get(name='Can add post')
        edit_post = Permission.objects.get(name='Can change post')
        add_thread = Permission.objects.get(name='Can add thread')
        edit_thread = Permission.objects.get(name='Can change thread')
        ban_user = Permission.objects.get(name='Can ban user')
        lock_thread = Permission.objects.get(name='Can lock thread')
        thread_type = Permission.objects.get(name='Can change threadtype')
        add_board = Permission.objects.get(name='Can add board')
        delete_board = Permission.objects.get(name='Can delete board')
        edit_board = Permission.objects.get(name='Can change board')
        add_topic = Permission.objects.get(name='Can add topic')
        edit_topic = Permission.objects.get(name='Can change topic')
        delete_topic = Permission.objects.get(name='Can delete topic')
        delete_thread = Permission.objects.get(name='Can delete thread')

        self.user.user_permissions.clear()

        if self.user_type == 1:
            self.user.is_staff = False
            self.user.user_permissions.add(add_post, edit_post, add_thread,
                                           edit_thread, delete_thread)
        elif self.user_type == 2:
            self.user.is_staff = False
            self.user.user_permissions.add(add_post, edit_post, add_thread,
                                           edit_thread, delete_thread, ban_user, lock_thread,
                                           thread_type)
        else:
            self.user.is_staff = True
            self.user.user_permissions.add(add_post, edit_post, add_thread, edit_thread,
                                           ban_user, lock_thread, thread_type, add_topic,
                                           edit_topic, delete_topic, add_board, delete_board,
                                           edit_board, delete_thread
                                           )
        self.user.save()
        super(UserProfile, self).save()

    def get_gender(self):
        return self.GENDER_CHOICES[self.gender-1][1]

    def get_type(self):
        return self.USER_TYPES[self.user_type-1][1]

    def get_post_count(self):
        posts = self.post_set.all()
        number = 0
        for post in posts:
            number = number + 1
        return number
    get_post_count.short_description = "Total Post Count"

    def __unicode__(self):
        return self.user.username


class Topic(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR)

    def get_board_number(self):
        boards = self.board_set.all()
        number = 0
        for board in boards:
            number = number+1
        return number
    get_board_number.short_description = "Number of Boards"

    def __unicode__(self):
        return self.name


class Board(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR)
    icon = models.ImageField(upload_to='icons/', null=True)
    description = models.TextField()
    topic = models.ForeignKey(Topic)
    rank = models.SmallIntegerField(unique=True, db_index=True)

    def get_thread_number(self):
        threads = self.thread_set.all()
        number = 0
        for thread in threads:
            number = number+1
        return number
    get_thread_number.short_description = "Number of Threads"

    def get_post_number(self):
        threads = self.thread_set.all()
        number = 0
        for thread in threads:
            posts = thread.post_set.all()
            for post in posts:
                number = number+1
        return number
    get_post_number.short_description = "Number of Posts"

    def increase_rank(self):
        """
        Changes position of this item with the next item in the
        list. Does nothing if this item is the last one.
        """
        try:
            next_item = Board.objects.filter(rank__gt=self.rank)[0]
        except IndexError:
            pass
        else:
            self.swap_ranks(next_item)

    def decrease_rank(self):
        """
        Changes position of this item with the previous item in the
        list. Does nothing if this item is the first one.
        """
        try:
            prev_item = Board.objects.filter(rank__lt=self.rank).reverse()[0]
        except IndexError:
            pass
        else:
            self.swap_ranks(prev_item)

    def swap_ranks(self, other):
        """
        Swap positions with ``other`` board.
        """
        maxrank = Board.objects.reverse()[0].rank + 1
        prev_rank, self.rank = self.rank, maxrank
        self.save()
        self.rank, other.rank = other.rank, prev_rank
        other.save()
        self.save()

    class Meta:
        ordering = ('rank',)

    def __unicode__(self):
        return self.name


class Thread(models.Model):
    THREAD_TYPE = [
        ['1', 'Sticky'],
        ['2', 'Non-sticky'],
    ]

    name = models.CharField(max_length=MAX_LENGTH_CHAR)
    date_created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserProfile)
    board = models.ForeignKey(Board)
    thread_type = models.CharField(max_length=MAX_LENGTH_TYPE, choices=THREAD_TYPE, default=2)
    is_locked = models.BooleanField(default=False)

    def get_post_number(self):
        posts = self.post_set.all()
        number = 0
        for post in posts:
            number = number+1
        return number
    get_post_number.short_description = "Number of Posts"

    class Meta:
        ordering = ('thread_type',)
        permissions = (
            ("lock_thread", "Can lock thread"),
            ("change_threadtype", "Can change threadtype")
        )

    def __unicode__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(UserProfile)
    thread = models.ForeignKey(Thread)
    message = models.TextField('Message Body as HTML', blank=True)
    message_markdown = models.TextField('Message Body')
    date_posted = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date_posted',)

    def save(self):
        self.message = markdown.markdown(self.message_markdown)
        super(Post, self).save()

    def __unicode__(self):
        return "%s's post" % self.user.user.username
