from collections import defaultdict
import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.timezone import now
from lxml import html, etree
import requests


from . import get_absolute_url
from .models import Notice, Status, FACILITIES, Subscriber


BASE_URL = 'https://www.nycgovparks.org'
NOTICE_URL = BASE_URL + '/news/notices'


logger = logging.getLogger(__name__)


def get_notices():
    # Return a set of Notices from the status page.

    req = requests.get(NOTICE_URL)
    tree = html.fromstring(req.content)
    notices = tree.xpath('//*[contains(@class,"closure_det")]')

    results = set()

    def finish_notice(facility_name, facility_path, paragraphs):
        if facility_name not in FACILITIES:
            logger.debug("unknown facility %r: %s %s", facility_name, facility_path, ''.join(paragraphs))

        results.add(Notice(facility_name, BASE_URL + facility_path, ''.join(paragraphs)))

    for notice in notices:
        facility_name = None
        facility_path = None
        paragraphs = []

        notice_paras = notice.getchildren()
        for part in notice_paras:
            assert part.tag == 'p'  # TODO. probably xpath for paras and not, then warn on any not

            contents = part.getchildren()
            if len(contents) == 1 and contents[0].tag == 'a' and not contents[0].text:
                # links mark new closures
                link = contents[0]

                if facility_name is not None:
                    # close out an old notice
                    finish_notice(facility_name, facility_path, paragraphs)
                    paragraphs = []

                # begin the new notice
                facility_name = link.text_content()
                facility_path = link.get('href')
            else:
                # continuing notice html
                paragraphs.append(etree.tostring(part, encoding='unicode', method='html'))

        # close a remaining notice
        finish_notice(facility_name, facility_path, paragraphs)

    return results


def sync_statuses():
    old_statuses = {s.to_notice(): s for s in Status.objects.all()}
    old_notices = old_statuses.keys()

    new_notices = get_notices()

    ended = old_notices - new_notices
    continued = old_notices & new_notices
    started = new_notices - old_notices

    for notice in ended:
        logger.info('ending %r', notice)
        old_statuses[notice].delete()
    for notice in continued:
        logger.debug('continuing %r', notice)
        status = old_statuses[notice]
        status.last_seen = now()
        status.save()
    for notice in started:
        logger.info('starting %r', notice)
        Status.from_notice(notice).save()

    logger.info('ended: %s, continued: %s, started: %s', len(ended), len(continued), len(started))

    return ended, continued, started


def notify_subscribers(notices):
    facility_notices = defaultdict(list)
    for notice in notices:
        facility_notices[notice.facility_name].append(notice)

    subscribers = Subscriber.objects.all()
    emails = []
    for subscriber in subscribers:
        notices = []
        for facility in subscriber.facility_names:
            notices.extend(facility_notices[facility])
        if notices:
            notices_html = '\n\n'.join(
                ('<h3>'
                 '<a href="{facility_link}">{facility_name}</a>'
                 '</h3>'
                 '{html_content}').format_map(n._asdict())
                for n in sorted(notices)
            )
            body_html_template = (
                "<p>Here's an update on your facilities:</p>"
                "{notices_html}"
                '<hr>'
                '<p><a href="{index_link}">NYC Park Alerts</a></p>'
                '<br/><a href="{unsub_link}">manage your subscription</a>'
            )
            body_c = {
                'notices_html': notices_html,
                'index_link': get_absolute_url('/'),
                'unsub_link': subscriber.manage_absolute_url,
            }
            msg = EmailMessage(
                subject='New Facility Notice',
                to=[subscriber.address],
                body=body_html_template.format_map(body_c),
            )
            msg.content_subtype = "html"
            emails.append(msg)

    return emails


def run():
    # django-utilities script interface
    _, _, started = sync_statuses()
    emails = notify_subscribers(started)
    for email in emails:
        email.send(fail_silently=False)


if __name__ == '__main__':
    run()
