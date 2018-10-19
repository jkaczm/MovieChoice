from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
import json
import time

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
    # get starting time of function
    start_time = time.time()

    # set up connection to database
    conn = sqlite3.connect('movieRecommender.db')
    cur = conn.cursor()

    # parse JSON data
    raw_JSON = request.GET["JSON"]
    user_data = json.loads(raw_JSON)
    # print for testing purposes
    for pair in user_data:
        print("User gave movie", pair[0], "a rating of", pair[1])

    # variable to store user's average rating
    user_avg_rating = 0
    for rating in user_data:
        user_avg_rating += rating[1]
    user_avg_rating /= len(user_data)
    # for testing purposes
    print("The average movie rating of user:", user_avg_rating)

    # variable to store list of movies user has rated
    movies_rated_by_user = [str(rating[0]) for rating in user_data]

    # list of user's who have rated movies in common
    cur.execute("""SELECT userId FROM ratings WHERE movieId IN %s""" % str(tuple(movies_rated_by_user)))
    users_with_movies_in_common = set(cur.fetchall())
    # print for testing purposes
    print("The number of users who have rated movies in common: ", len(users_with_movies_in_common))

    # get list of movies to iterate over (movies rated by users who have rated movies in common)
    cur.execute("""SELECT movieId FROM ratings WHERE userId IN %s""" % str(tuple([str(record[0]) for record in users_with_movies_in_common])))
    movies_to_iterate_over = set(cur.fetchall())
    # print for testing purposes
    print("The number of possible movies to iterate over:", len(movies_to_iterate_over))

    # Priority queue of movies to recommend
    movies_to_recommend = []
    # count to keep track of how many movies were considered for recommendation
    count = 0

    for movie in movies_to_iterate_over:
        # variable to hold the predicted rating of the movie
        predicted_rating = 0
        # variable to hold the sum of the absolute value of pearson correlation for the denominator of formula
        sum_of_pearson_correlation = 0
        # variable to hold the value of the numerator of formula
        value_of_numerator = 0

        # users to iterate over are uers who rated movie and have rated movies in common
        cur.execute("""SELECT userId FROM ratings WHERE movieId=?""", movie)
        users_who_have_rated_movie = set(cur.fetchall())
        users_to_iterate_over = users_who_have_rated_movie & users_with_movies_in_common
        # print for testing purposes
        # print("For movieId:", movie, "Users to Iterate Over:", users_to_iterate_over)
        
        # if too few users who have rated movie, skip it
        if len(users_to_iterate_over) < 10:
            # print for testing purposes
            # print("Too few users, skipping movie:", movie[0])
            continue

        # for each user to iterate over
        for user in users_to_iterate_over:
            cur.execute("""SELECT AVG(rating) FROM ratings WHERE userId=?""", user)
            avg_rating = cur.fetchall()[0][0]
            # print for testing purposes
            # print("UserId: ", user, "Average rating: ", avg_rating)
            pass
        
        # if either 20 movies were considered for review or the program is taking longer than 10 seconds, quit
        count += 1
        if(count == 20 or (time.time() - start_time > 10)):
            break



    
    # close database connection 
    conn.close()

    # print total time algorithm took
    print("The algorithm took %s seconds" % (time.time() - start_time))
    print("The algorithm considered ", count, "movies for recommendation")

    # return list of recommended movies as JSON
    return HttpResponse(json.dumps(user_data))