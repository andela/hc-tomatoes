from django import forms
from django.forms import Textarea, ModelChoiceField, CharField
from django.contrib.auth.decorators import login_required
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render, render_to_response, reverse)
from django.template import RequestContext
from django.template.defaultfilters import slugify

from hc.blog.models import Category, Comment, Post


class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.title)


class NewPostForm(forms.ModelForm):
    """
    Model Form for creating a new post.
    """
    class Meta:
        model = Post
        fields = ['title', 'body', 'category']
        widgets = {
            'body' : Textarea(attrs={'cols': 150, 'rows': 20}),
            'title' : Textarea(attrs={'cols':75, 'rows':1})
        }
    category = CategoryChoiceField(
        empty_label="Choose a Category", queryset=Category.objects.all())


class CategoryForm(forms.ModelForm):
    """
    Model form for adding a category
    """
    class Meta:
        model = Category
        fields = ['title']


class CommentForm(forms.ModelForm):
    """
    Model form for commenting on a blog Post
    """
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'cols': 150, 'rows': 4}),
        }

# VIEWS


@login_required
def index(request):
    form = CategoryForm()
    if form.is_valid():
        new_cat = Category()
        new_cat.title = form.cleaned_data['title']
        new_cat.slug = slugify(form.cleaned_data['title'])
        new_cat.save()
        return redirect(reverse('home'))
    return render(request, 'blog/index.html', {
        'categories': Category.objects.all(),
        'posts': Post.objects.all(),
        'form': form
    })


@login_required
def view_post(request, slug):
    form = CommentForm(request.POST)
    blog_post = get_object_or_404(Post, slug=slug)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = blog_post
        comment.author = request.user
        comment.save()
        return HttpResponseRedirect(request.path_info)
    return render(request, 'blog/view_post.html', {
        'post': blog_post,
        'form': form
    })


@login_required
def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'blog/view_category.html', {
        'category': category,
        'posts': Post.objects.filter(category=category)
    })


@login_required
def create_post(request):
    form = NewPostForm(request.POST)
    if form.is_valid():
        new_post = Post()
        new_post.title = form.cleaned_data['title']
        new_post.body = form.cleaned_data['body']
        new_post.author = request.user
        new_post.slug = slugify(form.cleaned_data['title'])
        new_post.category = form.cleaned_data['category']

        new_post.save()
        return redirect(reverse('home'))
    return render(request, 'blog/create_post.html', {
        'form': form})
