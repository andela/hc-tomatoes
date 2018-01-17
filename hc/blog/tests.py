from django.test import TestCase, Client
from hc.blog.models import Post, Category, Comment
from django.template.defaultfilters import slugify
from django.shortcuts import reverse
from hc.accounts.models import Member, Profile
from django.contrib.auth.models import User
from hc.accounts.views import login


class BlogTest(TestCase):
    def setUp(self):
        self.test_user = User(username="test_user", email="test@example.org")
        self.test_user.set_password("password")
        self.test_user.save()
        
        form = {"email": "test@example.org", "password": "password"}
        self.client.post(reverse('hc-login'), form)

        self.test_category = Category.objects.create(
            title='TestCategory',
            slug=slugify('TestCategory')
        )
        self.test_post = Post.objects.create(
            title='TestPost',
            slug=slugify('TestPost'),
            body='This is a test post.',
            category=self.test_category,
            author=self.test_user
        )

    def test_index_returns_all(self):
        response = self.client.get(reverse('home'))
        form = {'title':'Test-Category-Two'}
        response_one = self.client.post(reverse('home'), form)
        self.assertEqual(response_one.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
    
    def test_view_post(self):
        response = self.client.get(reverse('view_blog_post', kwargs={'slug':self.test_post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/view_post.html')
        response_one = self.client.post(reverse('view_blog_post', kwargs={'slug':self.test_post.slug}))
        self.assertEqual(response_one.status_code, 200)
        
    def test_view_category(self):
        response = self.client.get(reverse('view_blog_category', kwargs={'slug':self.test_category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/view_category.html')
        
    def test_create_post(self):
        response = self.client.get(reverse('create_blog_post'))        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/create_post.html')
        form = {
            'title':'Test Post Two',
            'body':'This is another test post.',
            'author':self.test_user,
            'slug':slugify('Test Post Two'),
            'category':self.test_category
        }
        response_one = self.client.post(reverse('create_blog_post'), form)
        self.assertEqual(response_one.status_code, 200)