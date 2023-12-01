import pymorphy2
from enum import Enum


class Inflect(Enum):
    """
    Падежи для склонения
    """
    nomn = 'nomn'
    gent = 'gent'
    datv = 'datv'
    accs = 'accs'
    ablt = 'ablt'
    loct = 'loct'
    voct = 'voct'
    gen2 = 'gen2'
    acc2 = 'acc2'
    loc2 = 'loc2'


morph = pymorphy2.MorphAnalyzer()


def inflect_collocation(collocation: str, inflect: Inflect):
    words = [morph.parse(word)[0].inflect({inflect.value}).word for word in collocation.split()]
    return ' '.join(words)
