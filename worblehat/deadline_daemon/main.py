import logging
from datetime import datetime, timedelta
from textwrap import dedent

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from worblehat.services.config import Config
from worblehat.models import (
    BookcaseItemBorrowing,
    DeadlineDaemonLastRunDatetime,
    BookcaseItemBorrowingQueue,
)
from worblehat.services.email import send_email

class DeadlineDaemon:
    def __init__(self, sql_session: Session):
        self.sql_session = sql_session
        self.last_run = self.sql_session.scalars(
            select(DeadlineDaemonLastRunDatetime),
        ).one()

        self.last_run_datetime = self.last_run.time
        self.current_run_datetime = datetime.now()


    def run(self):
        logging.info('Deadline daemon started')

        self.send_close_deadline_reminder_mails()
        self.send_overdue_mails()
        self.send_newly_available_mails()
        self.send_expiring_queue_position_mails()
        self.auto_expire_queue_positions()

        self.last_run.time = self.current_run_datetime
        self.sql_session.commit()


    def _sql_subtract_date(self, x: datetime, y: timedelta):
        if self.sql_session.bind.dialect.name == 'sqlite':
            # SQLite does not support timedelta in queries
            return func.datetime(x, f'-{y.days} days')
        elif self.sql_session.bind.dialect.name == 'postgresql':
            return x - y
        else:
            raise NotImplementedError(f'Unsupported dialect: {self.sql_session.bind.dialect.name}')


    def send_close_deadline_reminder_mails(self):
        logging.info('Sending mails about items with a closing deadline')

        # TODO: This should be int-parsed and validated before the daemon started
        days = [int(d) for d in Config['deadline_daemon.warn_days_before_borrow_deadline']]

        for day in days:
            borrowings_to_remind = self.sql_session.scalars(
                select(BookcaseItemBorrowing)
                .where(
                    self._sql_subtract_date(
                        BookcaseItemBorrowing.end_time,
                        timedelta(days=day),
                    )
                    .between(
                        self.last_run_datetime,
                        self.current_run_datetime,
                    ),
                    BookcaseItemBorrowing.delivered.is_(None),
                ),
            ).all()
            for borrowing in borrowings_to_remind:
                logging.info(f'  Sending close deadline mail to {borrowing.username}@pvv.ntnu.no. {day} days left')
                send_email(
                    f'{borrowing.username}@pvv.ntnu.no',
                    'Reminder - Your borrowing deadline is approaching',
                    dedent(f'''
                        Your borrowing deadline for the following item is approaching:
                        
                        {borrowing.item.name}
                        
                        Please return the item by {borrowing.end_time.strftime("%a %b %d, %Y")}
                        ''',
                    ).strip(),
                )


    def send_overdue_mails(self):
        logging.info('Sending mails about overdue items')

        to_remind = self.sql_session.scalars(
            select(BookcaseItemBorrowing)
            .where(
                BookcaseItemBorrowing.end_time < self.current_run_datetime,
                BookcaseItemBorrowing.delivered.is_(None),
            )
        ).all()

        for borrowing in to_remind:
            logging.info(f'  Sending overdue mail to {borrowing.username}@pvv.ntnu.no for {borrowing.item.isbn} - {borrowing.end_time.strftime("%a %b %d, %Y")}')
            send_email(
                f'{borrowing.username}@pvv.ntnu.no',
                'Your deadline has passed',
                dedent(f'''
                    Your delivery deadline for the following item has passed:
                    
                    {borrowing.item.name}
                    
                    Please return the item as soon as possible.
                    ''',
                ).strip(),
            )


    def send_newly_available_mails(self):
        logging.info('Sending mails about newly available items')

        newly_available = self.sql_session.scalars(
            select(BookcaseItemBorrowingQueue)
            .join(
                BookcaseItemBorrowing,
                BookcaseItemBorrowing.fk_bookcase_item_uid == BookcaseItemBorrowingQueue.fk_bookcase_item_uid,
            )
            .where(
                BookcaseItemBorrowingQueue.expired.is_(False),
                BookcaseItemBorrowing.delivered.is_not(None),
                BookcaseItemBorrowing.delivered.between(
                    self.last_run_datetime,
                    self.current_run_datetime,
                ),
            )
            .order_by(BookcaseItemBorrowingQueue.entered_queue_time)
            .group_by(BookcaseItemBorrowingQueue.fk_bookcase_item_uid)
        ).all()

        for queue_item in newly_available:
            logging.info(f'Sending newly available mail to {queue_item.username}')
            logging.warning('Not implemented')


    def send_expiring_queue_position_mails(self):
        logging.info('Sending mails about queue positions which are expiring soon')
        logging.warning('Not implemented')


    def auto_expire_queue_positions(self):
        logging.info('Expiring queue positions which are too old')
        logging.warning('Not implemented')