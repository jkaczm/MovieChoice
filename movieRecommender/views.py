from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
import json
import time
from math import sqrt
import heapq

def app(request):
    #conn = sqlite3.connect('movieRecommender.db')
    #cur = conn.cursor()
    #cur.execute("""SELECT movieId, rating FROM ratings WHERE userId = '1'""")
    #return HttpResponse(str(cur.fetchone()))
    return render(request,'movieRecommender/app.html')

def about(request):
    return render(request,'movieRecommender/about.html')

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
    # print for testing purposes
    print("*************************************************************************************")
    print("The algorithm begins execution")
    print("*************************************************************************************")

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

    # variable to store dictionary of ratings
    user_dict = dict(zip([rating[0] for rating in user_data],[rating[1] for rating in user_data]))
    # print for testing purposes
    print("The dictionary of user data:", user_dict)

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

    # heap of movies to recommend
    movies_to_recommend = []

    # count to keep track of how many movies were considered for recommendation
    count = 0

    for movie in movies_to_iterate_over:
        # variable to hold the predicted rating of the movie
        predicted_rating_numerator = 0
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
            # compute average rating
            cur.execute("""SELECT AVG(rating) FROM ratings WHERE userId=?""", user)
            avg_rating = cur.fetchall()[0][0]
            # get movies user has rated
            cur.execute("""SELECT movieId, rating FROM ratings WHERE userId=?""", user)
            # create a dictionary where movieId is key and rating is value
            dict_of_movies_user_in_database_has_rated = dict(cur.fetchall())
            # use list of movies in common to compute pearson correlation
            temp_pearson_numerator = 0
            temp_pearson_denom_left = 0
            temp_pearson_denom_right = 0
            for key in user_dict:
                if str(key) in dict_of_movies_user_in_database_has_rated:
                    x = user_dict[key] - user_avg_rating
                    y = int(float(dict_of_movies_user_in_database_has_rated[str(key)])) - avg_rating
                    temp_pearson_numerator += x * y
                    temp_pearson_denom_left += x * x
                    temp_pearson_denom_right += y * y
            try:
                pearson_correlation = temp_pearson_numerator / (sqrt(temp_pearson_denom_left) * sqrt(temp_pearson_denom_right))
            except ArithmeticError:
                # print for testing purposes
                print("Division by Zero Exception")
                pearson_correlation = 0

            sum_of_pearson_correlation += abs(pearson_correlation)
            predicted_rating_numerator += pearson_correlation * (int(float(dict_of_movies_user_in_database_has_rated[movie[0]])) - avg_rating)

        # compute predicted rating
        try:
            predicted_rating = user_avg_rating + (predicted_rating_numerator / sum_of_pearson_correlation)
        except ArithmeticError:
            predicted_rating = user_avg_rating

        # print for testing purposes
        print("The predicted rating for movie", movie[0], "is", predicted_rating)

        # add movie to heap of movies (It is a min heap, so subtract rating from 5 to make it a max heap)
        heapq.heappush(movies_to_recommend, (5 - predicted_rating, movie))

        # if either 20 movies were considered for review or the program is taking longer than 10 seconds, quit
        count += 1
        if(count == 40 or (time.time() - start_time > 20)):
            break

    # print total time algorithm took
    print("**********************************************************************************")
    print("The algorithm took %s seconds" % (time.time() - start_time))
    print("The algorithm considered ", count, "movies for recommendation")
    print("**********************************************************************************")

    # return list of recommended movies as JSON
    data_to_return = []
    for x in range(5):
        top_value_of_heap = heapq.heappop(movies_to_recommend)
        top_movie = top_value_of_heap[1]
        top_rating = 5 - top_value_of_heap[0]
        cur.execute("""SELECT title FROM movies WHERE movieId=?""", top_movie)
        movie_title = cur.fetchall()[0][0]
        # print for testing purposes
        print(x + 1, "The algorithm recommends movie", movie_title, "with predicted rating", top_rating)
        data_to_return.append([movie_title, top_rating])

    # close database connection 
    conn.close()

    # print for testing purposes
    print("**********************************************************************************")
    print("The algorithm finished executing")
    print("**********************************************************************************")

    # return top five movies to recommend in order
    return HttpResponse(json.dumps(data_to_return))