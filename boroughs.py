#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A doc string"""

import csv
import json


GRADE_SCALE = {
    'A': 1.00,
    'B': .90,
    'C': .80,
    'D': .70,
    'F': .60,
}


def get_score_summary(filename):
    """A csv import dictionary function.

    Args:
        filename (csv): A comma delimited file.

    Returns:
        Dict: Location, number of stores and grade.

    Examples:
        >>> get_score_summary('inspection_results.csv')
        >>> {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
        (417, 0.9745803357314141), 'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531), 'QUEENS':
        (414, 0.9719806763285017)}
    """

    new_dict = {}
    boro_dict = {}
    finaldict = {}

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['GRADE'] is not '' and row['GRADE'] is not 'P':
                restdict = {row['CAMIS']: {'BORO': row['BORO'],
                                           'GRADE': row['GRADE']}}
                new_dict.update(restdict)

    csvfile.close()

    for camitems in new_dict.itervalues():
        curgrade = GRADE_SCALE[camitems['GRADE']]
        if camitems['BORO'] not in boro_dict:
            boro_dict[camitems['BORO']] = {'count': 1,
                                           'sum_grade': curgrade}
        else:
            boro_dict[camitems['BORO']]['count'] += 1
            boro_dict[camitems['BORO']]['sum_grade'] += curgrade

    for key, data in boro_dict.iteritems():
        avegrade = data['sum_grade'] / data['count']
        finaldict[key] = (data['count'] , avegrade)
    return finaldict 


def get_market_density(filename):
    """A json import dictionary function.

    Args:
        filename (json): A json file.

    Returns:
        Dict: Number of green markets per borough.

    Examples:
        >>> get_market_density('green_markets.json')
        {u'STATEN ISLAND': 2, u'BROOKLYN': 48, u'BRONX': 32,
        u'MANHATTAN': 39, u'QUEENS': 16}
    """
    new_dict = {}
    fhandler = json.loads(open(filename).read())
    newlist = fhandler['data']
    for value in newlist:
        value[8] = value[8].strip() .upper()
        if value[8] not in new_dict:
            new_dict[value[8]] = 1
        else:
            new_dict[value[8]] += 1
    return new_dict


def correlate_data(inspect='inspection_results.csv',
                   green='green_markets.json', last='end.json'):
    """A I/O example.

    Args:
        inspect (csv): default= 'inspection_results.csv'
        green (json): default= 'green_markets.json'
        last (json: default= 'end.json'

    Returns:
        Dict: Boro score and percentage of density.

    Examples:
        >>> get_market_density('green_markets.json')
        {u'STATEN ISLAND': 2, u'BROOKLYN': 48, u'BRONX': 32,
        u'MANHATTAN': 39, u'QUEENS': 16}
    """
    dict3 = {}
    dict1 = get_score_summary(inspect)
    dict2 = get_market_density(green)
    for boro1, value in dict1.iteritems():
        for boro2, greennum in dict2.iteritems():
            if boro2 == boro1:
                endres = float(greennum) / value[0]
            dict3[boro1] = (value[1], endres)
    fhandler = open(last, 'w')
    json.dump(dict3, fhandler)
