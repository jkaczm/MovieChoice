from django.shortcuts import render
from django.http import HttpResponse
import sqlite3

def app(request):
    #conn = sqlite3.connect('movieRecommender.db')
    #cur = conn.cursor()
    #cur.execute("""SELECT movieId, rating FROM ratings WHERE userId = '1'""")
    #return HttpResponse(str(cur.fetchone()))
    return render(request,'movieRecommender/app.html')


