localrefresh:
	echo 'Status.objects.all().delete()' | python manage.py shell_plus \
	&& python manage.py runscript -v2 parkalerts.core.scrape

remoterefresh:
	echo 'Status.objects.all().delete()' | heroku run -x --no-tty python manage.py shell_plus \
	&& heroku run -x --no-tty python manage.py runscript -v2 parkalerts.core.scrape

remotesubs:
	echo 's = Subscriber.objects.all(); print(len(s)); print(s)' | heroku run -x --no-tty python manage.py shell_plus

deploy:
	git push heroku \
	&& curl -X POST "https://api.cloudflare.com/client/v4/zones/ea0960a7175f091da7344812320e9d99/purge_cache" \
	-H "X-Auth-Email: ${CFLARE_EMAIL}" \
	-H "X-Auth-Key: ${CFLARE_KEY}" \
	-H "Content-Type: application/json" \
	--data '{"files":["https://parks.simon.codes/", "https://parks.simon.codes/statuses/"]}'
