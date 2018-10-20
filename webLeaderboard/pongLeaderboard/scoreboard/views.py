from django.http import HttpResponse
from .models import userScore

def index(request):
    return HttpResponse("Index of leaderboard")

def get(request):
	return HttpResponse(userScore.objects.all())

def post(request, initialsParam, scoreParam):
	#put object in database
	obj = userScore(initials = initialsParam, score=scoreParam)
	obj.save()
	print("Saved post " + str(obj.id))
	return HttpResponse("Saved {}'s score of {}".format(initialsParam, str(scoreParam)))
