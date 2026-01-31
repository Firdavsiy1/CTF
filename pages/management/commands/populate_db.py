import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from pages.models import Category, Challenge, Solve, Attempt
from mentors.models import LessonTemplate, LessonSettings

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')

        # Create Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'password')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created'))
        else:
            self.stdout.write('Superuser "admin" already exists')

        # Create Regular Users
        for i in range(5):
            username = f'user_{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password',
                    bio=f'This is the bio for {username}',
                    country=random.choice(['USA', 'Russia', 'Germany', 'China', 'France'])
                )
                self.stdout.write(self.style.SUCCESS(f'User "{username}" created'))
            else:
                self.stdout.write(f'User "{username}" already exists')

        # Create Categories and Challenges
        categories = ['Web', 'Crypto', 'Pwn', 'Reverse', 'Misc']
        for cat_name in categories:
            category, created = Category.objects.get_or_create(name=cat_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Category "{cat_name}" created'))
            else:
                self.stdout.write(f'Category "{cat_name}" already exists')

            # Create Challenges for this category
            for i in range(3):
                title = f'{cat_name} Challenge {i+1}'
                if not Challenge.objects.filter(title=title).exists():
                    points = random.choice([100, 200, 300, 400, 500])
                    difficulty = random.choice(['Easy', 'Medium', 'Hard', 'Insane'])
                    flag = f'FLAG{{{cat_name.lower()}_{i+1}_{random.randint(1000, 9999)}}}'
                    Challenge.objects.create(
                        title=title,
                        category=category,
                        description=f'This is a description for {title}. Find the flag!',
                        points=points,
                        difficulty=difficulty,
                        flag=flag,
                        author='Admin',
                        max_attempts=0,
                        is_active=True
                    )
                    self.stdout.write(self.style.SUCCESS(f'Challenge "{title}" created'))
                else:
                    self.stdout.write(f'Challenge "{title}" already exists')

        # Create LessonTemplate
        template_title = "First Lesson"
        template, created = LessonTemplate.objects.get_or_create(title=template_title)
        if created:
            self.stdout.write(self.style.SUCCESS(f'LessonTemplate "{template_title}" created'))
            # Add random challenges to template
            challenges = list(Challenge.objects.all())
            if challenges:
                selected_challenges = random.sample(challenges, min(5, len(challenges)))
                template.challenges.set(selected_challenges)
                self.stdout.write(f'Added {len(selected_challenges)} challenges to "{template_title}"')
        else:
            self.stdout.write(f'LessonTemplate "{template_title}" already exists')

        # Create LessonSettings
        settings_obj = LessonSettings.get_settings()
        now = timezone.now()
        settings_obj.start_time = now
        settings_obj.end_time = now + timezone.timedelta(days=7)
        settings_obj.save()
        self.stdout.write(self.style.SUCCESS('LessonSettings updated'))

        # Create Solves and Attempts
        users = User.objects.exclude(is_superuser=True)
        challenges = Challenge.objects.all()

        if users.exists() and challenges.exists():
            for user in users:
                # Create attempts
                for _ in range(random.randint(1, 5)):
                    challenge = random.choice(challenges)
                    is_correct = random.choice([True, False])
                    flag_input = challenge.flag if is_correct else "WRONG_FLAG"

                    Attempt.objects.create(
                        user=user,
                        challenge=challenge,
                        flag_input=flag_input,
                        is_correct=is_correct
                    )

                    if is_correct:
                        # Create solve if correct and not already solved
                        Solve.objects.get_or_create(user=user, challenge=challenge)

            self.stdout.write(self.style.SUCCESS('Solves and Attempts generated'))
