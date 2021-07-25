from django.template.defaulttags import register

@register.filter
def get_next_url(request, next_url_number):
    '''
    фильр формирует URL для пагинации
    с целью сохранить выбранные фильтры
    '''
    a = request.GET.get("page")
    if len(request.GET) == 0 and request.GET.get("page") != None:
        return "?page="+str(next_url_number)

    url = "?"
    for get_request in request.GET:
        if get_request != "page":
            url += get_request + "="+request.GET.get(get_request) + "&"


    return url + "&page=" +str(next_url_number)
