from typing import Any
from django.core.management.commands import startapp
from operator import itemgetter

class Command(startapp.Command):

    def handle(self, *args: Any, **options: Any) -> str | None:
        template = itemgetter('template')
        template = template(options) or '.app_template'
        options.update(template = template)
         
        return super().handle(*args, **options)
    