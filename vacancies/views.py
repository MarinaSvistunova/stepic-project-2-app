import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, DetailView

from .forms import VacancySubmit, MyResume, MyCompany, MyVacancy
from .models import Vacancy, Specialty, Company, Application, Resume, CompanyOwner


class MainView(View):
    def get(self, request):
        context = {}

        specialties = Specialty.objects.all()
        specialties_count = Vacancy.objects.values('specialty_id').annotate(count=Count('specialty'))

        context['specialties'] = {}

        for specialty in specialties:
            specialty_count_for = specialties_count.filter(specialty_id=specialty.id)
            if specialty_count_for.exists():
                count = specialty_count_for[0].get('count')
            else:
                count = 0
            context['specialties'][specialty.code] = {'title': specialty.title,
                                                      'img': specialty.picture,
                                                      'count': count}

        companies = Company.objects.all()
        companies_count = Vacancy.objects.values('company_id').annotate( count=Count('company'))

        context['companies'] = {}

        for company in companies:
            companies_count_for = companies_count.filter(company_id=company.id)
            if companies_count_for.exists():
                count = companies_count_for[0].get('count')
            else:
                count = 0
            context['companies'][company.id] = {'name': company.name,
                                                'img': company.logo,
                                                'count': count}
        return render(request, 'vacancies/index.html', context)


class VacanciesView(View):
    def get(self, request):
        context = {}

        vacancies = Vacancy.objects.all()

        for vacancy in vacancies:
            vacancy.skills = vacancy.skills.split(',')

        context['vacancies'] = vacancies
        context['count'] = len(vacancies)

        return render(request, 'vacancies/vacancies_list.html', context)


class JobsView(DetailView):
    def get(self, request, id):

        context = {}

        vacancy = Vacancy.objects.filter( id=id ).first()

        context['vacancy'] = vacancy

        context['skills'] = vacancy.skills.split( ',' )

        context['vacancy_form'] = VacancySubmit()

        return render(request, 'vacancies/vacancy.html', context)

    def post(self, request):
        form_class = VacancySubmit(request.POST)
        data = form_class.cleaned_data
        return render(request, 'vacancies/vacancy.html', {'form':  form_class})


def send_application(request, id):
    form = VacancySubmit(request.POST)
    vacancy = Vacancy.objects.filter( id=id ).first()
    user = User.objects.filter(id=request.user.id).first() if request.user else None
    print(request.user.id)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = user
        instance.vacancy = vacancy
        instance.save()
    else:
        print(form.errors)
    return render(request, 'vacancies/sent.html', {'form': form})


class JobsCategoryView(View):
    def get(self, request, category):
        context = {}

        specialty = Specialty.objects.get(code=category)
        vacancies = Vacancy.objects.filter(specialty=specialty.id)
        context['title'] = specialty.title
        context['count'] = len(vacancies)
        context['vacancies'] = vacancies

        for vacancy in context['vacancies']:
            vacancy.skills = vacancy.skills.split(',')

        return render(request, 'vacancies/list.html', context)


class CompanyJobView(View):
    def get(self, request, id):
        context = {}

        company = Company.objects.filter(id=id).first()
        context['company'] = company

        vacancies = Vacancy.objects.filter(company=id)
        context['count'] = len(vacancies)
        context['vacancies'] = vacancies

        for vacancy in context['vacancies']:
            vacancy.skills = vacancy.skills.split(',')

        return render(request, 'vacancies/company.html', context)


class MyResumeView(View):
    form_class = MyResume
    template_name = 'vacancies/account/resume-edit.html'

    def get(self, request):
        context = {'update': 'd-none'}
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            user_has_resume = Resume.objects.filter(user=user)
            if len(user_has_resume) == 0:
                return render(request, 'vacancies/account/resume-create.html', context)
            else:
                user_resume = user_has_resume.first()
                form = self.form_class(instance=user_resume)
                context['form'] = form
                return render(request, self.template_name, context)
        else:
            return redirect('login_view')

    def post(self, request):
        context = {'update': 'd-none'}
        user = User.objects.get(id=request.user.id)
        user_name = user.first_name
        user_surname = user.last_name
        initial_data = {'user': user, 'name': user_name, 'surname': user_surname}
        user_has_resume = Resume.objects.filter(user=user)
        if len(user_has_resume) == 0:
            form = self.form_class(request.POST, initial_data)
            if form.is_valid():
                instance = form.save(commit=False )
                instance.user = user
                instance.save()
            else:
                print(form.errors)
            context['form'] = form
            context['update'] = ''
            return render(request, self.template_name, context)
        else:
            user_has_resume = user_has_resume.first()
            form = self.form_class(request.POST, instance=user_has_resume)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()
            else:
                print(form.errors)
            context['form'] = form
            context['update'] = ''
            return render(request, self.template_name, context)


class MyCompanyView(View):
    form_class = MyCompany
    template_name = 'vacancies/account/company-edit.html'

    def get(self, request):
        context = {'update': 'd-none'}
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            user_has_company = CompanyOwner.objects.filter(user=user)
            if len(user_has_company) == 0:
                return render(request, 'vacancies/account/company-create.html', context)
            else:
                user_company = user_has_company.first().company
                form = self.form_class(instance=user_company)
                context['form'] = form
                return render(request, self.template_name, context)
        else:
            return redirect('login_view')

    def post(self, request):
        context = {'update': 'd-none'}
        user = User.objects.get(id=request.user.id)
        initial_data = {}
        user_has_company = CompanyOwner.objects.filter(user=user)
        if len(user_has_company) == 0:
            form = self.form_class(request.POST, request.FILES, initial_data)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()

                company_owner = CompanyOwner.objects.get(company=instance)
                company_owner.user = user
                company_owner.save()

                return redirect('my_company_view')
            else:
                print(form.errors)
            context['form'] = form
            context['update'] = ''

            return render(request, self.template_name, context)
        else:
            user_company = user_has_company.first().company
            form = self.form_class(request.POST, request.FILES, instance=user_company)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()
            else:
                print(form.errors)
            context['form'] = form
            context['update'] = ''
            return render(request, self.template_name, context)


class MyCompanyVacanciesView(View):
    template_name = 'vacancies/account/vacancy-list.html'
    def get(self, request):
        if request.user.is_authenticated:
            context = {}
            user = User.objects.get(id=request.user.id)
            company_set = CompanyOwner.objects.filter(user=user)
            if len(company_set) == 0:
                return render(request, self.template_name, context)
            else:
                company = company_set.first().company
                vacancies = Vacancy.objects.filter(company=company)
                context['vacancies'] = {}
                for vacancy in vacancies:
                    applications_count = len(vacancy.applications.all())
                    context['vacancies'][vacancy.id] = {
                        'title': vacancy.title,
                        'salary_min': vacancy.salary_min,
                        'count': applications_count
                    }
                return render(request, self.template_name, context)
        else:
            return redirect('login_view')


class MyCompanyVacancy(View):
    form_class = MyVacancy
    template_name = 'vacancies/account/vacancy-edit.html'

    def get(self, request, id):
        context = {'update': 'd-none'}
        if request.user.is_authenticated:
            vacancy = Vacancy.objects.get(id=id)
            form = self.form_class(instance=vacancy)
            context['form'] = form
            applications = Application.objects.filter(vacancy=vacancy)
            context['applications'] = applications
            context['count'] = len(applications)
            return render(request, self.template_name, context)
        else:
            return redirect('login_view')

    def post(self, request, id):
        context = {'update': 'd-none'}
        if id == 0:
            form = self.form_class()
            context['form'] = form
            context['update'] = ''
            form = self.form_class(request.POST)
            user = request.user
            company = CompanyOwner.objects.get(user=user).company
            if form.is_valid():
                instance = form.save(commit=False)
                instance.company = company
                instance.publish_date = datetime.date.today()
                instance.save()
                return redirect('my_company_vacancies_view')
            else:
                print(form.errors)
            context['form'] = form
            return render(request, self.template_name, context)
        else:
            vacancy = Vacancy.objects.get(id=id)
            form = self.form_class(request.POST, instance=vacancy)
            company = Vacancy.objects.get(id=id).company
            applications = Application.objects.filter(vacancy=vacancy)
            context['applications'] = applications
            context['count'] = len(applications)
            context['update'] = ''
            if form.is_valid():
                instance = form.save(commit=False)
                instance.company = company
                instance.save()
            else:
                print(form.errors)
            context['form'] = form
            return render(request, self.template_name, context)


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'vacancies/register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'vacancies/login.html'

