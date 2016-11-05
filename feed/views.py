from django.http import HttpResponse
from eentv.settings import CURR_ENV, ENV_PROD
from feed.models import Event, IcalEventSource
from feed.services import cron_task_update_icals
from services import generate_ical


def index(request):
	return HttpResponse("Hello, OpenBracket2016.")

def _ical_response(events):
	content_type = 'text/calendar' if CURR_ENV == ENV_PROD else 'text/plain'
	return HttpResponse(generate_ical(events), content_type=content_type)


def feed_add_ical(request):
	url = request.GET.get('url', '')
	name = request.GET.get('name', '')
	IcalEventSource.objects.create(url=url, name=name)
	return HttpResponse('Added Ical Event Source [name={}, url={}]!'.format(name, url))


def feed_all(request):
	return _ical_response(Event.objects.all())


def feed_filter(request):
	query = request.GET.get('search', '')
	events = Event.objects.filter(summary__icontains=query)
	return _ical_response(events)


def force_update_icals(request):
	cron_task_update_icals()
	return HttpResponse('Updated!')
