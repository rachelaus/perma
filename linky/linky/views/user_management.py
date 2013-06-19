import logging

from linky.forms import EditorRegForm, regisrtar_member_register_form, registrar_form
from linky.models import Registrar

from django.contrib.auth.decorators import login_required
from django.http import  HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User, Permission, Group


logger = logging.getLogger(__name__)

try:
    from linky.local_settings import *
except ImportError, e:
    logger.error('Unable to load local_settings.py:', e)


@login_required
def landing(request):
    """ The logged-in user's dashboard """
    
    print request.user.groups.values_list('name',flat=True)
    
    context = {'user': request.user}

    return render_to_response('user_management/landing.html', context)
    

@login_required
def manage_members(request):
    """ Linky admins can manage jounral members (the folsk taht vest links) """

    registrars = User.objects.filter(groups__name='registrar_member')

    context = {'user': request.user, 'registrar_members': list(registrars)}
    context.update(csrf(request))

    if request.method == 'POST':

        form = regisrtar_member_register_form(request.POST, prefix = "a")

        if form.is_valid():
            new_user = form.save()

            new_user.backend='django.contrib.auth.backends.ModelBackend'
            auth.login(request, new_user)

            group = Group.objects.get(name='registrar_member')
            group.user_set.add(new_user)

            return HttpResponseRedirect(reverse('user_management_manage_registrar_member'))

        else:
            context.update({'regisrtar_register_form': form,})                      
    else:
        form = regisrtar_member_register_form(prefix = "a")
        context.update({'regisrtar_register_form': form,}) 

    return render_to_response('user_management/manage_registrar_members.html', context)
    
@login_required
def manage_registrar(request):
    """ Linky admins can manage registrars (libraries) """

    # TODO: support paging at some point
    registrars = Registrar.objects.all()[:500]

    context = {'user': request.user, 'registrars': list(registrars)}
    context.update(csrf(request))
    
    if request.method == 'POST':

        form = registrar_form(request.POST, prefix = "a")
        
        if form.is_valid():
            new_user = form.save()
            
            return HttpResponseRedirect(reverse('user_management_manage_registrar'))
        
        else:
            context.update({'form': form,})                      
    else:
        form = registrar_form(prefix = "a")
        context.update({'form': form,}) 

    return render_to_response('user_management/manage_registrars.html', context)
    
@login_required
def manage_registrar_member(request):
    """ Linky admins can manage registrar members (librarians) """

    registrar_members = User.objects.filter(groups__name='registrar_member')

    context = {'user': request.user, 'registrar_members': list(registrar_members)}
    context.update(csrf(request))
    
    if request.method == 'POST':

        form = regisrtar_member_register_form(request.POST, prefix = "a")
        
        if form.is_valid():
            new_user = form.save()

            new_user.backend='django.contrib.auth.backends.ModelBackend'
            auth.login(request, new_user)

            group = Group.objects.get(name='registrar_member')
            group.user_set.add(new_user)
            
            return HttpResponseRedirect(reverse('user_management_manage_registrar_member'))
        
        else:
            context.update({'form': form,})                      
    else:
        form = regisrtar_member_register_form(prefix = "a")
        context.update({'form': form,}) 

    return render_to_response('user_management/manage_registrar_members.html', context)


def process_register(request):
    """Register a new user"""
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':

        reg_key = request.POST.get('reg_key', '')
                
        editor_reg_form = EditorRegForm(request.POST, prefix = "a")
        
        if editor_reg_form.is_valid():
            new_user = editor_reg_form.save()

            new_user.backend='django.contrib.auth.backends.ModelBackend'
            auth.login(request, new_user)
            
            return HttpResponseRedirect(reverse('landing'))
        
        else:
            c.update({'editor_reg_form': editor_reg_form,})
                      
            return render_to_response('registration/register.html', c)
    else:
        editor_reg_form = EditorRegForm(prefix = "a")
        
        c.update({'editor_reg_form': editor_reg_form,})
        return render_to_response("registration/register.html", c)