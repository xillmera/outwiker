# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import json
import logging
from collections import MutableMapping

from .registry import Registry
from .defines import REGISTRY_SECTION_PAGES
from outwiker.utilites.textfile import readTextFile, writeTextFile

logger = logging.getLogger('outwiker.core.notestreeregistry')


class BaseSaver(object, metaclass=ABCMeta):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self, items_dict):
        pass


class JSONSaver(BaseSaver):
    def __init__(self, fname):
        self._fname = fname

    def load(self):
        try:
            text = readTextFile(self._fname)
            items = json.loads(text)
        except (IOError, json.JSONDecodeError):
            logger.error('Error reading a notes tree registry')
            items = {}

        return items

    def save(self, items):
        text = json.dumps(items)
        try:
            writeTextFile(self._fname, text)
        except IOError:
            logger.error('Error saving a notes tree registry')


class NotesTreeRegistry(Registry):
    def __init__(self, saver):
        '''
        saver - interface with two methods - save() and load().
        '''
        self._saver = saver
        self._version = 1
        self._VERSION_OPTION = '__version'

        items = saver.load()

        if items.get(self._VERSION_OPTION, None) != self._version:
            logger.warning('Invalid notes tree registry version')
            items = {}

        if not isinstance(items, MutableMapping):
            logger.error('Invalid notes tree registry format')
            items = {}

        items[self._VERSION_OPTION] = self._version
        super().__init__(items)

    def save(self):
        self._saver.save(self._items)

    def _get_pages_section(self):
        try:
            subregistry = self.get_subregistry(REGISTRY_SECTION_PAGES)
        except KeyError:
            self._items[REGISTRY_SECTION_PAGES] = {}
            subregistry = self.get_subregistry(REGISTRY_SECTION_PAGES)

        return subregistry

    def get_section_or_create(self, *path_elements):
        path_elements_list = list(path_elements[:])
        parent = self._items

        while path_elements_list:
            next = path_elements_list.pop(0)
            if next not in parent or not self._is_section(parent[next]):
                parent[next] = {}

            parent = parent[next]

        return Registry(parent)

    def get_page_registry(self, page):
        return self.get_section_or_create(REGISTRY_SECTION_PAGES, page.subpath)