#!/bin/python3
from __future__ import annotations
import typing
import os
import sys

os.system("")

from strictyaml import Map, Seq, EmptyDict, EmptyList
from strictyaml import Int, Str, Float
from strictyaml import Optional




modrons_info__modron = Map({
    'id': Str(), 
    Optional('upgrades'): Seq(Map({
        'chances': Float(),
        'next_id': Str(),
    })),
})

modrons_info = Seq(
    modrons_info__modron,
)




modrons_data__inv_item = Map({
    'id': Str(),
    Optional('amount', default = 1): Int()
})

modrons_data__inv = Seq(modrons_data__inv_item) | EmptyList()

modrons_data = Map({
    'inv': modrons_data__inv,
})




if __name__ == "__main__":
    print(
        f"modrons_info = {modrons_info}\n"
        f"modrons_data = {modrons_data}\n"
    )
