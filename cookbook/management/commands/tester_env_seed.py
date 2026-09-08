from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django_scopes import scopes_disabled

from cookbook.models import Food, Household, Ingredient, Keyword, Recipe, RecipeBook, RecipeBookEntry, Space, Step, Unit, UserSpace


SPACE_NAME = 'Harbor Kitchen'
HOUSEHOLD_NAME = 'Harbor Kitchen Household'
BOOK_NAME = 'Weeknight Favorites'
RECIPES = (
    ('Lemon Herb Salmon', 'A bright sheet-pan supper with lemon, dill, and roasted potatoes.', 2, 35, '2024-01-15T18:00:00+00:00', 'Seafood', 'salmon'),
    ('Smoky Chickpea Stew', 'A hearty pantry stew with tomatoes, spinach, and smoked paprika.', 4, 40, '2024-02-12T18:00:00+00:00', 'Vegetarian', 'chickpeas'),
    ('Garden Vegetable Pasta', 'Weeknight pasta with zucchini, cherry tomatoes, and basil.', 4, 25, '2024-03-08T18:00:00+00:00', 'Weeknight', 'pasta'),
    ('Blueberry Oat Muffins', 'Make-ahead breakfast muffins with oats and blueberries.', 12, 30, '2024-04-20T09:00:00+00:00', 'Baking', 'blueberries'),
    ('Tomato Basil Soup', 'A simple blended soup finished with fresh basil.', 4, 45, '2024-05-05T12:00:00+00:00', 'Vegetarian', 'tomatoes'),
)


class Command(BaseCommand):
    help = 'Create the deterministic tester-env recipe baseline.'

    def handle(self, *args, **options):
        with scopes_disabled():
            user = get_user_model().objects.get(username='admin')
            for space in Space.objects.filter(name=SPACE_NAME):
                space.safe_delete()

            space = Space.objects.create(name=SPACE_NAME, created_by=user, space_setup_completed=True, household_setup_completed=True)
            household = Household.objects.create(name=HOUSEHOLD_NAME, space=space)
            UserSpace.objects.filter(user=user).update(active=False)
            membership = UserSpace.objects.create(user=user, space=space, household=household, active=True)
            membership.groups.add(Group.objects.get(name='admin'))

            unit = Unit.objects.create(name='cup', plural_name='cups', space=space)
            cookbook = RecipeBook.objects.create(name=BOOK_NAME, description='Reliable dinners for busy evenings.', created_by=user, space=space)
            recipes = []
            for index, (name, description, servings, working_time, created_at, tag, ingredient_name) in enumerate(RECIPES):
                keyword, _ = Keyword.objects.get_or_create(name=tag, space=space)
                food = Food.add_root(name=ingredient_name, plural_name=ingredient_name, space=space)
                ingredient = Ingredient.objects.create(food=food, unit=unit, amount=1, space=space)
                step = Step.objects.create(name='Prepare and cook', instruction='Prepare the ingredients, cook until tender, and serve warm.', order=1, time=working_time, space=space)
                step.ingredients.add(ingredient)
                recipe = Recipe.objects.create(name=name, description=description, servings=servings, working_time=working_time, created_by=user, space=space)
                recipe.keywords.add(keyword)
                recipe.steps.add(step)
                Recipe.objects.filter(pk=recipe.pk).update(created_at=datetime.fromisoformat(created_at), updated_at=datetime.fromisoformat(created_at))
                recipes.append(recipe)
                if index < 3:
                    RecipeBookEntry.objects.create(recipe=recipe, book=cookbook)

            self.stdout.write(self.style.SUCCESS(f'Seeded {space.name}: {len(recipes)} recipes, 3 cookbook entries, and {household.name}.'))
