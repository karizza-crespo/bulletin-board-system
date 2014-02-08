from django.utils.datastructures import SortedDict
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from django.contrib.auth import authenticate, login

from bulletinboard.models import UserProfile, Board, Thread, Post, User
from bulletinboard.forms import UserProfileForm, ThreadForm, TopicForm, BoardForm, PostForm

import datetime

DEFAULT_AVATAR = 'avatars/profile_pic.jpg'
REDIRECT_HOME = '/bulletinboard/'
REDIRECT_BOARD = REDIRECT_HOME+'%s/'
REDIRECT_USERPROFILE = REDIRECT_HOME+'userprofile/'
REDIRECT_OTHERPROFILE = REDIRECT_HOME+'profiles/%s/'
REDIRECT_THREAD = REDIRECT_BOARD+'thread/%s/'
REDIRECT_BOARD_PAGE = REDIRECT_BOARD+'?page=%s'
REDIRECT_THREAD_PAGE = REDIRECT_THREAD+'?page=%s'
REDIRECT_USERPROFILE_PAGE = REDIRECT_USERPROFILE+'?page=%s'
REDIRECT_OTHERPROFILE_PAGE = REDIRECT_OTHERPROFILE+'?page=%s'


def login_user(request):

    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(REDIRECT_HOME)

    boards = Board.objects.all()
    grouping = SortedDict()
    for entry in boards:
        grouping.setdefault(entry.topic.name, [])
        grouping[entry.topic.name].append(entry)

    context = {
        'username': username,
        'boards': grouping,
    }

    return render(request, 'bulletinboard/login.html', context)


@login_required
def home(request):

    #if user does not have a user profile, create one
    profile = UserProfile.objects.filter(user=request.user)
    if not profile:
        profile = UserProfile(user=request.user, avatar=DEFAULT_AVATAR, about_me=" ",
                              birthdate=datetime.date.today(), hometown=" ", present_location=" ")
        if request.user.is_superuser or request.user.is_staff:
            profile.user_type = 3
        profile.save()

    boards = Board.objects.all()
    topic_form = TopicForm()
    board_form = BoardForm()
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        #user clicks the 'Add Topic'
        if 'addtopic' in request.POST:
            topic_form = TopicForm(request.POST)
            if topic_form.is_valid():
                topic_form.save()
                return HttpResponseRedirect(REDIRECT_HOME)
        #user clicks the 'Add Board' button
        elif 'addboard' in request.POST:
            board_form = BoardForm(request.POST, request.FILES)
            if board_form.is_valid():
                board = board_form.save(commit=False)
                if Board.objects.all():
                    last_board = Board.objects.aggregate(last_rank=Max('rank'))
                    board.rank = last_board['last_rank']+1
                else:
                    board.rank = 1
                board.save()

                return HttpResponseRedirect(REDIRECT_HOME)

    #group boards according to their topics
    grouping = SortedDict()
    for entry in boards:
        grouping.setdefault(entry.topic.name, [])
        grouping[entry.topic.name].append(entry)

    context = {
        'boards': grouping,
        'profile': profile,
        'reorder': True,
        'topic_form': topic_form,
        'board_form': board_form,
    }
    return render(request, 'bulletinboard/home.html', context)


#function displaying a specific board
@login_required
def board(request, board_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    board = get_object_or_404(Board, pk=board_id)
    thread_form = ThreadForm()
    post_form = PostForm()

    if request.method == 'POST':
        #user clicks the 'Add Thread' button
        if 'addthreadpost' in request.POST:
            thread_form = ThreadForm(request.POST)
            post_form = PostForm(request.POST)
            if thread_form.is_valid() and post_form.is_valid():
                thread = Thread(name=request.POST['name'], user=profile, board=board)
                thread.save()
                post = Post(user=profile, thread=thread, message_markdown=request.POST['message_markdown'])
                post.save()
                return HttpResponseRedirect(REDIRECT_BOARD % board_id)
        elif 'gotopage' in request.POST:
            page_number = request.POST['pagenumber']
            return HttpResponseRedirect(REDIRECT_BOARD_PAGE % (board_id, page_number))

    #sort threads according to their most recent post
    threads = Thread.objects.filter(board=board).annotate(latest_post=Max('post__date_posted')).order_by('thread_type', 'latest_post')
    posts = []
    for thread in threads:
        p = Post.objects.get(Q(thread=thread), Q(date_posted=thread.latest_post))
        posts.append(p)

    paginator = Paginator(threads, 20)
    page = request.GET.get('page')
    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        threads = paginator.page(1)
    except EmptyPage:
        threads = paginator.page(paginator.num_pages)

    context = {
        'board': board,
        'thread_form': thread_form,
        'post_form': post_form,
        'threads': threads,
        'posts': posts,
        'profile': profile,
    }
    return render(request, 'bulletinboard/boardIndex.html', context)


#function for displaying a specific thread
@login_required
def thread(request, board_id, thread_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    thread = get_object_or_404(Thread, pk=thread_id)
    post_form = PostForm()
    posts = thread.post_set.all().order_by('date_posted')

    paginator = Paginator(posts, 20)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    #user submits a post
    if request.method == 'POST':
        if 'addpost' in request.POST:
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post = Post(user=profile, thread=thread, message_markdown=request.POST['message_markdown'])
                post.save()
                return HttpResponseRedirect(REDIRECT_THREAD % (board_id, thread_id))
        elif 'gotopage' in request.POST:
            page_number = request.POST['pagenumber']
            return HttpResponseRedirect(REDIRECT_THREAD_PAGE % (board_id, thread_id, page_number))

    context = {
        'thread': thread,
        'posts': posts,
        'post_form': post_form,
        'profile': profile,
    }
    return render(request, 'bulletinboard/threadIndex.html', context)


#function for displaying the user's profile and posts
@login_required
def user_profile(request):

    profile = UserProfile.objects.get(user__username=request.user.username)
    posts = Post.objects.filter(user__user__username=request.user.username).order_by('-date_posted')

    paginator = Paginator(posts, 20)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        if 'gotopage' in request.POST:
            page_number = request.POST['pagenumber']
            return HttpResponseRedirect(REDIRECT_USERPROFILE_PAGE % page_number)

    context = {
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'bulletinboard/userProfile.html', context)


#function for creating a new user
def new_user(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['username']

            if len(username) == 0 or len(password) == 0 or len(request.POST['c_password']) == 0:
                return render(request, 'bulletinboard/newUser.html', {'message': 'All fields are required.'})
            if password != request.POST['c_password']:
                return render(request, 'bulletinboard/newUser.html', {'message': 'Passwords do not match.'})

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            #create an instance of the user profile for the newly created user
            profile = UserProfile(user=user, avatar=DEFAULT_AVATAR, about_me=" ", birthdate=datetime.date.today(), hometown=" ", present_location=" ")
            profile.save()
            return HttpResponseRedirect('/accounts/login/')
        except:
            #if there is an error, return to newUser.html
            return render(request, 'bulletinboard/newUser.html', {'message': 'Username is already taken.'})
    return render(request, 'bulletinboard/newUser.html', {})


#function for editing a user profile
@login_required
def edit_user_profile(request):

    user = UserProfile.objects.get(user__username=request.user)
    #instantiate a form with its current values
    form = UserProfileForm(instance=user)
    return render(request, 'bulletinboard/editProfile.html', {'form': form, 'profile': user})


#function that saves the values from the UserProfileForm
@login_required
def submit_user_profile(request):

    if request.method == 'POST':
        user = UserProfile.objects.get(user__username=request.user)
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form = UserProfileForm(request.POST, request.FILES, instance=user)
            form.save()
            return HttpResponseRedirect(REDIRECT_USERPROFILE)
        else:
            return render(request, 'bulletinboard/editProfile.html', {'form': form, })


#function for viewing other user's profile
@login_required
def other_profile(request, user_id):

    profile = get_object_or_404(UserProfile, pk=user_id)
    posts = Post.objects.filter(user__id=user_id).order_by('-date_posted')

    paginator = Paginator(posts, 20)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        if 'gotopage' in request.POST:
            page_number = request.POST['pagenumber']
            return HttpResponseRedirect(REDIRECT_OTHERPROFILE_PAGE % (profile.id, page_number))

    context = {
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'bulletinboard/userProfile.html', context)


#function for locking or unlocking a thread
@login_required
def lock_unlock_thread(request, board_id, thread_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    if request.user.has_perm('bulletinboard.lock_thread') is False or profile.is_banned is True:
        return HttpResponse('<h2>Permission Denied.</h2>')

    thread = get_object_or_404(Thread, pk=thread_id)
    if thread.is_locked is True:
        thread.is_locked = False
    else:
        thread.is_locked = True
    thread.save()

    return HttpResponseRedirect(REDIRECT_THREAD % (board_id, thread_id))


#function for marking a thread as sticky or not
@login_required
def sticky_not_sticky(request, board_id, thread_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    if request.user.has_perm('bulletinboard.change_threadtype') is False or profile.is_banned is True:
        return HttpResponse('<h2>Permission Denied.</h2>')

    thread = get_object_or_404(Thread, pk=thread_id)
    if thread.thread_type == '1':
        thread.thread_type = 2
    else:
        thread.thread_type = 1
    thread.save()

    return HttpResponseRedirect(REDIRECT_THREAD % (board_id, thread_id))


#function for deleting a board
@login_required
def delete_board(request, board_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    if request.user.has_perm('bulletinboard.delete_board') is False or profile.is_banned is True:
        return HttpResponse('<h2>Permission Denied.</h2>')

    board = get_object_or_404(Board, pk=board_id)
    board.delete()
    return HttpResponseRedirect(REDIRECT_HOME)


#function for banning or unbanning a user
@login_required
def ban_user(request, user_id):

    profile = get_object_or_404(UserProfile, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.user.has_perm('bulletinboard.ban_user') is False or user_profile.is_banned is True:
        return HttpResponse('<h2>Permission Denied.</h2>')

    if profile.is_banned is False:
        profile.is_banned = True
    else:
        profile.is_banned = False
    profile.save()
    return HttpResponseRedirect(REDIRECT_OTHERPROFILE % user_id)


#function for displaying the form for editing a post
@login_required
def edit_post(request, board_id, thread_id, post_id):

    post = get_object_or_404(Post, pk=post_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    thread = get_object_or_404(Thread, pk=thread_id)
    if post.user.user != request.user or profile.is_banned is True or thread.is_locked is True:
        return HttpResponse('<h2>Permission Denied.</h2>')

    form = PostForm(instance=post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'bulletinboard/editPost.html', context)


@login_required
def submit_post(request, board_id, thread_id, post_id):

    post = get_object_or_404(Post, pk=post_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    thread = get_object_or_404(Thread, pk=thread_id)
    if post.user.user != request.user or profile.is_banned is True or thread.is_locked is True:
        return HttpResponse('<h2>Permission Denied.</h2>')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.date_posted = datetime.datetime.now()
            post.message_markdown = request.POST['message_markdown']
            post.save()
            return HttpResponseRedirect(REDIRECT_THREAD % (board_id, thread_id))

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'bulletinboard/editPost.html', context)


#function for deleting a thread
@login_required
def delete_thread(request, board_id, thread_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    if request.user.has_perm('bulletinboard.delete_thread') is False or profile.is_banned is True:
        return HttpResponse('<h2>Permission Denied.</h2>')

    thread = get_object_or_404(Thread, pk=thread_id)
    thread.delete()
    return HttpResponseRedirect(REDIRECT_BOARD % board_id)


@login_required
def move_up(request, board_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    if profile.is_banned is True or profile.user_type != 3:
        return HttpResponse('<h2>Permission Denied.</h2>')

    board = get_object_or_404(Board, pk=board_id)
    board.decrease_rank()

    return HttpResponseRedirect(REDIRECT_HOME)


@login_required
def move_down(request, board_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    if profile.is_banned is True or profile.user_type != 3:
        return HttpResponse('<h2>Permission Denied.</h2>')

    board = get_object_or_404(Board, pk=board_id)
    board.increase_rank()

    return HttpResponseRedirect(REDIRECT_HOME)
