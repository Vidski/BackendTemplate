import factory

from Emails.models import Block


class BlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Block

    title = factory.Faker('word')
    content = factory.Faker('sentence')
    show_link = factory.Faker('boolean')
    link_text = factory.Faker('word')
    link = factory.Faker('url')
