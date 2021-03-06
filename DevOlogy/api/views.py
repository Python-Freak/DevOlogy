import json
from urllib import response
from crum import get_current_user
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Q
import re
from core.models import Follow
from core.models import Post, Bookmark, PostLike, Comment, CommentLike
from authentication.models import User
from .models import ProfilePostList

# Create your views here.

POSTS_PER_PAGE = 21
REGEX_FOR_EMAIL = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
MAX_USERNAME_CHARACTERS = 20
EXCLUDED_USERNAME_CHARACTERS = [
    "@",
    "!",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    "\\",
    "/",
    "?",
    "<",
    ">",
    ",",
    " ",
]

# AUTHENTICATION


def check_email(email):
    return re.fullmatch(REGEX_FOR_EMAIL, email)


def check_username(username: str) -> tuple:
    length = 0
    for i in username:
        length += 1
        if length == MAX_USERNAME_CHARACTERS:
            return (False, "Username too long .")
        if i in EXCLUDED_USERNAME_CHARACTERS:
            return (False, "You Can't use " + i + " in Username .")
    if length >= 5:
        return (True, None)
    else:
        return (False, "Minimum 5 characters are required in Username .")


def knowIfLoggedIn(request):
    if request.is_ajax():
        message = False
        if request.user.is_authenticated:
            message = True
        return HttpResponse(
            json.dumps({"result": str(message)}), content_type="application/json"
        )
    else:
        return HttpResponse("Page Not Found")


def isUserNameAvailable(request):
    if request.method == "POST":
        if request.is_ajax():
            is_available = False
            error = None
            body = request.body.decode("utf-8")
            user_name = json.loads(body)["username"]
            x = list(get_user_model().objects.filter(Q(username=user_name)))
            if len(x) == 0:
                y = check_username(user_name)
                if y[0]:
                    is_available = True
                else:
                    is_available = False
                    error = y[1]
            else:
                error = "Username Occupied"
            response_data = json.dumps(
                {"response": is_available, "error": error})
            mimetype = "application/json"
        return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO


def isEmailAvailable(request):
    if request.method == "POST":
        if request.is_ajax():
            is_available = False
            body = request.body.decode("utf-8")
            email = json.loads(body)["email"]
            x = list(get_user_model().objects.filter(Q(email=email)))
            if check_email(email) and len(x) == 0:
                is_available = True
            response_data = json.dumps({"response": is_available})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO


# NAVBAR/GENERAL
def getRequestUserInfo(request):
    if request.method == "POST":
        if request.is_ajax():
            user = request.user
            data = {
                "username": user.username,
                "name": user.full_name,
                "dp_url": user.get_dp_path,
                "id": user.custom_id,
            }
            response_data = json.dumps({"response": data})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO


def getSearchResults(request):
    if request.method == "POST":
        if request.is_ajax():
            query = json.loads(request.body.decode("utf-8"))["query"].lower()
            """USE CPP"""
            lst = sorted(
                list(
                    get_user_model()
                    .objects.prefetch_related()
                    .filter(
                        Q(username__icontains=query) | Q(
                            full_name__icontains=query)
                    )[0:100]
                ),
                key=lambda t: [t.get_no_of_followers],
                reverse=True,
            )
            data = {"response": {}}
            for val in lst:
                try:
                    data["response"][val.username] = {
                        "username": val.username,
                        "image": val.display_picture.url,
                        "full_name": val.full_name,
                        "link": f"/{val.username}",
                    }
                except:
                    data["response"][val.username] = {
                        "username": val.username,
                        "image": "/static/svgs/user.png",
                        "full_name": val.full_name,
                        "link": f"/{val.username}",
                    }
            response_data = json.dumps({"response": data})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO


def getUserSuggestions(request):
    if request.method == "POST":
        if request.is_ajax():
            suggs = request.user.get_min_sugg
            response = {}
            for i in suggs:
                response[i.username] = {
                    "username": i.username,
                    "dp_url": i.get_dp_path,
                    "name": i.full_name,
                }
            response_data = json.dumps({"response": response})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO


def knowPostLikesAndBookmarks(request):
    if request.method == "POST":
        if request.is_ajax():

            post_id = json.loads(request.body.decode("utf-8"))["custom_id"]
            post = Post.objects.prefetch_related().get(custom_id=post_id)
            response = {}
            response["wasLiked"] = post.was_liked_by_current_user()
            response["wasBookmarked"] = post.was_bookmarked_by_current_user()
            response["time_diff"] = post.get_time_diff()
            response["likes"] = post.get_post_likes_length
            response_data = json.dumps({"response": response})
            mimetype = "application/json"

            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO


def addLike(request):
    if request.method == "POST":
        if request.is_ajax():
            post_id = json.loads(request.body.decode("utf-8"))["custom_id"]
            try:
                post = Post.objects.prefetch_related().get(custom_id=post_id)
                try:
                    PostLike.objects.prefetch_related().get(
                        post=post, user_who_liked_the_post=request.user
                    )
                    response = "Already Liked"
                except:
                    x = PostLike.objects.create(
                        post=post, user_who_liked_the_post=request.user
                    )
                    x.save()
                    response = "Liked"
            except:
                response = "No Post"
            response_data = json.dumps({"response": response})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO


def removeLike(request):
    if request.method == "POST":
        if request.is_ajax():
            post_id = json.loads(request.body.decode("utf-8"))["custom_id"]
            try:
                post = Post.objects.prefetch_related().get(custom_id=post_id)
                try:
                    x = PostLike.objects.prefetch_related().get(
                        post=post, user_who_liked_the_post=request.user
                    )
                    x.delete()
                    response = "Like Removed"
                except:
                    response = "Already not Liked"
            except:
                response = "No Post"
            response_data = json.dumps({"response": response})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO


def addBookmark(request):
    if request.method == "POST":
        if request.is_ajax():
            post_id = json.loads(request.body.decode("utf-8"))["custom_id"]
            try:
                post = Post.objects.prefetch_related().get(custom_id=post_id)
                try:
                    Bookmark.objects.prefetch_related().get(
                        post=post, user=request.user
                    )
                    response = "Already Bookmarked"
                except:
                    x = Bookmark.objects.create(post=post, user=request.user)
                    x.save()
                    response = "Bookmarked"
            except:
                response = "No Post"
            response_data = json.dumps({"response": response})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO


def removeBookmark(request):
    if request.method == "POST":
        if request.is_ajax():
            post_id = json.loads(request.body.decode("utf-8"))["custom_id"]
            try:
                post = Post.objects.prefetch_related().get(custom_id=post_id)
                try:
                    x = Bookmark.objects.prefetch_related().get(
                        post=post, user=request.user
                    )
                    x.delete()
                    response = "Bookmark Removed"
                except:
                    response = "Already not Bookmarked"
            except:
                response = "No Post"
            response_data = json.dumps({"response": response})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)
    else:
        return HttpResponse("Page Not Found")  # TODO


def getPostData(request):
    if request.method == "POST":
        if request.is_ajax():
            post_id = json.loads(request.body)["custom_id"]
            post = Post.objects.prefetch_related().get(custom_id=post_id)
            response = {}
            response["post_image"] = post.picture.url
            response["time_diff"] = post.get_time_diff()
            response["likes"] = post.get_post_likes_length
            response["wasLiked"] = post.was_liked_by_current_user()
            response["wasBookmarked"] = post.was_bookmarked_by_current_user()
            response["user_data"] = {
                "username": post.user.username,
                "dp_url": post.user.get_dp_path,
            }
            response_data = json.dumps({"response": response})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)

    else:
        return HttpResponse("Page Not Found")  # TODO


def comment(request):
    if request.method == "POST":
        if request.is_ajax():
            post_id = json.loads(request.body.decode("utf-8"))["custom_id"]
            comment_text = json.loads(
                request.body.decode("utf-8"))["comment_text"]
            try:
                post = Post.objects.prefetch_related().get(custom_id=post_id)
                x = Comment.objects.create(
                    related_post=post,
                    user_who_commented=request.user,
                    text=comment_text,
                )
                x.save()
                response = "Comment Added"
            except:
                response = "No Post"
            response_data = json.dumps({"response": response, 'data': {
                f'{x.custom_id}': {
                    'custom_id': x.custom_id,
                    'user_dp': x.user_who_commented.get_dp_path,
                    'username': x.user_who_commented.username,
                    'comment': x.text,
                    'commented_on': str(x.commented_on),
                    'was_liked_by_current_user': str(x.was_liked_by_current_user).lower(),
                }
            }})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)


def addCommentLike(request):
    if request.method == "POST":
        if request.is_ajax():
            comment_id = json.loads(request.body.decode("utf-8"))["custom_id"]
            # try:
            comment = Comment.objects.prefetch_related().get(custom_id=comment_id)
            try:
                CommentLike.objects.prefetch_related().get(
                    comment=comment, user_who_liked_the_comment=request.user
                )
                response = "Already Liked"
            except:
                x = CommentLike.objects.create(
                    comment=comment, user_who_liked_the_comment=request.user
                )
                x.save()
                response = "Liked"
            # except:
            #     response = "No Comment"
            response_data = json.dumps({"response": response})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)


def removeCommentLike(request):
    if request.method == "POST":
        if request.is_ajax():
            comment_id = json.loads(request.body.decode("utf-8"))["custom_id"]
            try:
                comment = Comment.objects.prefetch_related().get(custom_id=comment_id)
                try:
                    x = CommentLike.objects.prefetch_related().get(
                        comment=comment, user_who_liked_the_comment=request.user
                    )
                    x.delete()
                    response = "Deleted"
                except:
                    response = "Already Not Liked"

            except:
                response = "No Comment"
            response_data = json.dumps({"response": response})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)


def deleteComment(request):
    if request.method == "POST":
        if request.is_ajax():
            comment_id = json.loads(request.body.decode("utf-8"))["custom_id"]
            try:
                comment = Comment.objects.prefetch_related().get(custom_id=comment_id)
                try:
                    if comment.user_who_commented == request.user:
                        comment.delete()
                        response = "Deleted"
                except:
                    response = "Not Authorised"
            except:
                response = "No Comment"
            response_data = json.dumps({"response": response})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)


def getIdFromUserName(request):
    if request.method == "POST":
        if request.is_ajax():
            username = json.loads(request.body.decode("utf-8"))["username"]
            try:
                user = User.objects.prefetch_related().get(username=username)
                response = user.custom_id
                status = 200
            except:
                response = "No User"
                status = 404
            response_data = json.dumps(
                {"response": response, "status": status})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)


def getBioData(request):
    if request.method == "POST":
        if request.is_ajax():
            username = json.loads(request.body.decode("utf-8"))["username"]
            try:
                user = User.objects.prefetch_related().get(username=username)
                response = {"bio": user.bio, "bio_links": user.get_bio_links}
                status = 200
            except:
                response = "No User"
                status = 404
            response_data = json.dumps(
                {"response": response, "status": status})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)


def getFollowerFollowing(request):
    if request.method == "POST":
        if request.is_ajax():
            username = json.loads(request.body.decode("utf-8"))["username"]
            try:
                user = User.objects.prefetch_related().get(username=username)
                response = {"posts": user.get_user_posts_length,
                            "followers": user.get_no_of_followers, "following": user.get_no_of_following}
                status = 200
            except:
                response = "No User"
                status = 404
            response_data = json.dumps(
                {"response": response, "status": status})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)


def getProfileUserData(request):
    if request.method == "POST":
        if request.is_ajax():
            username = json.loads(request.body.decode("utf-8"))["username"]
            try:
                user = User.objects.prefetch_related().get(username=username)
                try:
                    fo = Follow.objects.prefetch_related().get(
                        user_who_followed=request.user, user_who_is_followed=user)
                    fo = True
                except:
                    fo = False
                response = {"username": user.username, "name": user.full_name,
                            "dp": user.get_dp_path, "follows_request_user": fo}
                status = 200
            except:
                response = "No User"
                status = 404
            response_data = json.dumps(
                {"response": response, "status": status})
            mimetype = "application/json"
            return HttpResponse(response_data, mimetype)


def getProfilePosts(request):
    if request.method == "POST":
        if request.is_ajax():

            username = json.loads(request.body.decode("utf-8"))["username"]
            try:
                user = User.objects.prefetch_related().get(username=username)
                page = json.loads(request.body.decode("utf-8"))["page"]
                if page == 0:
                    profile_posts_list = ProfilePostList(
                        user=user, spec=request.user)
                    profile_posts_list.save()
                pl = ProfilePostList.objects.prefetch_related().get(user=user,
                                                                    spec=request.user)
                posts_dict = dict(json.loads(pl.profilePostList))
                counter = len(posts_dict.keys())
                start = page*POSTS_PER_PAGE
                stop = (page+1)*POSTS_PER_PAGE
                posts = list(posts_dict.values())
                has_more = True
                if stop >= counter:
                    has_more = False
                resp_posts = posts[start: stop]
                stop = (resp_posts == [])
                data = {}
                for i in resp_posts:
                    data[i['custom_id']] = i
                resp_posts = json.dumps({'data': data, 'response': "Successful",
                                         'has_more': has_more, 'stop': stop, 'status': 200, 'total': counter})

            except:
                resp_posts = json.dumps(
                    {'response': 'Unsuccessful', 'status': 404})
            mimetype = "application/json"
            return HttpResponse(resp_posts, mimetype)
