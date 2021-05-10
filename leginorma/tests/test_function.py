#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from dataclasses import replace

from leginorma import LegifranceClient, LegifranceText
from leginorma.models import ArticleStatus, _split_html


def test_client():
    client = LegifranceClient(os.environ['LEGIFRANCE_CLIENT_ID'], os.environ['LEGIFRANCE_CLIENT_SECRET'])
    LegifranceText.from_dict(client.consult_law_decree('JORFTEXT000034429274'))


def test_from_dict(legifrance_text: LegifranceText):
    assert (
        legifrance_text.title == "Arrêté du 14 janvier 2000 relatif aux prescriptions générales applicables "
        "aux installations classées pour la protection de l'environnement"
        " soumises à déclaration sous la rubrique n° 2662 (Stockage de polymères matières plastiques, "
        "caoutchouc, élastomères, résines et adhésifs synthétiques)"
    )


def test_extract_text_lines(legifrance_text: LegifranceText):
    expected_lines = [
        'Article 1',
        "Les installations classées pour la protection de l'environnement soumises"
        " à déclaration sous la rubrique n° 2662 (Stockage de polymères matières "
        "plastiques, caoutchouc, élastomères, résines et adhésifs synthétiques, le"
        " volume étant supérieur ou égal à 100 mètres cubes, mais inférieur à 1 000 mètres cubes)"
        " sont soumises aux dispositions de l'annexe I. Les présentes dispositions s'appliquent "
        "sans préjudice des autres législations.",
        'Article 2',
        "I. - Les dispositions de l'annexe I sont applicables :",
        '- aux installations nouvelles dès la date de publication du présent arrêté au Journal '
        'officiel de la République française ;',
        "- aux installations existant avant la date de publication du présent arrêté au Journal "
        "officiel de la République française selon les délais mentionnés à l'annexe II.",
        "II. - Les prescriptions auxquelles les installations existantes sont déjà soumises demeurent"
        " applicables jusqu'à la date de mise en application des dispositions équivalentes du présent"
        " arrêté selon les modalités définies à l'annexe II.",
        'Article 3',
        'Le préfet peut, pour une installation donnée, modifier par arrêté les dispositions des '
        'annexes I et II dans les conditions prévues aux articles 11 de la loi du 19 juillet 1976 et'
        ' 30 du décret du 21 septembre 1977 susvisés.',
        'Article 4',
        "Le directeur de la prévention des pollutions et des risques est chargé de l'exécution du "
        "présent arrêté, qui sera publié au Journal officiel de la République française.",
        'Annexes',
        'Annexe I',
        '1. Dispositions générales',
    ]
    computed_lines = legifrance_text.extract_lines(False)
    for computed, expected in zip(computed_lines, expected_lines):
        assert computed == expected


def test_extract_article_lines(legifrance_text: LegifranceText):
    article = legifrance_text.sorted_articles[2]
    expected = [
        'Article 3',
        'Le préfet peut, pour une installation donnée, modifier par arrêté les dispositions des '
        'annexes I et II dans les conditions prévues aux articles 11 de la loi du 19 juillet 1976 et'
        ' 30 du décret du 21 septembre 1977 susvisés.',
    ]
    assert article.extract_lines(False) == expected
    assert replace(article, etat=ArticleStatus.ABROGE).extract_lines(False) == []
    assert replace(article, etat=ArticleStatus.ABROGE).extract_lines(True) == expected


def test_extract_section_lines(legifrance_text: LegifranceText):
    assert legifrance_text.sorted_sections[0].extract_lines(False)[:2] == ['Annexes', 'Annexe I']


def test_split_html():
    assert _split_html('<p>Hello</p>') == ['Hello']
    assert _split_html('<p>Hello</p><p>World <i>!</i></p>') == ['Hello', 'World <i>!</i>']
    input_ = '<p align="left">alpha</p>beta<i>gamma</i><br/><p>delta</p>'
    assert _split_html(input_) == ['alpha', 'beta<i>gamma</i><br/>', 'delta']
