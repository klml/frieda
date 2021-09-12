from django.db import models

# TODO
# in DB
berids = (
    ('ERZ', 'Erziehung'),
    ('SEN', 'Senioren'),
    ('SOP', 'Sonderpädagogik')
)

class CommonBaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    class Meta:
        abstract = True


class Metacontent(CommonBaseModel):
    path            = models.CharField(max_length=100)
    content         = models.TextField(max_length=5000, blank=True)
    def __str__(self):
        return self.path


class School(CommonBaseModel):
    name            = models.CharField(max_length=100)
    mapbox          = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name


class Organisation(CommonBaseModel):
    name            = models.CharField(max_length=100)
    contactperson   = models.CharField(max_length=100, blank=True)
    street          = models.CharField(max_length=100, blank=True)
    zip             = models.CharField(max_length=5,   blank=True)
    city            = models.CharField(max_length=100, blank=True)
    phone           = models.CharField(max_length=100, blank=True)
    mail            = models.EmailField(blank=True)
    homepage        = models.URLField(max_length=300, blank=True)
    comment         = models.TextField(max_length=800, blank=True)
    schule          = models.ForeignKey(School, on_delete = models.PROTECT, null=True, blank=True)
    def __str__(self):
        return self.name


class Internship(CommonBaseModel):
    name            = models.CharField(max_length=150, blank=True)
    organisation    = models.ForeignKey(Organisation, on_delete = models.PROTECT)
    berid           = models.CharField(max_length=3,   blank=True)
    street          = models.CharField(max_length=100, blank=True)
    zip             = models.CharField(max_length=5,   blank=True)
    city            = models.CharField(max_length=100, blank=True)
    geo             = models.CharField(max_length=100, blank=True)
    publictransport = models.CharField(max_length=100, blank=True)
    contactperson   = models.CharField(max_length=100, blank=True)
    phone           = models.CharField(max_length=100, blank=True)
    # mail            = models.EmailField(blank=True) ## can not use mail, some email are doubled e.g. "alice@examle.com,bob@dot.net"
    mail            = models.CharField(max_length=100, blank=True)
    commentintern   = models.TextField(max_length=800, blank=True)
    commentextern   = models.TextField(max_length=800, blank=True)
    interview       = models.TextField(max_length=800, blank=True)
    biost           = models.BooleanField(default=False)
    care            = models.BooleanField(default=False)
    efz             = models.BooleanField(default=False)
    driverlicence   = models.BooleanField(default=False)
    least18         = models.BooleanField(default=False)
    allcourse       = models.BooleanField(default=False)
    todo            = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name


class SchoolYear(CommonBaseModel):
    name            = models.CharField(max_length=100) ## default 2021
    active          = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class InternshipAssignment(CommonBaseModel):
    schoolyear      = models.ForeignKey(SchoolYear, on_delete = models.PROTECT)
    internship      = models.ForeignKey(Internship, on_delete = models.PROTECT)
    ablock          = models.CharField(max_length=100, blank=True)
    bblock          = models.CharField(max_length=100, blank=True)
    student_a_1     = models.CharField(max_length=100, blank=True)
    student_b_1     = models.CharField(max_length=100, blank=True)
    student_a_2     = models.CharField(max_length=100, blank=True)
    student_b_2     = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return ( self.schoolyear.name + ' ' + self.internship.organisation.name + ' - ' + self.internship.name )