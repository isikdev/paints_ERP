from pydantic import BaseModel, ConfigDict


class ResponseModel(BaseModel):
    """Base model for response models."""
    model_config = ConfigDict(from_attributes=True)
