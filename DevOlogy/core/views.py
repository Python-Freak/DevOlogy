from typing import Counter
from django.shortcuts import render, redirect, HttpResponse
from .models import Post
import json
from django.core import serializers
from django.contrib.auth import get_user_model
import time
from .models import PostList, CommentList
# Create your views here.

MAX = 1000
posts_per_page = 21 
comments_per_page = 11 

def checkLogin(user):
    return user.is_authenticated 


def feed(request):
    if request.method == 'GET':
        if checkLogin(request.user):
            return render(request, 'frontend/index.html')
        else:
            return redirect('login/')
    elif request.method == "POST":
        if request.is_ajax():
            page = json.loads(request.body.decode())['page']
            if page == 0:
                pl = PostList()
                pl.save()
            pl = PostList.objects.get(user=request.user)
            posts_dict = dict(json.loads(pl.post_list))
            counter = len(posts_dict.keys())
            start = page*posts_per_page
            stop = (page+1)*posts_per_page
            posts = list(posts_dict.values())
            has_more = True
            if stop >= counter:
                has_more = False
            resp_posts = posts[start : stop]
            
            stop = (resp_posts == [])
            response = {}
            for i in resp_posts:
                response[i['custom_id']] = i
            resp_posts = json.dumps({'response': response, 'has_more': has_more, 'stop': stop})
            mimetype = 'application/json'
            return HttpResponse(resp_posts, mimetype)
            

    else:
        return HttpResponse("Page Not Found") # TODO
        

def post(request, post_id):
    if checkLogin(request.user):
        return render(request, 'frontend/index.html')
    else:
        return redirect('login/')
    

def profile(request, username):
    if checkLogin(request.user):
        return render(request, 'frontend/index.html')
    else:
        return redirect('login/')

def getComments(request):
    if request.method == 'POST':
        if request.is_ajax():
                post_id = json.loads(request.body.decode())['post_id']
            # try:
                post = Post.objects.get(custom_id=post_id)
                page = json.loads(request.body.decode())['page']
                if page == 0:
                    comment_list = CommentList(post = post)
                    comment_list.save()
                
                cl = CommentList.objects.get(post=post)
                
                comments_dict = dict(json.loads(cl.comments_list))
                counter = len(comments_dict.keys())
                print(counter)
                start = page*comments_per_page
                stop = (page+1)*comments_per_page
                comments = list(comments_dict.values())
                has_more = True
                if stop >= counter:
                    has_more = False
                resp_comments = comments[start : stop]
                print(has_more)
                stop = (resp_comments == [])
                response = {}
                for i in resp_comments:
                    response[i['custom_id']] = i
                    resp_comments = json.dumps({'response': response, 'has_more': has_more, 'stop': stop, 'status': 200, 'total': counter})
                mimetype = 'application/json'
                return HttpResponse(resp_comments, mimetype)

                
            # except:
            #     resp_posts = json.dumps({'status': 404})
            #     mimetype = 'application/json'
            #     return HttpResponse(resp_posts, mimetype)
