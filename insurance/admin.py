from django.contrib import admin
from django.db.models import QuerySet
from .form import *
from .models import *
# Register your models here.
#admin.site.register(Insurance_companies)

admin.site.register(Type_services)


class Insurance_companiesAdmin(admin.ModelAdmin):
    fields = ('name', 'expert_rating','image','customer_base','general_refusal','date_of_creation', )
    list_display = ('name','date_of_creation' )
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(autor=request.user)


    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        obj.autor_id = request.user.id
        super(Insurance_companiesAdmin, self).save_model(request, obj, form, change)

class Request_for_a_callAdmin(admin.ModelAdmin):
    ordering = ('-data_time',)
    list_display = ('name', 'services', 'phone_number','comment','data_time' )
    def get_queryset(self, request):
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

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_services',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "insurance_companies":
            kwargs["queryset"] = Insurance_companies.objects.filter(autor=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        queryset_one_user_service = qs.filter(id = 0)
        #ищет только те услуги которые принадлежат пользователю
        for a in qs.all():
            if a.insurance_companies.autor == request.user:
                queryset_one_user_service = queryset_one_user_service | qs.filter(id = a.id)
        return queryset_one_user_service


admin.site.register(Services, ServicesAdmin)
admin.site.register(Request_for_a_call,Request_for_a_callAdmin)

admin.site.register(Insurance_companies, Insurance_companiesAdmin)