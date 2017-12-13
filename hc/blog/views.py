from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render, render_to_response, reverse)
from django.template import RequestContext
from django.template.defaultfilters import slugify

from hc.blog.models import Category, Comment, Post


class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.title)


class PostForm(forms.ModelForm):
    """
    Model Form for creating a new post.
    """
    class Meta:
        model = Post
        fields = ['title', 'body', 'category']
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
    form = CommentForm(request.POST)
    return render(request, 'blog/view_category.html', {
        'category': category,
        'posts': Post.objects.filter(category=category),
        'form': form
    })


@login_required
def create_post(request):
    form = PostForm(request.POST)
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
