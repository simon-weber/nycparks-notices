import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDict
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache

from . import get_absolute_url
from .models import Status, Subscriber, FACILITIES

from django import forms
from django.forms import modelform_factory

logger = logging.getLogger(__name__)


# https://gist.github.com/stephane/00e73c0002de52b1c601
class ArrayFieldSelectMultiple(forms.SelectMultiple):
    def __init__(self, *args, **kwargs):
        # Accept a `delimiter` argument, and grab it (defaulting to a comma)
        self.delimiter = kwargs.pop('delimiter', ',')
        super().__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, MultiValueDict):
            # Normally, we'd want a list here, which is what we get from the
            # SelectMultiple superclass, but the SimpleArrayField expects to
            # get a delimited string, so we're doing a little extra work.
            return self.delimiter.join(data.getlist(name))

        return data.get(name)

    def get_context(self, name, value, attrs):
        return super().get_context(name, value.split(self.delimiter), attrs)


_f = sorted(list(FACILITIES))
facility_choices = list(zip(_f, _f))
SubscribeForm = modelform_factory(
    Subscriber,
    fields=("address", "facility_names"),
    widgets={'facility_names': ArrayFieldSelectMultiple(choices=facility_choices, attrs={'size': len(facility_choices) / 2})},
)


# keep in mind the cache key includes querystring
alerts = {
    # qstring: {'bootstrap type', 'message...'}
    'sub_success': ('success', "You'll receive an email confirming your subscription."),
    'unsub_success': ('success', "You have been unsubscribed."),
    'change_sub_success': ('success', "Your subscription has been changed."),
}


@cache_control(public=True, max_age=3600)
def index(request):
    c = {'alert': alerts.get(request.GET.get('alert'))}
    return render(request, "logged_out.html", c)


@cache_control(public=True, max_age=3600)
def statuses(request):
    statuses = Status.objects.all().order_by('facility_name')

    return render(request, "statuses.html", {'statuses': statuses})


@cache_control(public=True, max_age=3600)
def privacy(request):
    return render(request, "privacy.html")


@never_cache
def subscriber(request, key=None):
    c = {
        'FACILITIES': FACILITIES,
        'can_unsubscribe': False,
    }

    form_kwargs = {}
    if key:
        form_kwargs['instance'] = Subscriber.objects.get(key=key)
        c['can_unsubscribe'] = True
    if request.method == 'POST':
        form_kwargs['data'] = request.POST

    form = SubscribeForm(**form_kwargs)

    if request.method == 'POST' and form.is_valid():
        if request.POST.get("unsubscribe"):
            form.instance.delete()
            alert = 'unsub_success'
            logger.info("%s: %s", alert, form.instance)
        elif request.POST.get("subscribe"):
            s = form.save()
            alert = 'change_sub_success' if c['can_unsubscribe'] else 'sub_success'
            logger.info("%s: %s key %s", alert, s, s.key)
            if alert == 'sub_success':
                template = (
                    "Someone - hopefully you - signed up at {index_link} to receive emails about these locations:"
                    "{locations}"
                    "\n\nYou may unsubscribe at any time at: {unsub_link}"
                )
                body_c = {
                    'index_link': get_absolute_url('/'),
                    'locations': ''.join(['\n* ' + name for name in s.facility_names]),
                    'unsub_link': s.manage_absolute_url,
                }
                EmailMessage(
                    subject='Welcome!',
                    to=[s.address],
                    body=template.format_map(body_c),
                ).send(fail_silently=False)
        else:
            raise ValueError('unsupported action')
        return redirect("/?alert=%s" % alert)

    c['subscribe_form'] = form
    return render(request, "subscriber.html", c)


# These support favicons, which are templated since they refer to manifest-named static files.

@cache_control(public=True, max_age=3600)
def browserconfig(request):
    return render(request, "browserconfig.xml", content_type='application/xml')


@cache_control(public=True, max_age=3600)
def webmanifest(request):
    return render(request, "site.webmanifest", content_type='application/manifest+json')
