from sqlalchemy import select
from sqlalchemy.orm import Session

from worblehat.cli.prompt_utils import InteractiveItemSelector
from worblehat.models import (
    Bookcase,
    BookcaseShelf,
)

def select_bookcase_shelf(
    bookcase: Bookcase,
    sql_session: Session,
    prompt: str = "Please select the shelf where the item is placed (col-row):"
) -> BookcaseShelf:
    def __complete_bookshelf_selection(session: Session, cls: type, arg: str):
        args = arg.split('-')
        query = select(cls.row, cls.column).where(cls.bookcase == bookcase)
        try:
            if arg != '' and len(args) > 0:
                query = query.where(cls.column == int(args[0]))
            if len(args) > 1:
                query = query.where(cls.row == int(args[1]))
        except ValueError:
            return []

        result = session.execute(query).all()
        return [f"{c}-{r}" for r,c in result]

    print(prompt)
    bookcase_shelf_selector = InteractiveItemSelector(
        cls = BookcaseShelf,
        sql_session = sql_session,
        execute_selection = lambda session, cls, arg: session.scalars(
            select(cls)
            .where(
              cls.bookcase == bookcase,
              cls.column == int(arg.split('-')[0]),
              cls.row == int(arg.split('-')[1]),
            )
        ).all(),
        complete_selection = __complete_bookshelf_selection,
    )

    bookcase_shelf_selector.cmdloop()
    return bookcase_shelf_selector.result