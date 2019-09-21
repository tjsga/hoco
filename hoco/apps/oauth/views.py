import json

from oauthlib.oauth2.rfc6749.errors import InvalidGrantError
from requests_oauthlib import OAuth2Session

from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

# Create your views here. 
def login(request):
    oauth = OAuth2Session(settings.CLIENT_ID, redirect_uri=settings.REDIRECT_URI, scope=["read"])
    if "error" in request.GET:
        return redirect(reverse("login"))
    if "code" not in request.GET:
        authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")
        return redirect(authorization_url)
    try:
        oauth.fetch_token("https://ion.tjhsst.edu/oauth/token/", code=request.GET["code"], client_secret=settings.CLIENT_SECRET)
        profile = oauth.get("https://ion.tjhsst.edu/api/profile")
        user_data = json.loads(profile.content.decode())
        
        authorized_user = False
        authorized_users = ["2021abhave", "2020rranjan"]
        for user in authorized_users: 
            if user == user_data["ion_username"]: 
                authorized_user = True
        
        request.session["user"] = user_data["ion_username"]
        request.session["admin"] = user_data["is_teacher"] or user_data["is_eighth_admin"] or authorized_user
        return redirect(reverse("index"))
    except InvalidGrantError:
        return redirect(reverse("login"))