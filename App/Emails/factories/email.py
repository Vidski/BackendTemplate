import factory

from Emails.factories.block import BlockFactory
from Emails.models import Email


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Email

    subject = factory.Faker('sentence')
    header = factory.Faker('word')
    blocks = factory.SubFactory(BlockFactory)
    is_test = False
    to_all_users = False
    to = factory.Faker('email')
    template = 1
    programed_send_date = factory.Faker('date_time')
    sent_date = factory.Faker('date_time')
    was_sent = False

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for block in extracted:
                self.blocks.add(block)
        else:
            self.blocks.add(BlockFactory())