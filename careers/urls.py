from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from vacancies.views import MainView, VacanciesView, JobsView, JobsCategoryView, CompanyJobView, \
    MyLoginView, MySignupView, send_application, MyResumeView, MyCompanyView, MyCompanyVacanciesView, MyCompanyVacancy

urlpatterns = [
    path('', MainView.as_view(), name='main_view'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies_view'),
    path('jobs/<int:id>/', JobsView.as_view(), name='jobs_view'),
    path('jobs/cat/<str:category>/', JobsCategoryView.as_view(), name='jobs_category_view'),
    path('jobs/<int:id>/send', send_application, name='send_application'),
    path('myresume/', MyResumeView.as_view(), name='my_resume_view'),
    path('myresume/create/', MyResumeView.as_view(), name='my_resume_create'),
    path('mycompany/', MyCompanyView.as_view(), name='my_company_view'),
    path('mycompany/create/', MyCompanyView.as_view(), name='my_company_create'),
    path('mycompany/vacancies', MyCompanyVacanciesView.as_view(), name='my_company_vacancies_view'),
    path('mycompany/vacancies/<int:id>/', MyCompanyVacancy.as_view(), name='my_company_vacancy_view'),
    path('companies/<int:id>/', CompanyJobView.as_view(), name='company_job_view'),
    path('login', MyLoginView.as_view(), name='login_view'),
    path('logout', LogoutView.as_view(), name='logout_view'),
    path('signup', MySignupView.as_view(), name='signup_view'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
