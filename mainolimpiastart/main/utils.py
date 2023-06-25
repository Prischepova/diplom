

menu = [{'title': "Главная", 'url_name': 'index'},
        {'title': "Индив", 'url_name': 'indiv'},
        {'title': "Оплата", 'url_name': 'payment'},
        {'title': "Документы", 'url_name': 'documents'},
        {'title': "Посещаемость", 'url_name': 'attendance'},
        {'title': "Уведомления", 'url_name': 'notifications'}
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context


