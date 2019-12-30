from collections import namedtuple
import json
import os
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse

from . import get_absolute_url


FACILITY_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'rec_centers.json',
)
with open(FACILITY_FILE_PATH) as f:
    FACILITIES = {r['name'] for r in json.load(f)}


# These are keyed by name since ids are not used consistently.
Notice = namedtuple(
    'Notice',
    ['facility_name', 'facility_link', 'html_content']
)


class Status(models.Model):
    class Meta:
        verbose_name_plural = "Statuses"

    # A Status is a Notice with times associated with it.
    facility_name = models.TextField()
    facility_link = models.TextField()
    html_content = models.TextField()

    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now_add=True)

    @classmethod
    def from_notice(cls, notice):
        return cls(**notice._asdict())

    def to_notice(self):
        return Notice(self.facility_name, self.facility_link, self.html_content)

    def __str__(self):
        return "Status(%s to %s: %s)" % (
            self.first_seen.strftime('%Y-%m-%d %H:%M'),
            self.last_seen.strftime('%Y-%m-%d %H:%M'),
            self.to_notice()
        )

    __repr__ = __str__


class Subscriber(models.Model):
    address = models.EmailField(unique=True, verbose_name='email address')
    facility_names = ArrayField(
        models.TextField(),
        verbose_name='locations',
        help_text=("Don't see your location?"
                   ' <a href="mailto:simon@simonmweber.com?subject=Please add my NYC Parks location">'
                   "Email me</a> and I'll add it."),
        default=list)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return "Subscriber(%s: %r)" % (self.address, self.facility_names)

    __repr__ = __str__

    @property
    def manage_path(self):
        return reverse('subscriber', kwargs={'key': self.key})

    @property
    def manage_absolute_url(self):
        return get_absolute_url(self.manage_path)
