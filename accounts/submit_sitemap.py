from django.core.management.base import BaseCommand
import requests
from django.conf import settings

class Command(BaseCommand):
    help = 'Submit sitemap to Google'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='Your site URL (e.g. https://example.com)',
            default=getattr(settings, 'SITE_URL', None))
    
    def handle(self, *args, **options):
        site_url = options['url']
        if not site_url:
            self.stderr.write(self.style.ERROR(
                'Please provide site URL with --url or set SITE_URL in settings.py'
            ))
            return
        
        sitemap_url = f'{site_url}/sitemap.xml'
        ping_url = f'https://www.google.com/ping?sitemap={sitemap_url}'
        
        self.stdout.write(f'Submitting sitemap: {sitemap_url}')
        
        try:
            response = requests.get(ping_url)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS(
                    'Sitemap successfully submitted to Google'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Google returned status code: {response.status_code}'
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error submitting sitemap: {str(e)}'
            ))