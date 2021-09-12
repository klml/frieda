from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers


from django.apps import apps

from django.db.models import Q

import csv
import markdown

from .models import *
from .forms import *


def save_as_csv():
    for model in apps.get_models('frieda'):
        # blacklist django internal models like django.contrib.sessions.models.Session
        # TODO dont check only the string
        if "django" not in str(model):
            yaml = serializers.serialize("yaml", model.objects.all())
            f = open( 'backup/' + str(model._meta) + 'model.yaml', 'w+' )
            f.write( yaml )
            f.close()
    # TODO git commit
    return 

@login_required
def internship_organisation_csv(request):

    internships             = Internship.objects.all()
    organisations           = Organisation.objects.all()
    #  TODO student 

    internships_field_names    = [field.name for field in internships.model._meta.fields]
    # add specific fields from organisation 
    field_names = [*internships_field_names, *["contactperson","phone","mail","comment"]]

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="stellen.csv"'},
    )

    writer = csv.writer(response)
    # Write a first row with header information
    writer.writerow(field_names)

    # Write data rows
    for internship in internships:
        internship_row = [getattr(internship, field) for field in internships_field_names]
        internship_row = [*internship_row, 
            internship.organisation.contactperson,
            internship.organisation.phone,
            internship.organisation.mail,
            internship.organisation.comment
        ]
        writer.writerow(internship_row)
    return response

def organisations (request):

    filterargs = {  } 
    organisations = Organisation.objects.filter( **filterargs ).order_by('id')[:200]

    return render(request, 'frieda/organisations.html', {'organisations': organisations })


@login_required
def organisation (request, pk=None):

    # TODO school_year from GET
    try:
        school_year = SchoolYear.objects.get(active=True)
    except Content.DoesNotExist:
        school_year = None

    if pk :        
        organisation            = get_object_or_404(Organisation, pk=pk)
        internships             = Internship.objects.filter(organisation=pk)
    # new organisation
    else :
        organisation            = Organisation()
        internships    = []
        
    # organisation
    organisation_form           = Organisation_Form(request.POST or None, instance=organisation)
    
    print(request.user.is_staff)
    if request.POST and organisation_form.is_valid() and request.user.is_staff :
        organisation = organisation_form.save()
        save_as_csv()

    # all existing internship for this organisation   
    internship_forms   = []

    for internship in internships:
        internship_form      = Internship_Form(request.POST or None, prefix="offers" + str(internship.id), instance=internship) 

        # assign internship to students per active school_year and semester
        try:
            # TODO filter schoolyear
            internship_assignment               = InternshipAssignment.objects.get(internship=internship.id) ## assume ther is only ONE assignement TODO
        except:
            internship_assignment               = InternshipAssignment()
            internship_assignment.internship    = internship

        internship_assignment.schoolyear        = school_year
        internship_assignments_form             = InternshipAssignments_Form(request.POST or None, prefix="offers" + str(internship.id), instance=internship_assignment) 
        internship_form.assignment              = internship_assignments_form

        internship_forms.append( internship_form )
        
        # TODO https://docs.djangoproject.com/en/dev/ref/models/querysets/#bulk-update
        if request.POST and internship_form.is_valid() and request.user.is_staff :
            internship_form.save()
            internship_assignments_form.save()

    # add additional and empty form for new offers
    internship_new     = Internship()
    internship_new_form = Internship_Form(request.POST or None, prefix="offers_new" , instance=internship_new)
    internship_forms.append( internship_new_form )

    # save only when new offer is not empty
    # second send is need to EDIT and ADD internship
    if request.POST and internship_new_form.data["offers_new-name"] and internship_new_form.is_valid() and request.user.is_staff :
        internship_new.organisation = organisation # return from save organisation
        internship_new_form.save()

    if request.POST :
        return redirect('organisation', pk=organisation.id )

    return render(request, 'frieda/organisation.html', { 
        'organisation': organisation_form ,
        'internships':  internship_forms ,
        'pk': pk
    })



@login_required
def internships (request):

    filterargs = { } 
    excludeargs = { } 

    # /?id=42
    if request.GET.get('id') :
        id = request.GET['id']
        filterargs.update ( { 'id' : id } )

    # /?ber=SEN
    if request.GET.get('ber') :
        ber = request.GET['ber']
        filterargs.update ( { 'berid' : ber } )

    # /?todo=True
    if request.GET.get('todo') :
        excludeargs.update ( { 'todo' : "" } )

    # /?allcourse=True
    if request.GET.get('allcourse') :
        filterargs.update ( { 'allcourse' : True } )

    # /?course=S11b
    # handle course extra 
    # from Model InternshipAssignment
    if request.GET.get('course') :
        course = request.GET['course']

        internships = []
        # add all Internships assigend to all courses
        for allcourse in Internship.objects.filter( allcourse = True ):
            internships.append(allcourse.id)

        # get all not assigened internships
        if course == "empty":
            internships = []
            course = ""

        internshipassignments = InternshipAssignment.objects.filter( Q(ablock=course) | Q(bblock=course) )
        # TODO schoolyear active
        for internshipassignment in internshipassignments:
            internships.append(internshipassignment.internship.id)


        # create filter for django.db.models.query.QuerySet from list
        filterargs.update ( pk__in=internships )

    internships = Internship.objects.filter( **filterargs ).exclude(**excludeargs).order_by('id')[:200]

    internships_ber = []
    for ber in berids:
        filterargs.update( { 'berid' : ber[0] } )
        countfilter     = Internship.objects.filter( **filterargs ).exclude(**excludeargs).count()
        countall        = Internship.objects.filter( berid = ber[0] ).count()

        internships_ber.append([ber[0], ber[1], countfilter, countall])

    return render(request, 'frieda/internships.html', {'internships': internships , 'internships_ber': internships_ber })


def index(request):

    if request.POST:
        if request.POST.get('username') :
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                # Return an 'invalid login' error message.
                print('invalid login')
                return render(request, 'frieda/index.html', {'AuthenticationForm': "invalid login" })

        if request.POST.get('logout') :
            logout(request)

    return render(request, 'frieda/index.html', {'AuthenticationForm': AuthenticationForm })
    
def content(request):

    try:
        content = Metacontent.objects.get(path=request.path[1 : ]).content
    except:
        content = "Ask the administrator to add some content."
    content = markdown.markdown( content ) 

    return render(request, 'frieda/content.html', { 'content': content })