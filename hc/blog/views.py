from django.shortcuts import render_to_response, get_object_or_404, redirect, reverse, render
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django import forms
from hc.blog.models import Post, Category

# class CategoryChoiceField(forms.ModelChoiceField):
#      def label_from_instance(self, obj):
#          return "%s" % (obj.title)

#  class PostForm(forms.Form):
#      title = forms.CharField()
#      body = forms.CharField(widget=forms.Textarea, label='Body')
#      category  = CategoryChoiceField(empty_label="Choose a Category", queryset=Category.objects.all())

class PostForm(forms.ModelForm):
    """
    Model Form for creating a new post.
    """
    class Meta:
        model = Post
        fields = ['title', 'body', 'category']
## VIEWS

def index(request):
    return render(request, 'blog/index.html', {
        'categories': Category.objects.all(),
        'posts': Post.objects.all()
    })

def view_post(request, slug):
    return render(request, 'blog/view_post.html', {
        'post': get_object_or_404(Post, slug=slug)
    })


def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'blog/view_category.html', {
        'category': category,
        'posts': Post.objects.filter(category=category)
    })

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
        'form' : form})
