from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField

# Create your models here.
class Profile(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    user = models.OneToOneField(User, related_name = 'profile', on_delete=models.CASCADE)
    email = models.EmailField(max_length=150)
    alias = models.CharField('author Alias', max_length=100)
    contribution = models.IntegerField('author Contribution', default=0)
    status = models.BooleanField('Active author?', default=True)
    birthday = models.DateField("author's B-day", blank=True, null=True)
    creation_date = models.DateField('author Creation Date', auto_now_add=True, auto_now = False)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def __str__(self):
        return self.alias

    def save(self, *args, **kwargs):
        self.slug = slugify(self.alias)
        super(Profile, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, id=instance.id, email=instance.email, alias=instance.username)
    instance.profile.save()

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField('Category name', max_length=100, unique=True)
    image = models.URLField('Type image', max_length=255)
    slug = models.SlugField()
    status = models.BooleanField('Active Category?', default=True)
    creation_date = models.DateField('Category Creation Date', auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Tag', max_length=100, unique=True)
    image = models.URLField('Type image', max_length=300)
    slug = models.SlugField()
    status = models.BooleanField('Active Tag?', default=True)
    creation_date = models.DateField('Tag creation Date', auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name='Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

class Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Type', max_length=100, unique=True)
    image = models.URLField('Type image', max_length=300)
    slug = models.SlugField()
    status = models.BooleanField('Active Type?',default=True)
    creation_date = models.DateField('Type creation date', auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Type,self).save(*args, **kwargs)

class Suggestion(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('Suggestion Title', max_length=100, unique=True)
    slug = models.SlugField(default='asd')
    image = models.URLField('Suggestion Image', max_length=300)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, related_name='tag')
    status = models.BooleanField(default=True)
    creation_date = models.DateField('Suggestion creation date', auto_now_add=True, auto_now=False)
    ranking = models.IntegerField('Suggestion Views Ranking', default=0)
    votes = models.IntegerField('Suggestion Votes Ranking', default=0)

    class Meta:
        verbose_name = 'Suggestion'
        verbose_name_plural = 'Suggestions'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Suggestion, self).save(*args,**kwargs)


