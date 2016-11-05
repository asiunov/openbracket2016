import datetime
import urllib2
from dateutil.tz import tzutc
from pytz import utc
from feed.models import Event, IcalEventSource
from utils import log


TZ_UTC = tzutc()


def _escape_chars(value):
	# todo
	return value


def _ical_param(label, value):
	if value is None:
		return ''
	elif isinstance(value, datetime.datetime):
		value = value.astimezone(TZ_UTC).strftime('%Y%m%dT%H%M%SZ')
	elif isinstance(value, (int, long)):
		value = str(value)
	elif isinstance(value, basestring):
		value = _escape_chars(value)
	else:
		raise Exception("Unknown field type")
	return "{}:{}".format(label, value)


def _append_ical_event(lines, event):
	lines.append('BEGIN:VEVENT')
	values = [
		('SUMMARY', event.summary),
		('UID', event.id),
		('DTSTART', event.start_date),
		('DTEND', event.end_date),
		('LAST-MODIFIED', event.modified_date),
		('LOCATION', event.location),
	]

	for label, value in values:
		line = _ical_param(label, value)
		if line:
			lines.append(line)

	lines.append('END:VEVENT')


def generate_ical(events):
	lines = []
	lines.append('BEGIN:VCALENDAR')
	lines.append('VERSION:2.0')
	lines.append('PRODID:-//FAndES.ru//Eentv//EN')

	for event in events:
		_append_ical_event(lines, event)

	lines.append('END:VCALENDAR')
	return '\n'.join(lines)


def _ical_assert(b):
	if not b:
		raise Exception('Ical parsing failed')


def _parse_ical_next(values, ifrom, ito):
	res = dict()
	i = ifrom
	while i <= ito:
		if values[i][0] == 'BEGIN':
			q = []
			j = i
			while i <= ito:
				if values[i][0] == 'BEGIN':
					q.append(values[i][1])
				elif values[i][0] == 'END':
					if len(q) == 0:
						raise Exception()
					if q[-1] != values[i][1]:
						# log('{} {}', q[-1], values[i][1])
						raise Exception()
					q.pop()
				i += 1
				if len(q) == 0:
					break
			if len(q) != 0:
				raise Exception()
			if values[i - 1][1] != values[j][1]:
				raise Exception()
			if values[j][1] not in res:
				res[values[j][1]] = list()
			res[values[j][1]].append(_parse_ical_next(values, j + 1, i - 2))
		else:
			res[values[i][0]] = values[i][1]
			i += 1

	return res


def _parse_ical(content):
	content = content.replace('\r', '')
	values = []
	for line in content.split('\n'):
		if not line.strip():
			continue
		if line[0] == ' ':
			key, value = values[-1]
			values[-1] = (key, value + line[1:])
		else:
			tmp = line.split(':', 1)
			if len(tmp) != 2:
				log('Exception {}', tmp)
				raise Exception()
			key = tmp[0].upper()
			# todo hack hack (sometimes, DTSTART or DTEND may be in format 'DTSTART;TZ_INFO', so, for now we just clean it)
			if key.startswith('DTSTART'):
				key = key[:len('DTSTART')]
			if key.startswith('DTEND'):
				key = key[:len('DTEND')]
			value = tmp[1]
			if key in ('BEGIN', 'END'):
				value = value.upper()
			values.append((key, value))

	return _parse_ical_next(values, 0, len(values) - 1)


def _parse_date(value):
	if not value:
		return None
	return utc.localize(datetime.datetime.strptime(value.strip('Z'), '%Y%m%dT%H%M%S'))


def update_ical_events(ical_event_source):
	request = urllib2.Request(
		ical_event_source.url,
		headers={
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	)
	ical = _parse_ical(urllib2.urlopen(request).read())
	for event_dict in ical['VCALENDAR'][0].get('VEVENT', list()):
		event = list(Event.objects.filter(source=ical_event_source, external_id=event_dict.get('UID')))
		_ical_assert(len(event) <= 1)
		event = event[0] if len(event) == 1 else Event(source=ical_event_source, external_id=event_dict.get('UID'))

		event.summary = event_dict.get('SUMMARY')
		event.start_date = _parse_date(event_dict.get('DTSTART'))
		event.end_date = _parse_date(event_dict.get('DTEND'))
		event.modified_date = _parse_date(event_dict.get('LAST-MODIFIED'))
		event.location = event_dict.get('LOCATION')

		event.save()


def cron_task_update_icals():
	for source in IcalEventSource.objects.all():
		update_ical_events(source)
