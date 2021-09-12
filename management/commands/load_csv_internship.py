from csv import DictReader
from django.core.management import BaseCommand

from django.shortcuts import render, redirect, get_object_or_404

# Import model s
from frieda.models import Internship, Organisation, SchoolYear, InternshipAssignment



ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the internship_position data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from .csv"

    def handle(self, *args, **options):



    
        # Show this if the data already exist in the database
        if Internship.objects.exists():
            print('internship_position data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading internship_position data")


        schoolyear=SchoolYear(
            name = "2021/2022"
        )
        schoolyear.save()


        #Code to load the data into database
        for row in DictReader(open('./internships.csv')):
            
            try:
                Organisation.objects.get(name=row['Einrichtung'])
            except:

                org=Organisation(
                        name                =row['Einrichtung'],
                        contactperson       =row['Ansprechpartner Einrichtung'],
                        street              =row['Strasse Hausnummer'],
                        zip                 =row['PLZ'],
                        city                =row['Ort'],
                        phone               =row['Telefon Einrichtung'],
                        mail                =row['Mail Einrichtung'],
                        homepage            =row['homepage'],
                )  
                org.save()


            internship=Internship(
                organisation            = get_object_or_404(Organisation, name= row['Einrichtung']),
                # ~ organisation            = Organisation.objects.get(name= row['Einrichtung']),
                name                    =row['Praktikumsstelle'],
                berid                   =row['BerID'],
                street                  =row['Strasse Hausnummer'],
                zip                     =row['PLZ'],
                city                    =row['Ort'],
                geo                     =row['Geo'],
                publictransport         =row['MVV'],
                contactperson           =row['Ansprechpartner Stelle'],
                phone                   =row['Telefon Stelle'],
                mail                    =row['Mail Stelle'],
                commentintern           =row['BemerkungIntern'],
                commentextern           =row['BemerkungExtern'],
                interview               =row['Vorstellung'],
                biost                   =row['BioSt'],
                todo                    =row['Todo'],
                # ~ allcourse               = if (row['A-Block'] == "b"): true ; False
            )  
            internship.save()
   
            internshipassignment=InternshipAssignment(
                schoolyear      = get_object_or_404(SchoolYear, id=1),
                internship      = internship,
                ablock          = row['A-Block'],
                bblock          = row['B-Block']
                # ~ student_a_1     
                # ~ student_b_1     
                # ~ student_a_2     
                # ~ student_b_2
            )
            internshipassignment.save()

            print(internship)