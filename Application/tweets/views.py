from urllib import response
from .models import Tweets, User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404
from .serializers import TweetsSerializer, UserSerializer
from datetime import datetime, timedelta
from django.utils import timezone



class TweetList(APIView):
    authentication_class = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        queryset = Tweets.objects.select_related('user_id').all()
        serializer = TweetsSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = TweetsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TweetsDetails(APIView):
    authentication_class = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def check_valid_user(func):
        def inner(inst, *args, **kwargs):
            request =  args[0]
            try:
                str(request.query_params.get('username'))
            except:
                return Response({
                    'status':False, 
                    'message':'Enter Username as string'
                    }, status = status.HTTP_400_BAD_REQUEST)
            return func(inst, *args, **kwargs)
        return inner

    
    def check_valid_date(func):
        def inner(inst, *args, **kwargs):
            request =  args[0]
            try:
                datetime.strptime(request.query_params.get('date'), "%Y-%m-%d")
            except:
                return Response({
                    'status':False, 
                    'message':'Enter valid date in yyyy-mm-dd'
                    }, status = status.HTTP_400_BAD_REQUEST)
            return func(inst, *args, **kwargs)
        return inner
        

    def tweets_lists(self, request):
        user = User.objects.filter(username=request.query_params.get('username'))
        response = {
            'status':True,
            'message':'',
            'TweetsLen': 0,
        }
        if not user:
            response.update({
                'status':False,
                'message':'No user found',
                'status_code': 404,
            })
            return response
        if request.method == 'GET':
            enddate = timezone.now()
            time = request.query_params.get("date")
            startdate = datetime.strptime(time, "%Y-%m-%d")
            response['message'] = 'Tweet List'
            query_set = Tweets.objects.filter(
                user_id=user[0].id,
                tweet_created_at__range = [startdate, enddate]
            )
        else:
            response['message'] = 'Deleted Tweet List'
            query_set = Tweets.objects.filter(user_id=user[0].id)
        tweets = []
        for tweet in query_set:
            serializer = TweetsSerializer(tweet)
            data = serializer.data
            tweets.append(data)
            if request.method == 'DELETE':
                tweet.delete()
        if request.method == 'DELETE':
            response.update({'deletedTweets':tweets})
        else:
            response.update({'Tweets':tweets})
        response['TweetsLen'] = len(tweets)
        return response


    @check_valid_user
    @check_valid_date
    def get(self, request):
        # TODO check the variables and other things
        return Response(self.tweets_lists(request), status=status.HTTP_200_OK)


    def post(self, request):
        serializer = TweetsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def delete(self, request, id):
        return Response(self.tweets_lists(request), status=status.HTTP_204_NO_CONTENT)


class UsersList(APIView):

    authentication_class = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        response = {
            'message':"Created Successfully",
            'success':True,
            'response_code':200
        }
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            response.update({
                "message":str(e),
                "response_code":401,
                "success":False,
            })
        if response.get('success'):
            serializer.save()
            response.update(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED)







        


