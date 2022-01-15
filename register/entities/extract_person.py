from ..models import Person
from ..models import Firstnames
from typing import List


def extract_person(string):
    string = prepare_person_string(string)
    people = []
    last_name = ''
    for s in string:
        if len(s) < 3:
            continue
        if Firstnames.objects.filter(name=s.upper()):
            p = Person(first_name=s, last_name=last_name)
            people.append(p)
        else:
            last_name = s
            for p in people:
                if len(p.last_name) == 0:
                    p.last_name = s
    return people


def prepare_person_string(string):
    remove_it = ['in.', 'i', 'inni', '']
    sep = string.replace(',', ' ').split(sep=' ')
    # nie spełnia założenia bo set zamienia elementy kolejnościa
    # string = set(string.replace(',', ' ').split(sep=' ')) - remove_it
    return [s for s in sep if s not in remove_it]


# def set_lastnames(people: List[Person]):
#     [p for p in people]


