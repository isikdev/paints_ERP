from pydantic import BaseModel, Field, field_validator


class CounterpartyBase(BaseModel):
    name: str = Field(..., example="ИП Пример")
    inn: str = Field(..., example="7701234567")
    address: str = Field(..., example="г. Москва, ул. Ленина, д. 1")

    @field_validator("inn")
    def validate_inn(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("inn must contain only digits")
        if len(v) not in (10, 12):
            raise ValueError("inn must contain 10 or 12 digits")
        return v


class CounterpartyCreate(CounterpartyBase):
    pass

class CounterpartyUpdate(CounterpartyBase):
    id: int

class CounterpartyRead(CounterpartyBase):
    id: int
