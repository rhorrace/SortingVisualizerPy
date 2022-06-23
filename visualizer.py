import random
import time
from tkinter import Button, Canvas, Frame, Label, StringVar, Tk, W, ttk

from colors import *


class Visualizer:
    def __init__(self):
        self.__window = Tk()
        self.__algorithms = ['Bubble Sort', 'Heap Sort', 'Insertion Sort', 'Merge Sort', 'Quick Sort', 'Selection Sort']
        self.__speeds = ['Fast', 'Medium', 'Slow']
        self.__data = []
        self.__size = 0

        self.__UI = Frame(self.__window, width=900, height=300, bg=WHITE)
        self.__UI.grid(row=0, column=0, padx=10, pady=5)

        self.__lblAlgorithm = Label(self.__UI, text="Algorithm: ", bg=WHITE)
        self.__lblAlgorithm.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        self.__drpAlgorithm = ttk.Combobox(self.__UI, textvariable=StringVar(), values=self.__algorithms)
        self.__drpAlgorithm.grid(row=0, column=1, padx=5, pady=5)
        self.__drpAlgorithm.current(0)

        self.__lblSortSpeed = Label(self.__UI, text="Sorting Speed: ", bg=WHITE)
        self.__lblSortSpeed.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        self.__drpSortSpeed = ttk.Combobox(self.__UI, textvariable=StringVar(), values=self.__speeds)
        self.__drpSortSpeed.grid(row=1, column=1, padx=5, pady=5)
        self.__drpSortSpeed.current(0)

        self.__btnSort = Button(self.__UI, text="Sort", command=self.__sort, bg=LIGHT_GRAY)
        self.__btnSort.grid(row=2, column=1, padx=5, pady=5)

        # button for generating array
        self.__btnGenerate = Button(self.__UI, text="Generate Array", command=self.__generate, bg=LIGHT_GRAY)
        self.__btnGenerate.grid(row=2, column=0, padx=5, pady=5)

        # canvas to draw our array
        self.__canvas = Canvas(self.__window, width=800, height=400, bg=WHITE)
        self.__canvas.grid(row=1, column=0, padx=10, pady=5)

    def main_loop(self):
        self.__window.mainloop()

    def __draw_data(self, color_array):
        self.__canvas.delete("all")
        canvas_width = 800
        canvas_height = 400
        x_width = canvas_width / (len(self.__data) + 1)
        offset = 4
        spacing = 2
        max_data = max(self.__data)
        normalized_data = list(map(lambda x: x / max_data, self.__data))

        for i, height in enumerate(normalized_data):
            x0 = i * x_width + offset + spacing
            y0 = canvas_height - height * 390
            x1 = (i + 1) * x_width + offset
            y1 = canvas_height
            self.__canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])

        self.__window.update_idletasks()

    def __generate(self):
        self.__data = random.sample(range(1, 151), 150)
        self.__size = len(self.__data)

        self.__draw_data([BLUE] * len(self.__data))

    def __set_speed(self):
        if self.__drpSortSpeed.get() == 'Slow':
            return 0.3
        elif self.__drpSortSpeed.get() == 'Medium':
            return 0.1
        else:
            return 0.01

    def __sort(self):
        time_tick = self.__set_speed()

        if self.__drpAlgorithm.get() == 'Bubble Sort':
            self.__bubble_sort(time_tick)

        elif self.__drpAlgorithm.get() == 'Heap Sort':
            self.__heap_sort(time_tick)

        elif self.__drpAlgorithm.get() == 'Insertion Sort':
            self.__insertion_sort(time_tick)

        elif self.__drpAlgorithm.get() == 'Merge Sort':
            self.__merge_sort(0, self.__size - 1, time_tick)

        elif self.__drpAlgorithm.get() == 'Quick Sort':
            self.__quick_sort(0, self.__size - 1, time_tick)

        elif self.__drpAlgorithm.get() == 'Selection Sort':
            self.__selection_sort(time_tick)

    # Sorts

    # Bubble Sort
    def __bubble_sort(self, time_tick):
        swapped = False
        for n in range(self.__size - 1, 0, -1):
            for i in range(n):
                if self.__data[i] <= self.__data[i + 1]:
                    continue

                swapped = True
                self.__data[i], self.__data[i + 1] = self.__data[i + 1], self.__data[i]
                self.__draw_data([YELLOW if x == i or x == i + 1 else BLUE for x in range(self.__size)])
                time.sleep(time_tick)

            if not swapped:
                break

        self.__draw_data([BLUE] * self.__size)

    # Heap Sort
    def __heap_sort(self, time_tick):
        for i in range(self.__size // 2 - 1, -1, -1):
            self.__heapify(self.__size, i, time_tick)

        for i in range(self.__size - 1, 0, -1):
            self.__draw_data([YELLOW if x == i else BLUE for x in range(self.__size)])
            time.sleep(time_tick)

            self.__data[i], self.__data[0] = self.__data[0], self.__data[i]
            self.__heapify(i, 0, time_tick)

        self.__draw_data([BLUE] * self.__size)

    def __heapify(self, n, i, time_tick):
        largest = i
        lt = 2 * i + 1
        rt = 2 * i + 2

        if lt < n and self.__data[largest] < self.__data[lt]:
            largest = lt

        if rt < n and self.__data[largest] < self.__data[rt]:
            largest = rt

        if largest != i:
            self.__draw_data([YELLOW if x == largest else BLUE for x in range(self.__size)])
            time.sleep(time_tick)

            self.__data[i], self.__data[largest] = self.__data[largest], self.__data[i]

            self.__heapify(n, largest, time_tick)

    # Insertion Sort
    def __insertion_sort(self, time_tick):
        for i in range(1, self.__size):
            key = self.__data[i]
            j = i - 1

            while j >= 0 and self.__data[j] > key:
                self.__draw_data([YELLOW if x == j or x == j + 1 else BLUE for x in range(self.__size)])
                self.__data[j + 1] = self.__data[j]
                j -= 1

            self.__draw_data([YELLOW if x == j + 1 else BLUE for x in range(self.__size)])
            time.sleep(time_tick)

            self.__data[j + 1] = key

            self.__draw_data([BLUE] * self.__size)

    # Merge Sort
    def __merge_sort(self, start, end, time_tick):
        if start < end:
            mid = start + (end - start) // 2
            self.__merge_sort(start, mid, time_tick)
            self.__merge_sort(mid + 1, end, time_tick)

            self.__merge(start, mid, end, time_tick)

            time.sleep(time_tick)

        self.__draw_data([BLUE] * self.__size)

    def __merge(self, start, mid, end, time_tick):
        arr1 = self.__data[start:mid + 1]
        arr2 = self.__data[mid + 1:end + 1]

        i, j, k = 0, 0, start
        n1, n2 = len(arr1), len(arr2)

        while i < n1 and j < n2:
            self.__draw_data([YELLOW if x == k else BLUE for x in range(self.__size)])
            time.sleep(time_tick)

            if arr1[i] < arr2[j]:
                self.__data[k] = arr1[i]
                i += 1
            else:
                self.__data[k] = arr2[j]
                j += 1

            k += 1

        while i < n1:
            self.__draw_data([YELLOW if x == k else BLUE for x in range(self.__size)])
            time.sleep(time_tick)

            self.__data[k] = arr1[i]
            i += 1
            k += 1

        while j < n2:
            self.__draw_data([YELLOW if x == k else BLUE for x in range(self.__size)])
            time.sleep(time_tick)

            self.__data[k] = arr2[j]
            j += 1
            k += 1

    # Quick Sort
    def __quick_sort(self, low, high, time_tick):
        if low < high:
            pi = self.__partition(low, high, time_tick)

            self.__quick_sort(low, pi - 1, time_tick)
            self.__quick_sort(pi + 1, high, time_tick)

        self.__draw_data([BLUE] * self.__size)

    def __partition(self, low, high, time_tick):
        pivot = self.__data[high]

        i = low - 1

        for j in range(low, high):
            if self.__data[j] <= pivot:
                self.__draw_data([YELLOW if x == j else BLUE for x in range(self.__size)])
                time.sleep(time_tick
                           )
                i += 1

                self.__data[i], self.__data[j] = self.__data[j], self.__data[i]

        self.__draw_data([YELLOW if x == i + 1 else BLUE for x in range(self.__size)])
        time.sleep(time_tick)

        self.__data[i + 1], self.__data[high] = self.__data[high], self.__data[i + 1]

        return i + 1

    # Selection Sort
    def __selection_sort(self, time_tick):
        size = len(self.__data)

        for i in range(size):
            min_idx = i
            for j in range(i + 1, size):
                self.__draw_data([YELLOW if x == j else BLUE for x in range(size)])

                if self.__data[min_idx] <= self.__data[j]:
                    continue

                min_idx = j

            self.__data[i], self.__data[min_idx] = self.__data[min_idx], self.__data[i]

        self.__draw_data([BLUE] * size)
