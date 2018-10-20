import json
import requests

def postScore(initials, score):
	postReq = requests.post('localhost:8000/scoreboard/post/' + initials + '/' + str(score))
	
def getScoreboard():
	getReq = requests.get('http://localhost:8000/scoreboard/get/')
	arr = json.loads(getReq.text)
	print(arr)
	ret = []
	for item in arr:
		s = item.split('-')
		ret.append((s[0], s[1]))
	return ret
	
if __name__ == '__main__':
	board = getScoreboard()
