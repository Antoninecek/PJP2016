# -*- coding: utf-8 -*-
"""
Na vstupu jsou dány 3 sekvence. Každá z nich obsahuje několik uspořádaných
dvojic uložených jako tuple (id, count).
Sekvence může tedy vypadat například takto: ((1, 3), (3, 4), (10, 2)).
První prvek sekvence je tedy tuple s hodnotami  id = 1 je count = 3 a tak dále.
Vaším úkolem je spojit tyto tři sekvence do jednoho slovníku. Ten bude výstupem z programu.

Položky slovníku budou v následujícím tvaru {id: [A, B, C]},
kde A, B a C jsou hodnoty pro příslušné ID v první, druhé a třetí sekvenci.

Ovšem pozor - neplatí, že každé id je obsaženo ve všech sekvencích.
Může být ve všech, ve dvou, nebo pouze v jedné.

Tady máte konkrétní příklad. Zadané sekvence mají následující podobu:

line_a = ((1, 3), (3, 4), (10, 2))
line_b = ((1, 2), (2, 4), (5, 2))
line_c = ((1, 5), (3, 2), (7, 3))

Transformací musí vzniknout následující slovník:

{1: [3, 2, 5],
 2: [0, 4, 0],
 3: [4, 0, 2],
 5: [0, 2, 0],
 7: [0, 0, 3],
10: [2, 0, 0]}
"""

from collections import defaultdict


def merge_tuples(*lines):
    """
    funkce merge tuples - spojujici sekvence
    """
    out_dict = defaultdict(lambda: [0, ] * len(lines))
    for i, k in enumerate(lines):
        for j in k:
            out_dict[j[0]][i] = j[1]
    return out_dict


# pylint: disable=C0103
# BECAUS line_x is not a constant
if __name__ == '__main__':
    line_a = ((1, 3), (3, 4), (10, 2), (11, 3))
    line_b = ((1, 2), (2, 4), (5, 2))
    line_c = ((1, 5), (3, 2), (7, 3))
    line_d = ((1, -1), (11, -1), (3, -1), (7, -1))
    assert merge_tuples(line_a, line_b, line_c, line_d)
