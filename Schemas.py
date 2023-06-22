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


class Part(Float):
    def validate_scalar(self, chunk):
        result = Float.validate_scalar(self, chunk)
        if 0.0 <= result:
            return result
        chunk.expecting_but_found("when expecting a float that is 0.0 or bigger")

modrons_data__inv_item = Map({
    'id': Str(),
    Optional('amount', default = 1): Int(),
})

modrons_data__inv = Seq(modrons_data__inv_item) | EmptyList()

modrons_data__wip_item = Map({
    'id': Str(),
    'part_done': Part(),
})

modrons_data__wip = Seq(modrons_data__wip_item) | EmptyList()

modrons_data = Map({
    'inv': modrons_data__inv,
    Optional('wip'): modrons_data__wip,
})




if __name__ == "__main__":
    print(
        f"modrons_info = {modrons_info}\n"
        f"modrons_data = {modrons_data}\n"
    )
