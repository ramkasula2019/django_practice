from django.core.management.base import BaseCommand, CommandError
from snippets.models import Snippet 

class Command(BaseCommand):
    help = 'Change Snippets Title'

    def add_arguments(self, parser):
        parser.add_argument('snippet_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for snippet_id in options['snippet_ids']:
            try:
                snippet = Snippet.objects.get(pk=snippet_id)
            except Snippet.DoesNotExist:
                raise CommandError('Snippet "%s" does not exist' % snippet_id)

            snippet.title = 'changed from mgmt command'
            snippet.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % snippet_id))