from django.db import models


class EventSource(models.Model):
	name = models.CharField(max_length=255)


class IcalEventSource(EventSource):
	url = models.CharField(max_length=255)


class Event(models.Model):
	summary = models.TextField(db_index=True, null=True)
	start_date = models.DateTimeField(null=True)
	end_date = models.DateTimeField(null=True)
	modified_date = models.DateTimeField(null=True)
	location = models.TextField(null=True)

	source = models.ForeignKey(to=EventSource)
	external_id = models.CharField(max_length=100, db_index=True)

	class Meta(object):
		unique_together = (('source', 'external_id'),)

