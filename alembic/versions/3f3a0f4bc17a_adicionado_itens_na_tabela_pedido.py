"""adicionado itens na tabela Pedido

Revision ID: 3f3a0f4bc17a
Revises: c3849cf6fe94
Create Date: 2025-06-19 14:51:30.997481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f3a0f4bc17a'
down_revision: Union[str, None] = 'c3849cf6fe94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
