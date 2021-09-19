from django.shortcuts import redirect, render
from django.contrib import messages
import tweepy

from . import twitterAPI
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .utils import addHandleUtil, handleExists

from .models import UserHandlesMap

# Create your views here.
def loadFeed(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login/register to view this page!")
        return redirect("/login")

    user_handles = UserHandlesMap.objects.filter(user=request.user)

    if(user_handles.exists()):
        handles = list(user_handles)
        for i in range(len(handles)):
            handles[i] = handles[i].handle
    else:
        handles = []

    return render(request, "feed.html", {'handles': handles})

def addHandle(request):   
    return render(request, "add_handle.html")

def removeHandle(request, handle):
    user_handles = UserHandlesMap.objects.filter(user=request.user, handle=handle)
    user_handles.delete()
    messages.success(request, "Deleted handle added successfully!")
    return redirect("/feed")

class SearchUsers(APIView):
    
    def get(self, request):
        return Response("You aren't supposed to be here, trespasser!")
    
    def post(self, request):
        search_query = request.data.get("query")

        if not search_query:
            return Response({'results': 'Query parameters are missing!'}, 400)

        results = tweepy.Cursor(twitterAPI.search_users, q=search_query).items(10)
        results = [i for i in results]

        for i in range(0, len(results)):
            results[i] = handleExists(self.request.user, results[i])

        results = list(map(lambda user: UserSerializer(user), results))
        results = list(map(lambda serialized: JSONRenderer().render(serialized.data), results))
        return Response({'results': results})

class AddUsers(APIView):
    
    def get(self, request):
        return Response("You aren't supposed to be here, trespasser!")
    
    def post(self, request):
        handle = request.data.get("handle")

        if not handle:
            return Response({'results': 'Query parameters are missing!'})

        addHandleUtil(self.request.user, handle)
        return Response({'results': 'Handle added successfully'}, 201)
