# -*- coding: utf-8 -*-
import json
from django.views.generic.base import TemplateView
from django.conf import settings
from server.forms import SubscriptionForm, SubscriptionFormWithNgModel
from django.http import HttpResponseBadRequest, HttpResponse


class NgFormValidationView(TemplateView):
    template_name = 'subscribe-form.html'
    form = SubscriptionForm(form_name='subscribe_form')

    def __init__(self, **kwargs):
        super(NgFormValidationView, self).__init__(**kwargs)
        self.form.fields['height'].widget.attrs['step'] = 0.05  # Ugly hack to set step size

    def get_context_data(self, **kwargs):
        context = super(NgFormValidationView, self).get_context_data(**kwargs)
        context.update(form=self.form, with_ws4redis=hasattr(settings, 'WEBSOCKET_URL'))
        return context


class NgFormValidationViewWithNgModel(NgFormValidationView):
    template_name = 'subscribe-form-with-model.html'
    form = SubscriptionFormWithNgModel(scope_prefix='subscribe_data')

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest('Expected an XMLHttpRequest')

        in_data = json.loads(request.body)
        bound_contact_form = SubscriptionFormWithNgModel(data=in_data)
        # now validate ‘bound_contact_form’ and use it as in normal Django
        # bound_contact_form is always invalid
        import pdb;pdb.set_trace();
        return HttpResponse(json.dumps({}), content_type="application/json")

class Ng3WayDataBindingView(NgFormValidationViewWithNgModel):
    template_name = 'three-way-data-binding.html'
