"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum

class Poll(models.Model):
    """A poll object for use in the application views and repository."""
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def total_votes(self):
        """Calculates the total number of votes for this poll."""
        return self.choice_set.aggregate(Sum('votes'))['votes__sum']

    def __unicode__(self):
        """Returns a string representation of a poll."""
        return self.text

class Choice(models.Model):
    """A poll choice object for use in the application views and repository."""
    poll = models.ForeignKey(Poll)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def votes_percentage(self):
        """Calculates the percentage of votes for this choice."""
        total = self.poll.total_votes()
        return self.votes / float(total) * 100 if total > 0 else 0

    def __unicode__(self):
        """Returns a string representation of a choice."""
        return self.text


class House(models.Model):
    name = models.CharField(max_length = 200, help_text="Укажите название дома")
    address = models.CharField(max_length = 200)

    def __str__(self):
        return self.address

class Flat(models.Model):
    house = models.ForeignKey('House',on_delete=models.SET_NULL,null=True)
    numberFlat = models.CharField(max_length=10,help_text="Укажите номер квартиры")
    entrance = models.IntegerField()
    floor = models.IntegerField()
    square = models.CharField(max_length=10,help_text="Укажите площадь квартиры")

    def __str__(self):
        return 'Кв. %s' % (self.numberFlat)

class People(models.Model):
    flat = models.ForeignKey('Flat',on_delete=models.SET_NULL,null=True)
    lastname = models.CharField(verbose_name = 'Фамилия',max_length = 200)
    firstname = models.CharField(verbose_name = 'Имя',max_length = 200)
    fathername = models.CharField(verbose_name = 'Отчество',max_length = 200)
    birthday = models.DateField(verbose_name = 'Дата рождения',null = False)
    TYPE_DOCUMENTS = (
        ('п','Паспорт'),
        ('св','Свидетельство о рождении'),
        ('ин','Паспорт иностранного гражданина')
    )
    docType = models.CharField(max_length=3,choices = TYPE_DOCUMENTS,blank=True,default='п', help_text='Укажите тип документа')
    docSeries = models.CharField(max_length = 5)
    docNumber = models.CharField(max_length = 8)
    docIssueDate = models.DateField(null = True)
    docIssueOrg = models.TextField()
    owner = models.BooleanField(verbose_name = 'Собственник')
    PART_OWNER = (
        ('-','-'),
        ('1','целая'),
        ('1/2','одна втрорая'),
        ('1/3','одна третья'),
        ('1/4','одна четвертая')
    )
    ownerPart = models.CharField(verbose_name = 'Часть собственности',default = '-',choices = PART_OWNER,max_length = 200)

    def __str__(self):
        return '%s %s %s %s (кв. %s)' % (self.lastname,self.firstname,self.fathername,self.birthday ,self.flat.numberFlat)





