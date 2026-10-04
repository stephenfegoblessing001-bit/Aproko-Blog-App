from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime as dt
from .models import Blog, Category, Profile, Like, Comment
from .forms import BlogForm, CategoryForm, ProfileForm, UserForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

blogs = [
        {
            "id": 1,
            "title": "Nigeria Decides",
            "slug": "nigeria-decides",
            "author": "Damilare Arise",
            "category": "Politics",
            "excerpt": "A look at the key issues shaping Nigeria's electoral landscape and what citizens should expect.",
            "content": "Nigeria's elections continue to influence the nation's future, with debates around governance, youth participation, and electoral reforms taking center stage.",
            "image": "blog/nigeria-decides.jpg",
            "is_published": True,
            "views": 2543,
            "created_at": dt.strptime("2026-08-10", "%Y-%m-%d"),
        },
        {
            "id": 2,
            "title": "Osun State Election 2026",
            "slug": "osun-state-election-2026",
            "author": "Damilare Arise",
            "category": "Politics",
            "excerpt": "An overview of the major candidates, campaign promises, and the issues driving the 2026 Osun election.",
            "content": "The Osun State election has generated significant public interest, with voters paying close attention to education, infrastructure, and economic development.",
            "image": "blog/osun-election-2026.jpg",
            "is_published": True,
            "views": 1876,
            "created_at": dt.strptime("2026-08-12", "%Y-%m-%d"),
        },
        {
            "id": 3,
            "title": "How to Make Money in Tech",
            "slug": "how-to-make-money-in-tech",
            "author": "Damilare Arise",
            "category": "Technology",
            "excerpt": "Practical ways beginners and professionals can earn income through software development, data science, and freelancing.",
            "content": "The tech industry offers multiple income streams, including remote jobs, freelancing, SaaS products, content creation, and teaching technical skills.",
            "image": "blog/make-money-tech.jpg",
            "is_published": False,
            "views": 932,
            "created_at": dt.strptime("2026-08-13", "%Y-%m-%d"),
        },
    ]



def homeView(request):
    username = 'Tolulope'
    # model_blogs = Blog.objects.all().order_by("-created_at")
    # model_blogs = Blog.objects.all().order_by("?")[:3]
    model_blogs = Blog.objects.filter(is_published=True).order_by("?")[:3]
    # blog = Blog.objects.get(id=20)
    # blog = get_object_or_404(Blog, id=20)
    # print(model_blogs)
    
    return render(
        request, 
        template_name="index.html", 
        context={
           "username": username,
           "blogs":model_blogs
        
        }
    )

def AboutView(request):
    return render(request, template_name="about.html")


def blogView(request):
    
    # print(request.GET.get("category"))
    
    
    blogs = Blog.objects.filter(is_published=True).order_by("-created_at")
    categories = Category.objects.all()
    
    category_id = request.GET.get("category")
    if category_id:
        blogs = blogs.filter(category_id=category_id)
    
    return render(
        request,
        template_name="blogs.html",
        context={
            "blogs": blogs,
            "categories": categories
        }
    )

def addCategory(request):

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully")
            return redirect("blogs")

    else:
        form = CategoryForm()

    return render(
        request,
        template_name="categoryform.html",
        context={
            "form": form
        }
    )


def singleBlogView(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    if not blog.is_published:
        if not request.user.is_authenticated:
            messages.error(
                request,
                "This blog post has not been published."
            )
            return redirect("blogs")

        if not request.user.is_superuser and blog.author != request.user:
            messages.error(
                request,
                "This blog post has not been published."
            )
            return redirect("blogs")

    blog.clicks += 1
    blog.save()

    user_liked = False

    if request.user.is_authenticated:
        user_liked = blog.likes.filter(
            user=request.user
        ).exists()
    comments = blog.comments.all().order_by("-created_at")
    comment_form = CommentForm()

    return render(
    request,
    template_name="single_blog.html",
    context={
        "blog": blog,
        "user_liked": user_liked,
        "comments": comments,
        "comment_form": comment_form,
    }
)

@login_required
def createBlog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()

            messages.success(request, "Blog created successfully")
            return redirect("blogs")

        messages.error(request, "Please correct the errors below.")

    else:
        form = BlogForm()

    return render(
        request,
        template_name="blogform.html",
        context={"form": form}
    )
        
        
@login_required
def editBlog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    if not request.user.is_superuser and blog.author != request.user:
        messages.error(
            request,
            "You don't have permission to perform this operation."
        )
        return redirect("blogs")

    if request.method == "POST":
        form = BlogForm(
            request.POST,
            request.FILES,
            instance=blog
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Blog edited successfully")
            return redirect("single-blog", slug=blog.slug)

        messages.error(request, "Please correct the errors below.")

    else:
        form = BlogForm(instance=blog)

    return render(
        request,
        template_name="blogform.html",
        context={"form": form}
    )
        

@login_required
def deleteBlog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    if not request.user.is_superuser and blog.author != request.user:
        messages.error(
            request,
            "You don't have permission to perform this operation."
        )
        return redirect("blogs")

    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted successfully")
        return redirect("blogs")

    return redirect("single-blog", slug=blog.slug)


@login_required
def likeBlog(request, slug):
    if request.method == "POST":
        blog = get_object_or_404(
            Blog,
            slug=slug,
            is_published=True
        )

        like, created = Like.objects.get_or_create(
            user=request.user,
            blog=blog
        )

        if not created:
            like.delete()

    return redirect("single-blog", slug=slug)



@login_required
def addComment(request, slug):
    blog = get_object_or_404(
        Blog,
        slug=slug,
        is_published=True
    )

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()

            messages.success(request, "Comment added successfully.")
        else:
            messages.error(request, "Please enter a valid comment.")

    return redirect("single-blog", slug=slug)


@login_required
def deleteComment(request, comment_id):
    comment = get_object_or_404(
        Comment,
        id=comment_id,
        user=request.user
    )

    if request.method == "POST":
        blog_slug = comment.blog.slug
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect("single-blog", slug=blog_slug)

    return redirect("single-blog", slug=comment.blog.slug)


@login_required
def profileView(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "profile.html",
        context={
            "profile": profile
        }
    )

@login_required
def editProfileView(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        "edit_profile.html",
        context={
            "user_form": user_form,
            "profile_form": profile_form
        }
    )


