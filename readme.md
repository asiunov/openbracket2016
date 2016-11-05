I use python 2.7.10

To init env and db:
pip install django-crontab
python manage.py migrate

To run cron and web server:
python manage.py crontab add
python manage.py runserver


So, you have access to the server!

To add new iCal, go to page like this (you need to specify params 'name' and 'url'):
http://127.0.0.1:8000/feed/add_ical_source?name=Philly-Loves-Boardgames&url=http://www.meetup.com/Philly-Loves-Boardgames/events/ical/

To see all events:
http://127.0.0.1:8000/feed/all

To find events:
http://127.0.0.1:8000/feed/filter?search=Night

To force update events from sources:
http://127.0.0.1:8000/feed/force_update_icals
