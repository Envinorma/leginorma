from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Union, cast

from bs4 import BeautifulSoup
from bs4.element import Tag


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

    @property
    def sorted_sections_and_articles(self) -> List[Union['LegifranceSection', 'LegifranceArticle']]:
        return sorted([*self.sections, *self.articles], key=lambda x: x.int_ordre)

    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]) -> 'LegifranceSection':
        return cls(
            dict_['intOrdre'],
            dict_['title'],
            [LegifranceArticle.from_dict(article) for article in dict_['articles']],
            [LegifranceSection.from_dict(section) for section in dict_['sections']],
            ArticleStatus(dict_['etat']),
        )

    def extract_lines(self, keep_abrogated_content: bool) -> List[str]:
        return [self.title] + [
            line
            for section in self.sorted_sections_and_articles
            for line in section.extract_lines(keep_abrogated_content)
        ]


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

    @property
    def title(self) -> str:
        if self.num and self.num.isdigit():
            return f'Article {self.num}'
        return self.num or ''

    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]) -> 'LegifranceArticle':
        return cls(dict_['id'], dict_['content'], dict_['intOrdre'], dict_['num'], ArticleStatus(dict_['etat']))

    def extract_lines(self, keep_abrogated_content: bool) -> List[str]:
        if not keep_abrogated_content and self.etat == ArticleStatus.ABROGE:
            return []
        return [self.title] + _split_html(self.content)


@dataclass
class LegifranceText:
    visa: str
    title: str
    articles: List[LegifranceArticle]
    sections: List[LegifranceSection]
    last_modification_date: date

    @property
    def sorted_sections_and_articles(self) -> List[Union[LegifranceSection, LegifranceArticle]]:
        return sorted([*self.sections, *self.articles], key=lambda x: x.int_ordre)

    @property
    def sorted_sections(self) -> List[LegifranceSection]:
        return sorted(self.sections, key=lambda x: x.int_ordre)

    @property
    def sorted_articles(self) -> List[LegifranceArticle]:
        return sorted(self.articles, key=lambda x: x.int_ordre)

    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]) -> 'LegifranceText':
        return cls(
            dict_['visa'],
            dict_['title'],
            [LegifranceArticle.from_dict(article) for article in dict_['articles']],
            [LegifranceSection.from_dict(section) for section in dict_['sections']],
            last_modification_date=date.fromisoformat(dict_['modifDate']),
        )

    def extract_lines(self, keep_abrogated_content: bool) -> List[str]:
        return [
            line
            for section in self.sorted_sections_and_articles
            for line in section.extract_lines(keep_abrogated_content)
        ]


def _split_html(html_str: str) -> List[str]:
    soup = BeautifulSoup(html_str, 'html.parser')
    for tag in soup.find_all('p'):
        tag = cast(Tag, tag)
        tag.append('\n')
        tag.insert(0, '\n')
        tag.unwrap()
    return [x for x in str(soup).split('\n') if x]
