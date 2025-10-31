#!/usr/bin/env python

from abc import ABC, abstractmethod
from enum import Enum


class Heap(ABC):
    class SortOrder(Enum):
        ASC = 0
        DSC = 1

    @abstractmethod
    def heap_property(self, i):
        ...

    @abstractmethod
    def classname(self):
        ...

    def __init__(self, ls):
        self.ls = ls
        self.length = len(ls)
        self.heapsize = 1

    def __getitem__(self, i):
        return self.ls[i]

    def __setitem__(self, i, v):
        self.ls[i] = v

    def __repr__(self):
        return f'{self.classname()} {self.ls}, heapsize={self.heapsize}'

    def left(self, i) -> int | None:
        idx = (i+1) * 2 - 1
        return idx if idx < self.length else None

    def right(self, i) -> int | None:
        l = self.left(i)
        idx = l + 1 if l else None
        return idx if idx and idx < self.length else None

    def parent(self, i) -> int | None:
        idx = (i+1) // 2 - 1
        return idx if idx > -1 and idx < self.length else None

    def swap(self, i, j):
        temp = self[i]
        self[i] = self[j]
        self[j] = temp

    def heapify(self, i):
        '''
        Bubble down, assuming all subtrees are heaps
        that abide by self.heap_property
        '''
        ok, idx = self.heap_property(i)
        if not ok:
            self.swap(idx, i)
            self.heapify(idx)

    def build(self):
        ''' Heapify the first half of self.ls

        It would be redundant to do it for the second half, since the last
        level of the tree is already heaps.

        Do it descendingly, so as to always start adjacent to known heaps.
        '''
        self.heapsize = self.length
        for i in reversed(range(0, self.length // 2)):
            self.heapify(i)

    def sort(self):
        '''reduce heapsize to 1 by reordering all elements'''
        self.build()
        self.heapsize = 1
        for i in reversed(range(1, self.length)):
            self.swap(0, i)
            self.heapify(0)

    def bubble_up(self, i):
        p = self.parent(i)
        ok, idx = self.heap_property(p)
        if not ok:
            self.swap(i, p)
            self.bubble_up(p)

    def insert(self, v):
        self.ls.append(v)
        self.bubble_up(v)

    def delete(self, i):
        self.swap(self.length-1, i)
        self.ls = self[:-1]
        self.length = len(self.ls)
        p = self.parent(i)
        ok, idx = self.heap_property(p)
        if not ok:
            self.bubble_up(idx)
        else:
            self.heapify(idx)
        self.heapsize = self.length


class MaxHeap(Heap):
    def classname(self):
        return self.__class__.__name__

    def heap_property(self, i):
        l = self.left(i)
        r = self.right(i)
        idx = i
        if l and not self[idx] >= self[l]:
            idx = l
        if r and not self[idx] >= self[r]:
            idx = r
        return (idx == i, idx)
    ...


class MinHeap(Heap):
    def classname(self):
        return self.__class__.__name__

    def heap_property(self, pi):
        l = self.left(pi)
        r = self.right(pi)
        idx = pi
        if l and not self[idx] <= self[l]:
            idx = l
        if r and not self[idx] <= self[r]:
            idx = r
        return (idx == pi, idx)
    ...
