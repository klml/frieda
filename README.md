## Frieda

__Frieda__ is a management tool to assign external internships for students.

Made with [Django](https://www.djangoproject.com).


[![screenshot frieda stellenliste](//img.klml.de/devel/frieda_stellenliste__520.png)](https://img.klml.de/devel/frieda_stellenliste.png)

### Import

Add internships and correspodning organisations in `internships.csv` (use example from `/static/frieda/internship_organisation.example.csv`)

```bash
python3 manage.py migrate
python3 manage.py load_csv_internship 
```

