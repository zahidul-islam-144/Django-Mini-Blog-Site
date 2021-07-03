from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView
from App_Blog.models import Blog, Comment, like
from django.urls import reverse, reverse_lazy  
from django.contrib.auth.decorators import login_required # for function based view
from django.contrib.auth.mixins import LoginRequiredMixin # for class based view
from App_Blog.forms import CommentForm
import uuid


# Create your views here.

# def blog_list(request):
#     return render(request, 'App_Blog/blog_list.html')
      
class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog #creating a object under Blog model to create a new blog
    template_name = 'App_Blog/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image') # which fields i want to show 

    def form_valid(self, form): #this funciton will be called at the time of taking data 
        blog_obj = form.save(commit=False) # creating a object to store form data into a object and commit false holds data before saving into database cause it needs to indentify the user request
        blog_obj.author = self.request.user # setting request user
        title = blog_obj.blog_title # setting blog title which is created by the user
        blog_obj.slug = title.replace(" ","-") + "-" + (str(uuid.uuid4())) # when title is written, replace fn set hyphen removing white spaces and uuid4 fn sets unique id to find actual user if same blog title found
        blog_obj.save() # now form is saved 
        return HttpResponseRedirect(reverse('index')) # after saving the form it will take you index(home) page 

class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/blog_list.html'
    # queryset = Blog.objects.order_by('-publish_date')

class MyBlog(LoginRequiredMixin, TemplateView):
    model = Blog
    template_name = 'App_Blog/my_blog.html'

class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('blog_title', 'blog_content', 'blog_image')
    template_name = 'App_Blog/edit_blog.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('App_Blog:blog_details', kwargs={'slug':self.object.slug})

@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    already_liked = like.objects.filter(blog=blog, user=request.user)
    if already_liked:
        liked = True
    else:
        liked = False
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            Comment = comment_form.save(commit=False)
            Comment.user = request.user
            Comment.blog = blog
            Comment.save()
            return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':slug}))
    return render(request, 'App_Blog/blog_details.html', context={'blog':blog, 'comment_form':comment_form, 'liked':liked})

@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = like.objects.filter(blog=blog, user=user)
    if not already_liked:
        liked_post = like(blog=blog, user=user)
        liked_post.save()
        return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':blog.slug}))

@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = like.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':blog.slug}))


