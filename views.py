from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.context_processors import csrf
from django.template import RequestContext
import json
import requests
import urllib.parse
from collections import defaultdict
import datetime
import dateutil.parser
import json

def home(request):
	if request.method == 'POST' and request.is_ajax():
		username = request.POST['username']
		year = 2016 #datetime.datetime.now().year
		# Starting date of the year
		start_date = datetime.datetime(year, 1, 1, 00, 00, 00)
		# Ending date of the year
		end_date = datetime.datetime(year, 12, 31, 23, 59, 59)

		generalParameters = {'action': 'query',
		           'format': 'json',
		           'list': 'usercontribs',
		           'uclimit':'max',
		           'ucuser':username,
		           'ucdir':'newer',
		           'ucnamespace':0,
		           'ucstart':start_date.isoformat(' '),
		           'ucend':end_date.isoformat(' ')
		           }
		articlesCreatedParameters = generalParameters.copy()
		articlesEditedParameters = generalParameters.copy()
		articlesCreatedParameters['ucshow'] = "new"
		articlesEditedParameters['ucshow'] = "!new"
		# For articles created
		articlesCreatedDates = getContributionTimelineData(articlesCreatedParameters)
		# For articles edited
		articlesEditedDates = getContributionTimelineData(articlesEditedParameters)
		return HttpResponse(json.dumps({'articlesCreatedDates':articlesCreatedDates, 'articlesEditedDates':articlesEditedDates}), content_type="application/json")
	return render(request, 'home.html', {})


def getContributionTimelineData(parameters):
	contributionDatesDict = defaultdict(int) # default value of int is 0
	url='https://en.wikipedia.org/w/api.php'
	while True:
		url_parameters = urllib.parse.urlencode(parameters)
		formatted_url =  (url + '?{}').format(url_parameters)
		response_object = requests.get(formatted_url)
		if response_object.status_code == 200:
				# Loading the response data into a dict variable
				# json.loads takes in only binary or string variables so using text to fetch binary content
				# Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
				json_data = json.loads(response_object.text)
				try:
					 # if username is not valid
					if json_data['error']:
						print("Error", json_data['error']['info'])
				except:
					contribution_data = [i for i in json_data['query']['usercontribs']]
					 # if user has no edits
					if len(contribution_data) == 0:
						print("0 edits found")
					else:
						for contribution_details in contribution_data:
							timestamp = dateutil.parser.parse(contribution_details['timestamp'])
							contributionDatesDict[str(timestamp.date())] += 1
						print(len(contribution_data))
				if 'continue' in json_data:
					parameters['uccontinue'] = json_data['continue']['uccontinue']
					parameters['continue'] = json_data['continue']['continue']
				else:
					return contributionDatesDict
					break

		else:
				# If response code is not ok (200), print the resulting http error code with description
				response_object.raise_for_status()