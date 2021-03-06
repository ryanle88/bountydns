from os.path import join
from bountydns.core.utils import db_dir, load_env
from bountydns.db.session import session, db_register
from bountydns.db.utils import make_db_url
from bountydns.db.migrate.show import show
from bountydns.cli.commands.base import BaseCommand


class AlembicShow(BaseCommand):
    name = "alembic-show"
    aliases = ["al-show"]
    description = "run alembic show"
    migration_dir = join(db_dir("alembic"), "api")

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        load_env("api")
        db_register(make_db_url())
        show(self.migration_dir)
