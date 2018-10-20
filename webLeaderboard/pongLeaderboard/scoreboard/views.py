from django.http import HttpResponse
from .models import userScore
from django.core import serializers

def index(request):
    return HttpResponse("Index of leaderboard")

def get(request):
	"""
	ordered_scores = (userScore.objects
		.order_by('-score')
		.values_list('score', flat=True)
		.distinct())
	top_records = (userScore.objects
		.order_by('-score')
		.filter(score__in=ordered_scores[:5]))
	"""
	top_scores = serializers.serialize('json', userScore.objects.order_by('-score')[:5], fields=('initials', 'score'))
	#score_list = []
	#for score in top_scores:
	#	score_list.append(score)
	return HttpResponse(top_scores)

def post(request, initialsParam, scoreParam):
	#put object in database
	obj = userScore(initials = initialsParam, score=scoreParam)
	obj.save()
	print("Saved post " + str(obj.id))
	return HttpResponse("Saved {}'s score of {}".format(initialsParam, str(scoreParam)))
