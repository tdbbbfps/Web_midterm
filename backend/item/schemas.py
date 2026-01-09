from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ItemBase(BaseModel):
    name: str = Field(..., description="Item's name.")
    image: str = Field(..., description="道具的圖片 URL")
    description: str = Field(..., description="Item's description.")
    price: int = Field(..., description="Item's price.", gt=0)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None

class Item(ItemBase):
    id: int = Field(..., description="Item's ID.")
    
    model_config = ConfigDict(from_attributes=True)

class ItemRead(BaseModel):
    id: int = Field(..., description="Item's ID.")
    name: str = Field(..., description="Item's name.")
    image: str = Field(..., description="Item's image URL.")
    description: str = Field(..., description="Item's description.")
    price: float = Field(..., description="Item's price.")
