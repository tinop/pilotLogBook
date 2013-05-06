from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from flightlog.models import PilotUser
from datetime import date, timedelta, datetime


def addUser(group, account, first_name, last_name,pwd, **kwargs):
    
    if PilotUser.objects.filter(username=account).exists():
        logging.info('User %s already exists, skipping')
        return
    
    email = kwargs['email'] if 'email' in kwargs else '{0}.{1}@dacuda.com'.format(first_name.lower(), last_name.lower())
    
    user = PilotUser.objects.create_user(account, email, account+'.')
    user.first_name = first_name
    user.last_name = last_name
    user.password = pwd
    user.expireData = date.today()
    user.groups.add(group)
    user.is_staff = True
    user.save()

def addPilotUser():
    # First we add the group...
    group, created = Group.objects.get_or_create(name='Pilot')
    if not created:
        logging.info('The group pilot already exists')
    group.save()
    
    # ... then we make sure I have a valid first/last name...
    user = User.objects.get(username='tino')
    user.first_name = 'Tino'
    user.last_name = 'Perucchi'
    user.save()
    
    # ... and finally we add the Dacudees
    addUser(group, 'p1', 'P1', '11','n')
    addUser(group, 'p2', 'P2', '22','n')


if __name__ == "__main__":
    addPilotUser()