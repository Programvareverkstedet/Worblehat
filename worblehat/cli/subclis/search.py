from sqlalchemy import select
from sqlalchemy.orm import Session


from worblehat.cli.prompt_utils import (
    NumberedCmd,
    NumberedItemSelector,
)
from worblehat.models import Author, BookcaseItem


class SearchCli(NumberedCmd):
    def __init__(self, sql_session: Session):
        super().__init__()
        self.sql_session = sql_session


    def do_search_all(self, _: str):
        print('TODO: Implement search all')


    def do_search_title(self, _: str):
        while (input_text := input('Enter title: ')) == '':
            pass

        items = self.sql_session.scalars(
            select(BookcaseItem)
            .where(BookcaseItem.name.ilike(f'%{input_text}%')),
        ).all()

        if len(items) == 0:
            print('No items found.')
            return

        selector = NumberedItemSelector(
            items = items,
            stringify = lambda item: f"{item.name} ({item.isbn})",
        )
        selector.cmdloop()
        if selector.result is not None:
            self.result = selector.result
            return True


    def do_search_author(self, _: str):
        while (input_text := input('Enter author name: ')) == '':
            pass

        author = self.sql_session.scalars(
            select(Author)
            .where(Author.name.ilike(f'%{input_text}%')),
        ).all()

        if len(author) == 0:
            print('No authors found.')
            return
        elif len(author) == 1:
            selected_author = author[0]
            print('Found author:')
            print(f"  {selected_author.name} ({sum(item.amount for item in selected_author.books)} items)")
        else:
            selector = NumberedItemSelector(
                items = author,
                stringify = lambda author: f"{author.name} ({sum(item.amount for item in author.books)} items)",
            )
            selector.cmdloop()
            if selector.result is None:
                return
            selected_author = selector.result

        selector = NumberedItemSelector(
            items = selected_author.books,
            stringify = lambda item: f"{item.name} ({item.isbn})",
        )
        selector.cmdloop()
        if selector.result is not None:
            self.result = selector.result
            return True


    def do_search_owner(self, _: str):
        while (input_text := input('Enter username: ')) == '':
            pass

        users = self.sql_session.scalars(
            select(BookcaseItem.owner)
            .where(BookcaseItem.owner.ilike(f'%{input_text}%'))
            .distinct(),
        ).all()

        if len(users) == 0:
            print('No users found.')
            return
        elif len(users) == 1:
            selected_user = users[0]
            print('Found user:')
            print(f"  {selected_user}")
        else:
            selector = NumberedItemSelector(items = users)
            selector.cmdloop()
            if selector.result is None:
                return
            selected_user = selector.result

        items = self.sql_session.scalars(
            select(BookcaseItem)
            .where(BookcaseItem.owner == selected_user),
        ).all()

        selector = NumberedItemSelector(
            items = items,
            stringify = lambda item: f"{item.name} ({item.isbn})",
        )
        selector.cmdloop()
        if selector.result is not None:
            self.result = selector.result
            return True


    def do_done(self, _: str):
        return True


    funcs = {
        1: {
            'f': do_search_all,
            'doc': 'Search everything',
        },
        2: {
            'f': do_search_title,
            'doc': 'Search by title',
        },
        3: {
            'f': do_search_author,
            'doc': 'Search by author',
        },
        4: {
            'f': do_search_owner,
            'doc': 'Search by owner',
        },
        9: {
            'f': do_done,
            'doc': 'Done',
        },
    }