from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class ArticleStatus(Enum):
    VIGUEUR = 'VIGUEUR'
    ABROGE = 'ABROGE'


@dataclass
class LegifranceSection:
    int_ordre: int
    title: str
    articles: List['LegifranceArticle']
    sections: List['LegifranceSection']
    etat: ArticleStatus

    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]) -> 'LegifranceSection':
        return cls(
            dict_['intOrdre'],
            dict_['title'],
            [LegifranceArticle.from_dict(article) for article in dict_['articles']],
            [LegifranceSection.from_dict(section) for section in dict_['sections']],
            ArticleStatus(dict_['etat']),
        )


@dataclass
class LegifranceArticle:
    id: str
    content: str
    int_ordre: int
    num: Optional[str]
    etat: ArticleStatus

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'intOrdre': self.int_ordre,
            'num': self.num,
            'etat': self.etat.value,
        }

    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]) -> 'LegifranceArticle':
        return cls(dict_['id'], dict_['content'], dict_['intOrdre'], dict_['num'], ArticleStatus(dict_['etat']))


@dataclass
class LegifranceText:
    visa: str
    title: str
    articles: List[LegifranceArticle]
    sections: List[LegifranceSection]

    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]) -> 'LegifranceText':
        return cls(
            dict_['visa'],
            dict_['title'],
            [LegifranceArticle.from_dict(article) for article in dict_['articles']],
            [LegifranceSection.from_dict(section) for section in dict_['sections']],
        )
