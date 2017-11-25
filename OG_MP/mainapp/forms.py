from django import forms


class MineralForm(forms.Form):
    MINERAL_CHOICES = [
        ("PB", "PB"),
        ("CU", "CU"),
        ("ZI", "ZI"),
    ]
    MINERAL_CHOICES = [
        ("PB", "PB"),
        ("CU", "CU"),
        ("ZI", "ZI"),
    ]
    YEAR_CHOICE = [
        ("2012", "2012"),
        ("2013", "2013"),
        ("2014", "2014"),
        ("2015", "2015"),
        ("2016", "2016"),
        ("2017", "2017"),
    ]
    mineral = forms.ChoiceField(
                              choices=MINERAL_CHOICES,
                              widget=forms.Select(attrs={
                                                  'id': 'mineral_input',
                                                  'class': 'form-control'})
                              )
    start_year = forms.ChoiceField(
                                 choices=YEAR_CHOICE,
                                 widget=forms.Select(attrs={
                                                     'id': 'start_year',
                                                     'class': 'form-control'})
                                 )
    end_year = forms.ChoiceField(
                               choices=YEAR_CHOICE,
                               widget=forms.Select(attrs={
                                                   'id': 'end_year',
                                                   'class': 'form-control'}))
    def clean(self):
        cleaned_data = super(MineralForm, self).clean()
        mineral = cleaned_data.get("mineral")
        start_year = cleaned_data.get("start_year")
        end_year = cleaned_data.get("end_year")

        if int(start_year) > int(end_year):
            msg = "End Year should be greater than or equal to Start Year"
            self.add_error('end_year', msg)
