#!/bin/python3
from __future__ import annotations
import typing

import copy
import time
import os
import random
import sys

os.system("")

import strictyaml as strict_yaml

os.chdir(os.path.dirname(__file__))

import Schemas

class ModronThing:
    def __init__(
        self, file_path: str, *, 
        modron_file_path: str = "./Info/Modrons.yaml", 
        auto_save: int | None = None,
    ):
        self.__file_path = file_path
        self.__auto_save = auto_save
        self.__steps_since_last_save = 0

        with open(modron_file_path, 'r') as file:
            self.__modrons = strict_yaml.load(file.read(), Schemas.modrons_info).data
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                self.__data = strict_yaml.load(file.read(), Schemas.modrons_data).data
        else:
            os.makedirs(os.path.dirname(file_path), exist_ok = True)
            self.__data = {'inv': [], 'wip': []}
    
    def new_modron_by_id(self, id_: str) -> Schemas.modrons_info__modron:
        for modron in self.__modrons:
            if modron['id'] == id_:
                return copy.deepcopy(modron)
        raise NotImplementedError()

    def upgrade(self):
        for item in self.__data['inv']:
            for i in range(item['amount']):
                current_modron = self.new_modron_by_id(item['id'])
                for upgrade in current_modron['upgrades']:
                    if random.random() < upgrade['chances']:
                        self.create(upgrade['next_id'])
                        item['amount'] -= 1
    
    def add_to_inv(self, item_id: str):
        found_item = False
        for item in self.__data['inv']:
            if item['id'] == item_id:
                found_item = True
                item['amount'] += 1
                break
    
        if found_item == False:
            self.__data['inv'].append({
                'id': item_id,
                'amount': 1,
            })
    
    def add_to_wip(self, item_id: str, part_done: float > 0):
        found_item = False
        if not 'wip' in self.__data:
            self.__data['wip'] = []
        for item in self.__data['wip']:
            if item['id'] == item_id:
                found_item = True
                item['part_done'] += part_done
                while item['part_done'] >= 1:
                    item['part_done'] -= 1
                    self.create(item_id, create_upgrades = True)
                break
    
        if found_item == False:
            item = {
                'id': item_id,
                'part_done': part_done % 1,
            }
            self.__data['wip'].append(item)
            while item['part_done'] >= 1:
                item['part_done'] -= 1
                self.create(item_id, create_upgrades = True)

    def create(self, modron_id: str, *, create_upgrades: bool = False):
        self.add_to_inv(modron_id)
        
        if create_upgrades:
            for modron_upgrade in self.new_modron_by_id(modron_id)['upgrades']:
                self.add_to_wip(modron_upgrade['next_id'], modron_upgrade['chances'])
        self.auto_save()
    
    def save(self):
        with open(self.__file_path, 'w') as file:
            file.write(
                strict_yaml.as_document(
                    self.__data, Schemas.modrons_data
                ).as_yaml()
            )
        self.__steps_since_last_save = 0

    def data(self) -> Schemas.modrons_data:
        return copy.deepcopy(self.__data)
    
    def auto_save(self):
        self.__steps_since_last_save += 1
        if self.__steps_since_last_save == self.__auto_save:
            self.save()

if __name__ == "__main__":
    delay = 1
    thing = ModronThing("./Data/progress.yaml")
    while True:
        thing.create('Monodrone', create_upgrades = True)
        
        
        os.system("clear")
        print(
            f"""\u001B[27J{
                strict_yaml.as_document(thing.data(), Schemas.modrons_data).as_yaml()
            }---"""
        )
        print(
            f"""{''
            }delay: {delay}\n{''
            }---"""
        )
        thing.save()
        time.sleep(delay)
        delay += random.random() * random.random()
