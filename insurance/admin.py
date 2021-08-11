from django.contrib import admin
from django.db.models import QuerySet

from .models import Services,Type_services, Insurance_companies, Request_for_a_call, CommentService
from project.settings import collection_mongoDB_statistics_serivice
admin.site.register(Type_services)


class InsuranceСompaniesAdmin(admin.ModelAdmin):
    fields = ('name', 'expert_rating','image','customer_base','general_refusal','date_of_creation', )
    list_display = ('name','date_of_creation' )

    def get_queryset(self, request):
        '''
        функция огарничивает просмотр списка компаний
        пользователь видит только те компании, которые создал сам
        '''
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(autor=request.user)

    def save_model(self, request, obj, form, change):
        '''
        при сохраении компании функиция добавлет в качества автора
        авторизованного пользователя
        '''
        obj.autor = request.user
        obj.autor_id = request.user.id
        super(InsuranceСompaniesAdmin, self).save_model(request, obj, form, change)


class RequestForACallAdmin(admin.ModelAdmin):
    ordering = ('-data_time',)
    list_display = ('name', 'services', 'phone_number','comment','data_time' )

    def get_queryset(self, request):
        '''
        Функция показывает запросы только к тем сервисам,который
        пользователь создал сам
        '''
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        queryset_one_user_service = qs.filter(id = 0)
        #ищет только те завки которые принадлежат пользователю
        for a in qs.all():
            b = a.services.insurance_companies.autor
            if a.services.insurance_companies.autor == request.user:
                queryset_one_user_service = queryset_one_user_service | qs.filter(id = a.id)
        return queryset_one_user_service
    def get_queryset(self, request):
        '''
        функция огарничивает просмотр списка компаний
        пользователь видит только те компании, которые создал сам
        '''
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(autor=request.user)

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_services','number_of_views',)
    def number_of_views(self, obj):
        '''
        создём ещё одно поле для отопбражения
        количестов просмотров
        '''
        request = collection_mongoDB_statistics_serivice.find_one({"id":obj.id})
        return  (request.get('count') if request != None else 0)

    number_of_views.short_description = 'Всего количество просмотров'


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        '''
        функция ограничивает выбор компаниий создания сервиса
        пользовтаель видит только список свои компаний
        '''
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "insurance_companies":
            kwargs["queryset"] = Insurance_companies.objects.filter(autor=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        '''
        ищет только те услуги которые принадлежат пользователю
        '''
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        queryset_one_user_service = qs.filter(id = 0)
        for a in qs.all():
            if a.insurance_companies.autor == request.user:
                queryset_one_user_service = queryset_one_user_service | qs.filter(id = a.id)
        return queryset_one_user_service


class CommentServiceAdmin(admin.ModelAdmin):
    list_display = ('services','name','email','comment', 'date_of_creation')

    def get_queryset(self, request):
        '''
            функция ограничивает прсотмотр комментарием
            руководить компании могут лишь просматривать те комментарии, которые
            оставили к их сервисам
        '''
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        result_request = qs.none()
        for one_comment in qs.all():
            if one_comment.services.insurance_companies.autor == request.user:
                result_request = result_request | qs.filter(id=one_comment.id)

        return result_request


admin.site.register(Services, ServicesAdmin)
admin.site.register(Request_for_a_call,RequestForACallAdmin)
admin.site.register(Insurance_companies, InsuranceСompaniesAdmin)
admin.site.register(CommentService,CommentServiceAdmin)