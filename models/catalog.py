from datetime import datetime

from pydantic import BaseModel


class CatalogMetadata(BaseModel):

    catalog_id: str

    file_name: str

    uploaded_datetime: datetime

    uploaded_by: str