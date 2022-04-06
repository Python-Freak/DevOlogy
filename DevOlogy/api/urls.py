from django.contrib import admin
from django.urls import path, include
from .views import (knowIfLoggedIn, isUserNameAvailable, isEmailAvailable, getRequestUserInfo, getSearchResults,
                    getUserSuggestions, knowPostLikesAndBookmarks,  addLike, removeLike, addBookmark, removeBookmark, getPostData, comment, addCommentLike, removeCommentLike)
from core.views import getComments

urlpatterns = [
    path('isLoggedIn/', knowIfLoggedIn),
    path('isUserNameAvailable/', isUserNameAvailable),
    path('isEmailAvailable/', isEmailAvailable),
    path('getRequestUserInfo/', getRequestUserInfo),
    path("getSearchResults/", getSearchResults),
    path("getUserSuggestions/", getUserSuggestions),
    path("knowPostLikesAndBookmarks/", knowPostLikesAndBookmarks),
    path("addLike/", addLike),
    path("removeLike/", removeLike),
    path("addBookmark/", addBookmark),
    path("removeBookmark/", removeBookmark),
    path("getPostData/", getPostData),
    path("comment/", comment),
    path("getComments/", getComments),
    path("addCommentLike/", addCommentLike),
    path("removeCommentLike/", removeCommentLike)

]
