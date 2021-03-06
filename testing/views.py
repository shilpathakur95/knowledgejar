from django.shortcuts import render
from django.shortcuts import render_to_response,RequestContext,get_object_or_404
from testing.forms import UserForm, UserProfileForm,PostForm,CourseForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from testing.models import Course,Posts,UserProfile
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.admin import User

# Create your views here.
def home(request):
    template = get_template("open.html")
    return HttpResponse(template.render())


def first(request):
    template = get_template("first.html")
    return HttpResponse(template.render())

# @method_decorator(login_required,name='dispatch')
# class coursecreateview(CreateView):
#     model = Course
#     fields = {"course_name"}
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super(coursecreateview, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse("list")

@method_decorator(login_required,name='dispatch')
class courseupdateview(UpdateView):
    model = Course
    fields = {"course_name", "created_on"}
    #template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse("list")

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        query = Course.objects.all().get(id=id)
        return query

@method_decorator(login_required,name='dispatch')
class coursedeleteview(DeleteView):
    model = Course
    fields = {"course_name", "created_on"}

    def get_success_url(self):
        return reverse_lazy("list")

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        query = Course.objects.all().get(id=id)
        return query

def list(request):
    q=Course.objects.filter(owner=request.user.id)
    template = get_template("style.html")
    if request.method == 'POST':
        course_form = CourseForm(data=request.POST)
        course_form.instance.owner=User.objects.get(id=request.user.id)
        course_form.save()
    else:
        course_form=CourseForm()
    return HttpResponse(template.render(context={'list': q,'course_form':course_form}, request=request))

def postlist(request,pk):
    q=Posts.objects.filter(courseid=pk)
    template = get_template("post.html")
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        post_form.instance.courseid = Course.objects.get(id=pk)
        post_form.save()
    else:
        post_form = PostForm()
    return HttpResponse(template.render(context={'list': q,'id':pk,'post_form':post_form}, request=request))


# @method_decorator(login_required,name='dispatch')
# class postcreateview(CreateView):
#     model=Posts
#     fields = {'title','content'}
#     def form_valid(self, form):
#         form.instance.courseid = Course.objects.get(id=self.kwargs.get('pk'))
#         return super(postcreateview, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse("posts", kwargs={'pk': self.kwargs.get('pk')})

@method_decorator(login_required,name='dispatch')
class postupdateview(UpdateView):
    model=Posts
    fields = {'title', 'content'}
    def get_success_url(self):
        return reverse("posts", kwargs={'pk': self.kwargs.get('id')})

@method_decorator(login_required,name='dispatch')
class postdeleteview(DeleteView):
    model = Posts
    fields = {'title', 'content'}

    def get_success_url(self):
        return reverse("posts", kwargs={'pk': self.kwargs.get('id')})


def allcourses(request):
    e=UserProfile.objects.get(pk=request.user.id)
    en=e.enrolled.all()
    q = Course.objects.exclude(id__in=[o.id for o in en]).exclude(owner=request.user.id)
    template = get_template("allcourses.html")
    return HttpResponse(template.render(context={'list': q,'enro':en}, request=request))

def enroll(request,pk):
    u1=UserProfile.objects.get(id=request.user.id)
    c1=Course.objects.get(id=pk)
    u1.enrolled.add(c1)
    e = UserProfile.objects.get(pk=request.user.id)
    en = e.enrolled.all()
    q = Course.objects.exclude(id__in=[o.id for o in en]).exclude(owner=request.user.id)
    template = get_template("allcourses.html")
    return HttpResponse(template.render(context={'list': q, 'enro': en}, request=request))

def unenroll(request,pk):
    u1 = UserProfile.objects.get(id=request.user.id)
    c1 = Course.objects.get(id=pk)
    u1.enrolled.remove(c1)
    e = UserProfile.objects.get(pk=request.user.id)
    en = e.enrolled.all()
    q = Course.objects.exclude(id__in=[o.id for o in en]).exclude(owner=request.user.id)
    template = get_template("allcourses.html")
    return HttpResponse(template.render(context={'list': q, 'enro': en}, request=request))

def postdetail(request,pk):
    q=Posts.objects.filter(courseid=pk)
    cour=Course.objects.get(id=pk)
    template = get_template("postdetails.html")
    return HttpResponse(template.render(context={'list': q,'c':cour}, request=request))


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            #if 'picture' in request.FILES:
                #profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
        'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                #response = HttpResponse("", status=302)
                #response['Location'] =('http://localhost:63342/App/templates/piazza.html')
                #return response
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Knowledge Jar account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('registration/login.html', {}, context)

def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')