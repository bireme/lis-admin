from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.utils import ErrorList
from utils.forms import is_valid_for_publication


def check_url_or_attachment(form, formset_attachment):
    """
    Check if is present the electronic_address field or attachment and run LILACS validation
    across pages, electronic_address, record_type and descriptive_information atribute_a
    """
    url_or_attachment = True

    pages = form.cleaned_data.get('pages')
    electronic_address = form.cleaned_data.get('electronic_address')
    record_type = form.cleaned_data.get('record_type')
    descriptive_information = form.cleaned_data.get('descriptive_information')

    check_record_type = ['a', 'c', 'd', 'e', 'f', 't']
    check_descriptive_information = ['cdrom', 'cd-rom', 'disquete', 'diskete', 'cd', 'disquette', 'diskette']

    # if not electronic_address field check for attachment files
    if not electronic_address:
        count = 0
        for form_attach in formset_attachment:
            try:
                if form_attach.cleaned_data and form_attach.cleaned_data.get('DELETE') == False:
                    electronic_address = True
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass

    descriptive_atribute_a = ''
    # run LILACS validation check
    if not pages and not electronic_address:
        if record_type in check_record_type:
            if descriptive_information:
                descriptive_atribute_a = descriptive_information[0].get('_a').lower()

            if not descriptive_atribute_a in check_descriptive_information:
                form.add_error('pages', _('Eletronic address, fulltext file OR pages are required'))
                url_or_attachment = False

    return url_or_attachment


def check_for_publication(form, formsets, user_data):
    """
    Run additional validation across forms fields for status LILACS-Express and LILACS
    """
    valid = True
    status = form.cleaned_data['status']
    user_role = user_data['service_role'].get('LILDBI')

    # for LILACS status and not Serie Source is required descriptor and thematic area
    if status == 1 and form.document_type != 'S':
        valid = is_valid_for_publication(form, [formsets['descriptor'], formsets['thematic']])

    # for analytic is required electronic_address or page field
    if valid and 'a' in form.document_type and status != -1:
        # check for electronic_address/attachment or page
        valid = check_url_or_attachment(form, formsets['attachment'])


    return valid