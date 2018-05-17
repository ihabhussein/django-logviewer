from django.db import models, connection
from django.utils.translation import ugettext_lazy as _


class Facility(models.Model):
    id = models.IntegerField(_('ID'), primary_key=True)
    title = models.CharField(_('Title'), max_length=32)

    def __str__(self):
        return self.title


class Priority(models.Model):
    id = models.IntegerField(_('ID'), primary_key=True)
    title = models.CharField(_('Title'), max_length=32)

    def __str__(self):
        return self.title


class Event(models.Model):
    time_reported = models.DateTimeField(_('Time Reported'), null=True)
    time_received = models.DateTimeField(_('Time Received'), null=True, db_index=True)
    host = models.CharField(_('Host'), max_length=32, null=True)
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True, db_index=True)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, db_index=True)
    message = models.TextField(_('Message'), null=True)
    tag = models.CharField(_('Program'), max_length=32, null=True, db_index=True)

    @classmethod
    def tags(self):
        result = []
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT regexp_replace(tag, '(\[\d+\]|-\d+|):$', '')
                  FROM rsyslog_event ORDER BY 1;
                """)
            for row in cursor.fetchall():
                result.append(row[0])
        return result
