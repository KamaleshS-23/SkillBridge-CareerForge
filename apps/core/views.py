from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def dashboard(request):

    certifications = request.user.certifications.all()
    recommended = []

    if request.user.field_of_interest == 'data_science':
        recommended = [
            {'name': 'Data Science with Python', 'org': 'Infosys'},
            {'name': 'Machine Learning Basics', 'org': 'AICTE'},
        ]
    elif request.user.field_of_interest == 'web_dev':
        recommended = [
            {'name': 'Full Stack Web Development', 'org': 'Internshala'},
            {'name': 'Frontend Development', 'org': 'Edunet'},
        ]
    elif request.user.field_of_interest == 'ai_ml':
        recommended = [
            {'name': 'Artificial Intelligence', 'org': 'Infosys'},
            {'name': 'Deep Learning', 'org': 'AICTE'},
        ]

    context = {
        'certifications': certifications,
        'recommended': recommended,
    }

    return render(request, 'core/dashboard.html', context)