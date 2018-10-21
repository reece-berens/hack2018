from django.db import models

# Create your models here.
class userScore(models.Model):
	initials = models.CharField(max_length=9)
	score = models.IntegerField(default=0)
	
	def __str__(self):
		return self.initials + '-' + str(self.score) #+ '~'
