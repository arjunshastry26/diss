import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forum_project.settings')
django.setup()

from django.contrib.auth.models import User
from forum.models import Category, Discussion, Comment, UserProfile

cats = ['Python', 'Django', 'Databases', 'Frontend', 'DevOps', 'General']
for c in cats:
    Category.objects.get_or_create(name=c, defaults={'description': f'Discussions about {c}'})

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')

demo_user, created = User.objects.get_or_create(username='demo', defaults={'email': 'demo@example.com'})
if created:
    demo_user.set_password('demo12345')
    demo_user.save()
UserProfile.objects.get_or_create(user=demo_user, defaults={'bio': 'Just here to help solve problems.'})

if not Discussion.objects.exists():
    d = Discussion.objects.create(
        title='How do I fix "CSRF verification failed" in Django?',
        body='I keep getting a CSRF error when submitting my form. I have {% csrf_token %} in my template already. What else could be wrong?',
        category=Category.objects.get(name='Django'),
        author=demo_user,
    )
    Comment.objects.create(discussion=d, author=demo_user, body='Check that your form uses method="post" and that CSRF middleware is enabled in settings.py.')

print('Seed complete.')
