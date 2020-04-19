def variable_to_context(request):
    return {
        'menu_titles': {
            'Главная': 'main_view',
            'Вакансии': 'vacancies_view'
            # 'О проекте': 'main_view'
        },
        'dropdown_menu': {
            # 'Профиль': '',
            'Резюме': 'my_resume_view',
            'Компания': 'my_company_view',
            'Выйти': 'logout_view'
        },
        'searches': ['Python', 'Flask', 'Django', 'Парсинг', 'ML'],
        'register_form': {
            'username': 'Никнейм',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
            'password': 'Пароль'
        }
    }
