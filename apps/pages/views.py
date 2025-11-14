from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class pagesview(LoginRequiredMixin,TemplateView):
    pass 

authentication_signin = pagesview.as_view(template_name = "pages/authentication/auth-signin.html")
authentication_signup = pagesview.as_view(template_name = "pages/authentication/auth-signup.html")
authentication_pass_reset = pagesview.as_view(template_name = "pages/authentication/auth-pass-reset.html")
authentication_change = pagesview.as_view(template_name = "pages/authentication/auth-pass-change.html")
authentication_lockscreen = pagesview.as_view(template_name = "pages/authentication/auth-lockscreen.html")
authentication_logout = pagesview.as_view(template_name = "pages/authentication/auth-logout.html")
authentication_success_msg = pagesview.as_view(template_name = "pages/authentication/auth-success-msg.html")
authentication_twostep_verification = pagesview.as_view(template_name = "pages/authentication/auth-twostep.html")

# errors
error_404 = pagesview.as_view(template_name = "pages/errors/auth-404.html")
error_500 = pagesview.as_view(template_name = "pages/errors/auth-500.html")
error_503 = pagesview.as_view(template_name = "pages/errors/auth-503.html")
error_offline = pagesview.as_view(template_name = "pages/errors/auth-offline.html")

# pages
pages_starter = pagesview.as_view(template_name = "pages/pages-starter.html")
pages_profile = pagesview.as_view(template_name = "pages/pages-profile.html")
pages_timeline= pagesview.as_view(template_name = "pages/pages-timeline.html")
pages_faqs= pagesview.as_view(template_name = "pages/pages-faqs.html")
pages_pricing= pagesview.as_view(template_name = "pages/pages-pricing.html")
pages_maintenance= pagesview.as_view(template_name = "pages/pages-maintenance.html")
pages_coming_soon= pagesview.as_view(template_name = "pages/pages-coming-soon.html")
pages_privacy_policy= pagesview.as_view(template_name = "pages/pages-privacy-policy.html")
pages_term_conditions= pagesview.as_view(template_name = "pages/pages-term-conditions.html")
pages_web_apps = pagesview.as_view(template_name = "pages/pages-web-apps.html")

