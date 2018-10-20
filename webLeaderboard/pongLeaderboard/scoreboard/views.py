from django.http import HttpResponse
from .models import userScore
from django.core import serializers
import json

def index(request):
    return HttpResponse("Index of leaderboard")

def get(request):
	top_scores = userScore.objects.order_by('-score')[:5]
	scoresArr = []
	for q in top_scores:
		scoresArr.append(q.initials + '-' + str(q.score))
	print(scoresArr)
	toReturn = json.dumps(scoresArr)
	return HttpResponse(toReturn)

def post(request, initialsParam, scoreParam):
	#put object in database
	obj = userScore(initials = initialsParam, score=scoreParam)
	obj.save()
	print("Saved post " + str(obj.id))
	return HttpResponse("Saved {}'s score of {}".format(initialsParam, str(scoreParam)))
