from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Specialty(models.Model):
    code = models.CharField(max_length=30, default='frontend')
    title = models.CharField(max_length=100, default='Фронтенд')
    picture = models.ImageField(upload_to='MEDIA_SPECIALITY_IMAGE_DIR', default='60x60.png')

    class Meta:
        verbose_name = 'специальность'
        verbose_name_plural = 'специальности'

    def __str__(self) -> str:
        return f'{self.title}'


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='MEDIA_COMPANY_IMAGE_DIR', null=True, default='60x60.png')
    description = models.CharField(max_length=300)
    employee_count = models.TextField()

    class Meta:
        verbose_name = 'компания'
        verbose_name_plural = 'компании'

    def __str__(self) -> str:
        return f'{self.name}'


class Vacancy(models.Model):
    title = models.CharField(max_length=100, verbose_name='название вакансии')
    specialty = models.ForeignKey(Specialty, default=id(0), on_delete=models.CASCADE,
                                   related_name='speciality_vacancies')
    company = models.ForeignKey(Company, default=id(0), on_delete=models.CASCADE, related_name='company_vacancies')
    skills = models.TextField()
    description = models.CharField(max_length=300, verbose_name='описание вакансии')
    salary_min = models.IntegerField(verbose_name='зарплата от')
    salary_max = models.IntegerField(verbose_name='зарплата до')
    publish_date = models.DateField(verbose_name='дата публикации')

    class Meta:
        verbose_name = 'вакансия'
        verbose_name_plural = 'вакансии'

    def __str__(self) -> str:
        return f'{self.title} ({self.specialty})'


class Application(models.Model):
    written_username = models.CharField(max_length=100)
    written_phone = models.CharField(max_length=100)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="applications")

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __str__(self) -> str:
        return f'{self.written_username} - {self.vacancy}'


class Resume(models.Model):

    status_all = [
        ('stop_search', 'Не ищу работу'),
        ('active', 'Рассматриваю предложения'),
        ('search', 'Ищу работу'),
    ]

    grade_all = [
        ('intern', 'Стажер'),
        ('junior', 'Джуниор'),
        ('middle', 'Миддл'),
        ('senior', 'Синьор'),
        ('lead', 'Лид'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    status = models.CharField(max_length=100, null=True, choices=status_all)
    salary = models.IntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    grade = models.CharField(max_length=100, null=True, choices=grade_all)
    education = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    portfolio = models.CharField(max_length=100)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.OneToOneField(Company, null=True, on_delete=models.CASCADE, related_name="companies")
    resume = models.OneToOneField(Resume, null=True, on_delete=models.CASCADE, related_name="resumes")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class CompanyOwner(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    company = models.OneToOneField(Company, null=True, on_delete=models.CASCADE)


@receiver(post_save, sender=Company)
def create_company(sender, instance, created, **kwargs):
    if created:
        CompanyOwner.objects.create(company=instance)


@receiver(post_save, sender=Company)
def save_company(sender, instance, **kwargs):
    instance.companyowner.save()
