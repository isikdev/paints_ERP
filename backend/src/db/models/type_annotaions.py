from typing import Annotated

from sqlalchemy import String, ForeignKey, Integer, DateTime, func, text, Text
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB

import datetime
import uuid

from constants import MAX_NAME_LENGTH

# common
uuid_pk = Annotated[uuid.UUID, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)]
created_at = Annotated[
    datetime.datetime,
    mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
]
text_type = Annotated[str, mapped_column(Text, nullable=False, server_default=text("''"))]

# AbstractDocument
document_number = Annotated[int, mapped_column(Integer, nullable=False)]
document_name = Annotated[str | None, mapped_column(String(MAX_NAME_LENGTH))]
document_status_name = Annotated[str, mapped_column(String(50), nullable=False)]
document_datetime = Annotated[
    datetime.datetime,
    mapped_column(DateTime(timezone=True), nullable=False)
]
document_type_fk = Annotated[
    uuid.UUID,
    mapped_column(UUID(as_uuid=True), ForeignKey("document_types.id", ondelete="RESTRICT"), nullable=False)
]

# DocumentNumberCounter
year = Annotated[int, mapped_column(Integer, nullable=False)]
counter = Annotated[int, mapped_column(Integer, nullable=False, default=0)]
document_type_counter_fk = Annotated[
    document_type_fk,
    mapped_column(ForeignKey("document_types.id", ondelete="CASCADE"))
]

# DocumentType
type_name = Annotated[str, mapped_column(String(MAX_NAME_LENGTH), nullable=False, unique=True)]

# BaseRecipe
rules = Annotated[dict[str, any], mapped_column(JSONB, nullable=False)]
