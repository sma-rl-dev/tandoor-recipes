from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django_scopes import scopes_disabled

from cookbook.management.commands.tester_env_seed import BOOK_NAME, HOUSEHOLD_NAME, RECIPES, SPACE_NAME
from cookbook.models import Household, Recipe, RecipeBook, RecipeBookEntry, Space, UserSpace


class Command(BaseCommand):
    help = 'Verify the deterministic tester-env recipe baseline.'

    def handle(self, *args, **options):
        with scopes_disabled():
            user = get_user_model().objects.filter(username='admin').first()
            space = Space.objects.filter(name=SPACE_NAME).first()
            if not user or not space or not Household.objects.filter(name=HOUSEHOLD_NAME, space=space).exists():
                raise CommandError('Missing Harbor Kitchen household baseline.')
            if not UserSpace.objects.filter(user=user, space=space, active=True).exists():
                raise CommandError('admin is not active in Harbor Kitchen.')
            names = [recipe[0] for recipe in RECIPES]
            if list(Recipe.objects.filter(space=space).order_by('name').values_list('name', flat=True)) != sorted(names):
                raise CommandError('Recipe inventory does not match the deterministic baseline.')
            book = RecipeBook.objects.filter(name=BOOK_NAME, space=space).first()
            if not book or RecipeBookEntry.objects.filter(book=book).count() != 3:
                raise CommandError('Weeknight Favorites does not contain three recipes.')
            self.stdout.write(self.style.SUCCESS('Verified Harbor Kitchen: 5 recipes, 3 Weeknight Favorites entries, active admin household.'))
