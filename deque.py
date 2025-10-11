#!/usr/bin/env python
from gvanim import Animation
import inspect


class MinHeap:
    def __init__(self, ls):
        self.ls = ls
        self.heapsize = 0
        self.length = len(ls)
        self.animator = Animation()
        self.clean_animation()

    def __getitem__(self, i):
        if not i < self.length:
            return None
        return self.ls[i]

    def __setitem__(self, i, val):
        self.ls[i] = val

    def __repr__(self):
        return f'MinHeap: {self.ls}, heapsize: {self.heapsize}'

    def heap_prop(self, i) -> (bool, int | None):
        li = self._left(i)
        ri = self._right(i)
        min = i
        if li and not self[i] <= self[li]:
            min = li
        if ri and not self[min] <= self[ri]:
            min = ri
        return (min == i, min)

    def minheapify(self, i):
        '''
        bubbledown
        '''
        ok, min = self.heap_prop(i)
        if not ok:
            assert min
            swap(self, min, i)
            self.minheapify(min)

    def build_min_heap(self):
        if self.animator.steps():
            self.animator = Animation()
        self.heapsize = self.length
        for i in reversed(range(0, self.length)):
            self.minheapify(i)
        print(f'Op: {inspect.currentframe().f_code.co_name}, {self}')

    def bubbleup(self, i):
        p = self._parent(i)
        ok, min = self.heap_prop(p)
        if not ok:
            assert min
            swap(self, p, min)
            self.bubbleup(p)

    def insert(self, val):
        self.ls.append(val)
        self.length += 1
        self.bubbleup(self.length-1)
        self.heapsize += 1
        print(f'Op: {inspect.currentframe().f_code.co_name}, {self}')

    def delete(self, i):
        swap(self, i, self.length-1)
        self.ls = self.ls[:-1]
        self.length = len(self.ls)
        p = self._parent(i)
        ok, min = self.heap_prop(p)
        if not ok:
            assert min
            self.bubbleup(i)
        else:
            self.minheapify(i)
        self.heapsize = self.length
        print(f'Op: {inspect.currentframe().f_code.co_name}, {self}')

    def clean_animation(self):
        self.animator.next_step(clean=True)
        for i, v in enumerate(self.ls):
            i += 1
            self.animator.label_node(i, label=v)
            p = self._parent(i)
            if p and i != p:
                self.animator.add_edge(p, i)

    def _left(self, i) -> int | None:
        idx = (i) * 2
        return idx if idx < self.length else None

    def _right(self, i) -> int | None:
        idx = i * 2 + 1
        return idx if idx < self.length else None

    def _parent(self, i) -> int | None:
        idx = (i) // 2
        return idx if idx < self.length else None


def swap(heap, i, j, delete_edges=False):
    temp = heap[i]
    heap[i] = heap[j]
    heap[j] = temp
    if heap.animator:
        heap.clean_animation()
        heap.animator.highlight_edge(j+1, i+1, color='green')
