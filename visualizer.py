import random
import time
from tkinter import Button, Canvas, Frame, Label, StringVar, Tk, W, ttk

from colors import *


class Visualizer:
    def __init__(self):
        self.__window = Tk()
        self.__algorithms = ['Bubble Sort', 'Merge Sort']
        self.__speeds = ['Fast', 'Medium', 'Slow']
        self.__data = []

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
        self.__data = []
        for i in range(0, 100):
            random_value = random.randint(1, 150)
            self.__data.append(random_value)

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

        elif self.__drpAlgorithm.get() == 'Merge Sort':
            self.__merge_sort(0, len(self.__data) - 1, time_tick)

    # Sorts

    def __bubble_sort(self, time_tick):
        size = len(self.__data)
        for i in range(size - 1):
            for j in range(size - i - 1):
                if self.__data[j] > self.__data[j + 1]:
                    self.__data[j], self.__data[j + 1] = self.__data[j + 1], self.__data[j]
                    self.__draw_data([YELLOW if x == j or x == j + 1 else BLUE for x in range(len(self.__data))])
                    time.sleep(time_tick)

        self.__draw_data([BLUE] * size)

    def __merge_sort(self, start, end, time_tick):
        def pick_color(x, s, m, e):
            if s <= x < m:
                return PURPLE
            if x == m:
                return YELLOW
            if mid < x <= e:
                return DARK_BLUE
            return BLUE

        if start < end:
            mid = start + (end - start) // 2
            self.__merge_sort(start, mid, time_tick)
            self.__merge_sort(mid + 1, end, time_tick)

            self.__merge(start, mid, end)

            self.__draw_data([pick_color(x, start, mid, end) for x in range(len(self.__data))])
            time.sleep(time_tick)

        self.__draw_data([BLUE] * len(self.__data))

    def __merge(self, start, mid, end):
        arr1 = self.__data[start:mid+1]
        arr2 = self.__data[mid+1:end]

        i, j, k = 0, 0, start
        n1, n2 = len(arr1), len(arr2)

        while i < n1 and j < n2:
            if arr1[i] <= arr2[j]:
                self.__data[k] = arr1[i]
                i += 1
            else:
                self.__data[k] = arr2[j]
                j += 1

            k += 1

        while i < n1:
            self.__data[k] = arr1[i]
            i += 1
            k += 1

        while j < n2:
            self.__data[k] = arr2[j]
            j += 1
            k += 1
