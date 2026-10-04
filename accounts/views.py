from django.shortcuts import render, redirect
from .forms import Signupform
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 

# Create your views here.

def signup_view(request):

    if request.method == "POST":
        form = Signupform(request.POST)

        if form.is_valid():
            form.save()

            send_mail(
                subject="Registration Successful",
                message="You've successfully created an account on "
                        "Aproko blog.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.cleaned_data.get("email")],
                fail_silently=True
            )

            messages.success(request, "Registration successful")
            return redirect("login")

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = Signupform()

    return render(
        request,
        template_name="registration/signup.html",
        context={
            "form": form
        }
    )