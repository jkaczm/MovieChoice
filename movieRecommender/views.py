from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
import json

def app(request):
    #conn = sqlite3.connect('movieRecommender.db')
    #cur = conn.cursor()
    #cur.execute("""SELECT movieId, rating FROM ratings WHERE userId = '1'""")
    #return HttpResponse(str(cur.fetchone()))
    return render(request,'movieRecommender/app.html')

def getMovieIds(request):
    conn = sqlite3.connect('movieRecommender.db')
    cur = conn.cursor()
    cur.execute("""SELECT movieId, title FROM movies ORDER BY RANDOM() LIMIT 20""")
    movieList = cur.fetchall()
    conn.close()
    return HttpResponse(json.dumps(movieList))

def testJsonRequest(request):
    # to get parameter "name" (From getMovieIds originally)
    # name = request.GET["name"]

    # receive and parse JSON data
    JSON_data = request.GET["JSON"]
    ratings_info = json.loads(JSON_data)
    # create and send new JSON
    samepleList = ["movie1", "movie2", "movie3"]
    asString = json.dumps(samepleList)
    return HttpResponse(asString)

def getRecommendations(request):
    # set up connection to database
    conn = sqlite3.connect('movieRecommender.db')
    cur = conn.cursor()

    # parse JSON data
    raw_JSON = request.GET["JSON"]
    user_data = json.loads(raw_JSON)
    # print for testing purposes
    print(user_data[0])
    print(user_data[1])

    # variable to store user's average rating
    user_avg_rating = 0
    for rating in user_data:
        user_avg_rating += rating[1]
    user_avg_rating /= len(user_data)
    # for testing purposes
    print("User avg rating:", user_avg_rating)

    # variable to store list of movies user has rated
    movies_rated_by_user = [str(rating[0]) for rating in user_data]

    # list of user's who have rated movies in common
    users_with_movies_in_common = []
    cur.execute("""SELECT userId FROM ratings WHERE movieId IN %s""" % str(tuple(movies_rated_by_user)))
    users_with_movies_in_common = list(set(cur.fetchall()))
    

    # work on this part



    # close database connection 
    conn.close()

    return HttpResponse(json.dumps(user_data))