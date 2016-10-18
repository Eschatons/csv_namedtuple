# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from collections import namedtuple
import csv
def _set_label_case(labels, case):
    """ helper function to set labels to correct case. """
    if case is None:
        return labels
    try:
        case = case.lower()
    except AttributeError as err:
        raise err("""keyword argument 'case' should be one of 
        the following only: 'lower', 'upper', 'title""")
        
    if case == 'upper':
        return tuple(x.upper() for x in labels)
    elif case == 'lower':
        return tuple(x.lower() for x in labels)
    elif case == 'title':
        return tuple(x.title() for x in labels)
    raise TypeError("""keyword argument 'case' should be one of 
        the following only: 'lower', 'upper', 'title""")

def generate_namedtuples(file, *args, tupleName = 'Column', case = None, **kwargs):
    """ uses the first row of a CSV to yield labeled namedtuples,
    where the labels are taken from the first row of the CSV.
    args and **kwargs are passed through to csv.reader.
    tuplename = name of namedtuple. tupleName = 'Person' --> namedtuple('Person', *args)
    case = case to convert namedtuple _fields. 'upper', 'lower', or 'title'.
    case = 'upper' -->
    
    I.E, if examplefile.csv is as follows:
        'first, last, age'
        'Jim', 'Bob', '32'
        'Steve', 'Carell', '40'
    IN:
        for person in generate_namedtuples('examplefile.csv', tupleName = 'Person', case = 'upper'):
            print person
    OUT:
        Person(FIRST = 'Jim', LAST = 'Bob', AGE = '32')
        Person(FIRST = 'STEVE', LAST = 'CARELL', AGE = '40')
    """
    with open(file) as file:
        reader = csv.reader(file, *args, **kwargs)
        labels = next(reader)
        labels = _set_label_case(labels, case)
        _NamedTuple = namedtuple(tupleName, labels)
        for column in reader:
            if len(column) == 0:
                continue
            yield _NamedTuple(*column)

def write_with_labels(file, namedtuples, *args, case = None, **kwargs):
    """ 
    example code:
    bob = Person(first = 'Bob', last = 'Scorcese', age = 22')
    melissa = Person(first = 'Melissa', last = 'Murdertown', age = 29)
    people = (bob, melissa)
    write_with_labels('testfile.csv, people, case = 'upper')
    --> 
        'FIRST, LAST, AGE'
        'Bob', 'Scorcese', '22'
        'Melissa', 'Murdertown', '29'"""
    rows = iter(namedtuples)
    with open(file, 'w+') as file:
        writer = csv.writer(file, *args, **kwargs)
        firstItem = next(rows)
        labels = firstItem._fields
        labels = _set_label_case(labels, case)
        writer.writerow(firstItem._fields) # write labels
        # start writing data
        writer.writerow(firstItem)
        for row in rows:
            writer.writerow(row)
