from django.conf import settings

import requests


def get_absolute_url(path, **r_kwargs):
    # I can't believe django doesn't have a way to do this that's not dependent on sites / requests

    url = "%s://%s" % (settings.SCHEME, settings.HOST)
    port = getattr(settings, 'PORT')
    if port:
        url += ":%s" % port
    url += path

    r = requests.Request('GET', url, **r_kwargs)
    return r.prepare().url
