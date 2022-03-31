from datetime import datetime
from dateutil.relativedelta import relativedelta
import factory

from Users.factories.profile import ProfileFactory


class FemaleProfileFaker(ProfileFactory):
    bio = 'Custom bio for female profile'
    gender = 'F'

class MaleProfileFaker(ProfileFactory):
    bio = 'Custom bio for male profile'
    gender = 'M'

class NonBinaryProfileFaker(ProfileFactory):
    bio = 'Custom bio for non-binary profile'
    gender = 'N'

class NotSaidProfileFaker(ProfileFactory):
    bio = 'Custom bio for x profile'
    gender = 'P'

class AdultProfileFaker(ProfileFactory):
    bio = 'Custom bio for adult profile'
    birth_date = factory.LazyAttribute(
        lambda object: (
            (datetime.now() - relativedelta(years=20)).strftime('%Y-%m-%d')
        )
    )

class KidProfileFaker(ProfileFactory):
    bio = 'Custom bio for kid profile'
    birth_date = factory.LazyAttribute(
        lambda object: (
            (datetime.now() - relativedelta(years=15)).strftime('%Y-%m-%d')
        )
    )
