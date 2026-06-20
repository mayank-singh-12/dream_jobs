"""excluding_teacher_from_user_role_(added_by_mistake)_including_company

Revision ID: 3c3569182684
Revises: 53b3dd370415
Create Date: 2026-06-05 19:46:49.689649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c3569182684'
down_revision: Union[str, Sequence[str], None] = '53b3dd370415'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("UPDATE users SET role = 'student' WHERE role::text NOT IN ('admin', 'company', 'student')")
    op.execute("ALTER TABLE users ALTER COLUMN role DROP DEFAULT")
    op.execute("ALTER TYPE user_role RENAME TO user_role_old")
    company_status = sa.Enum("admin" ,"company" ,"student" ,name="user_role")
    company_status.create(op.get_bind(), checkfirst=True)
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE user_role USING role::text::user_role")
    op.execute("ALTER TABLE users ALTER COLUMN role SET DEFAULT 'student'::user_role")
    op.execute("DROP TYPE user_role_old")

def downgrade() -> None:
    """Downgrade schema."""
    pass
