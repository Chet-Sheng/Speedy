class Account:
    def __init__(self, username, email, date_joined):
        self.username = username
        self.email = email
        self.date_joined = date_joined

    def __str__(self):
        return '%s (%s) joined at %s' % (self.username, self.email, self.date_joined)


class Profile:

    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_UNKNOWN = 'u'  # If the user refused to give it

    def __init__(self, account, gender, firstname, lastname, planet='Earth'):
        self.account = account
        self.gender = gender
        self.firstname = firstname
        self.lastname = lastname
        self.planet = planet

    def __str__(self):
        return '%s %s (%s) joined at (s)' % (
            self.firstname,
            self.lastname,
            self.account.username,
        )
