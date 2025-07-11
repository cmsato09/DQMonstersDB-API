from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Item(SQLModel, table=True):
    """
    Lists all items sold in shops and found in the field
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    item_name: str
    item_category: str
    item_description: str
    price: Optional[int] = Field(default=None)
    sell_price: Optional[int] = Field(default=None)
    sell_location: str

    ja_translation: Optional["ItemJA"] = Relationship(backpopulates="item")


class ItemJA(SQLModel, table=True):
    """
    Japanese translation for Item
    """

    __tablename__ = "item_ja"

    id: Optional[int] = Field(default=None, primary_key=True)
    name_ja: str
    category_ja: str
    description_ja: str
    shop_ja: str

    item_id: Optional[int] = Field(default=None, foreign_key="item.id")
    item: Optional[Item] = Relationship(back_popluates="ja_translation")
