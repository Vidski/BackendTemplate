from Emails.factories.block import BlockFactory


class BlockFaker(BlockFactory):
    title: str = "test"
    content: str = "test"
    show_link: bool = True
    link_text: str = "test"
    link: str = "test.com"
