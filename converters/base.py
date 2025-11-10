"""
中間データ構造の定義
全ての変換で使用する共通のデータ形式
"""
from dataclasses import dataclass, field
from typing import List, Any, Optional
from enum import Enum


class ContentType(Enum):
    """コンテンツタイプ"""
    TEXT = 'text'
    TITLE = 'title'
    LIST_ITEM = 'list_item'
    NUMBERED_LIST = 'numbered_list'
    TABLE = 'table'
    CODE_BLOCK = 'code_block'
    EMPTY = 'empty'


@dataclass
class Content:
    """個別のコンテンツアイテム"""
    type: ContentType
    value: Any
    metadata: dict = field(default_factory=dict)
    
    def __repr__(self):
        return f"Content({self.type.value}, {self.value})"


@dataclass
class Sheet:
    """シート（セクション）を表すデータ構造"""
    name: str
    contents: List[Content] = field(default_factory=list)
    
    def add_content(self, content: Content):
        """コンテンツを追加"""
        self.contents.append(content)
    
    def __repr__(self):
        return f"Sheet('{self.name}', {len(self.contents)} items)"


@dataclass
class Document:
    """ドキュメント全体を表すデータ構造"""
    title: Optional[str] = None
    sheets: List[Sheet] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    
    def add_sheet(self, sheet: Sheet):
        """シートを追加"""
        self.sheets.append(sheet)
    
    def get_sheet(self, name: str) -> Optional[Sheet]:
        """名前でシートを取得"""
        for sheet in self.sheets:
            if sheet.name == name:
                return sheet
        return None
    
    def __repr__(self):
        return f"Document('{self.title}', {len(self.sheets)} sheets)"


# テーブル用のヘルパークラス
@dataclass
class Table:
    """テーブルデータ"""
    headers: List[str]
    rows: List[List[str]]
    
    def __repr__(self):
        return f"Table({len(self.headers)} cols, {len(self.rows)} rows)"
