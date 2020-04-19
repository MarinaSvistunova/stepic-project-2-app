from django import forms
from django.forms import ModelForm

from .models import Application, Resume, Company, Vacancy


class VacancySubmit(ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']

        widgets = {
            "written_username": forms.TextInput(
                attrs={
                    'id': 'username',
                    "class": "form-control"
                }
            ),
            "written_phone": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "written_cover_letter": forms.Textarea(
                attrs={
                    "class": "form-control"
                }
            )
        }


class MyResume(ModelForm):
    class Meta:
        model = Resume
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id': 'userName'
                }
            ),
            'surname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id': 'userSurname'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'custom-select mr-sm-2',
                    'id': 'userReady'
                }
            ),
            'specialty': forms.Select(
                attrs={
                    'class': 'custom-select mr-sm-2',
                    'id': 'userSpecialization'
                }
            ),
            'salary': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'userPortfolio',
                    'placeholder': '120000'
                }
            ),
            'grade': forms.Select(
                attrs={
                    'class': 'custom-select mr-sm-2',
                    'id': 'userQualification',
                }
            ),
            'education': forms.Textarea(
                attrs={
                    'class': 'form-control text-uppercase',
                    'id': 'userEducation',
                    'rows': '4',
                    'style': 'color:#000;',
                    'placeholder': 'АСТРАХАНСКИЙ ГОСУДАРСТВЕННЫЙ ТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ ИНСТИТУТ РЫБНОГО ХОЗЯЙСТВА, БИОЛОГИИ И ПРИРОДОПОЛЬЗОВАНИЯ, БАКАЛАВР ГОЛОВАСТИКОВЕДЕНИЯ'
        }
            ),
            'experience': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'userExperience',
                    'rows': '4',
                    'style': 'color:#000;',
                    'placeholder': 'Астраханская государственная библиотека – администратор базы данных, системный'
                                   ' архитектор, 2018-2020' 
                                   'Астра - инжиниинг, системный интегратор – младший разработчик 2016– 2018 '
                }
            ),
            'portfolio': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'userPortfolio',
                    'placeholder': 'http://anylink.github.io'
                }
            )
        }


class MyCompany(ModelForm):
    class Meta:
        model = Company
        logo = forms.FileField(label=None, required=False, widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'companyName'
                }
            ),
            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Санкт-Петербург',
                    'id': 'companyLocation'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '4',
                    'style': 'color:#000;',
                    'placeholder': 'Для тех, кто желает работать в комфортном офисе, - у нас их целых три. '
                                   'Исторически так сложилось, что руководство и менеджерский состав располагается в'
                                   'Москве (обусловлено близостью заказчиков), центр разработки в Ульяновске, '
                                   'в т.ч. школа молодых разработчиков и QA-центр в Казани.',
                    'id': 'companyInfo'
                }
            ),
            'employee_count': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '10',
                    'id': 'companyTeam'
                }
            )
        }

class MyVacancy(ModelForm):
    class Meta:
        model = Vacancy
        fields = '__all__'
        exclude = ['company', 'publish_date']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'vacancyTitle',
                    'placeholder': 'Мидл программист на Python'
                }
            ),
            'skills': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'vacancySkills',
                    'rows': '3',
                    'style': 'color:#000;',
                    'placeholder': 'Бэкенд, Средний (Middle), PHP, PostgreSQL, MySQL, Node.js, Laravel, Symfony, '
                                   'Yii framework, Sails.js, Rabbitmq, Kafka'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'vacancyDescription',
                    'rows': '13',
                    'style': 'color:#000;',
                    'placeholder': 'Финтех компания входит в международную группу  и занимается развитием '
                                   'факторингового бизнеса. В связи с расширением штата, мы хотим усилить нашу '
                                   'команду Backend-разработчиком, для работы над улучшением продуктов компании. \n'
                                   'Мы предлагаем: \n'
                                   'Оформление по ТК РФ \n'
                                   'ДМС со стоматологией \n'
                                   'Достойную зарплату, уровень которой можно обсудить по телефону с рекрутером \n'
                                   'Гибкое начало дня, отдельные дни удаленной работы обсуждаются \n'
                                   'Современный офис \n'
                                   'Демократичную корпоративную культуру\n'
                                   'Работу в команде по Scrum'
                }
            ),
            'salary_min': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'vacancySalaryMin',
                    'placeholder': '90000'
                }
            ),
            'salary_max': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'vacancySalaryMax',
                    'placeholder': '120000'
                }
            ),
            'specialty': forms.Select(
                attrs={
                    'class': 'custom-select mr-sm-2',
                    'id': 'userSpecialization'
                }
            ),
        }