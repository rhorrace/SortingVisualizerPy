import random
import time
from tkinter import Button, Canvas, Frame, Label, StringVar, Tk, W, ttk

from colors import *


class Visualizer:
    def __init__(self):
        self.__window = Tk()
        self.__algorithms = ['Bitonic Sort', 'Bubble Sort', 'Comb Sort', 'Cycle Sort', 'Gnome Sort',
                             'Heap Sort', 'Insertion Sort', 'Merge Sort', 'Quick Sort', 'Selection Sort',
                             'Shell Sort']
        self.__speeds = ['Fast', 'Medium', 'Slow']
        self.__data = []
        self.__size = 0
        self.__tick = 0.0

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
        self.__data = random.sample(range(1, 129), 128)
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
        self.__time_tick = self.__set_speed()

        match self.__drpAlgorithm.get():
            case 'Bitonic Sort':
                self.__bitonic_sort(0, self.__size, 1)
            case 'Bubble Sort':
                self.__bubble_sort()
            case 'Comb Sort':
                self.__comb_sort()
            case 'Cycle Sort':
                self.__cycle_sort()
            case 'Gnome Sort':
                self.__gnome_sort()
            case 'Heap Sort':
                self.__heap_sort()
            case 'Insertion Sort':
                self.__insertion_sort()
            case 'Merge Sort':
                self.__merge_sort(0, self.__size - 1)
            case 'Quick Sort':
                self.__quick_sort(0, self.__size - 1)
            case 'Selection Sort':
                self.__selection_sort()
            case 'Shell Sort':
                self.__shell_sort()

    # Sorts

    # Bitonic Sort
    def __bitonic_sort(self, low, cnt, dire):
        if cnt > 1:
            k = cnt // 2

            self.__bitonic_sort(low, k, 1)
            self.__bitonic_sort(low + k, k, 0)
            self.__bitonic_merge(low, cnt, dire)

        self.__draw_data([BLUE] * self.__size)

    def __bitonic_merge(self, low, cnt, dire):
        if cnt > 1:
            k = cnt // 2

            for i in range(low, low + k):
                self.__comp_and_swap(i, i + k, dire)

            self.__bitonic_merge(low, k, dire)
            self.__bitonic_merge(low + k, k, dire)

    def __comp_and_swap(self, i, j, dire):
        if (dire == 1 and self.__data[i] > self.__data[j]) or (dire == 0 and self.__data[i] < self.__data[j]):
            self.__data[i], self.__data[j] = self.__data[j], self.__data[i]

            self.__draw_data([YELLOW if x == i or x == j else BLUE for x in range(self.__size)])
            time.sleep(self.__time_tick)

    # Bubble Sort
    def __bubble_sort(self):
        swapped = False
        for n in range(self.__size - 1, 0, -1):
            for i in range(n):
                if self.__data[i] > self.__data[i + 1]:
                    self.__data[i], self.__data[i + 1] = self.__data[i + 1], self.__data[i]
                    swapped = True

                # Update graph
                self.__draw_data([YELLOW if x == i + 1 else BLUE for x in range(self.__size)])
                time.sleep(self.__time_tick)

            if not swapped:
                break

        # Update graph
        self.__draw_data([BLUE] * self.__size)

    # Comb Sort
    def __comb_sort(self):
        def pick_color(x, idx, gp):
            return YELLOW if x == idx else PURPLE if x == idx + gp else BLUE

        gap = self.__size
        swapped = True

        while gap != 1 or swapped:
            gap = self.__get_next_gap(gap)
            swapped = False

            for i in range(0, self.__size - gap):
                if self.__data[i] > self.__data[i + gap]:
                    self.__data[i], self.__data[i + gap] = self.__data[i + gap], self.__data[i]
                    swapped = True

                # Update graph
                self.__draw_data([pick_color(x, i, gap) for x in range(self.__size)])
                time.sleep(self.__time_tick)

        # Update graph
        self.__draw_data([BLUE] * self.__size)

    @staticmethod
    def __get_next_gap(gap):
        gap = (gap * 10) // 13

        return 1 if gap < 1 else gap

    # Cycle Sort
    def __cycle_sort(self):
        def pick_color(x, idx, strt):
            return YELLOW if x == idx else PURPLE if x == strt else BLUE

        for start in range(0, self.__size - 1):
            item = self.__data[start]

            pos = start

            for i in range(start + 1, self.__size):
                if self.__data[i] < item:
                    pos += 1

            if pos == start:
                continue

            while item == self.__data[pos]:
                pos += 1

            self.__data[pos], item = item, self.__data[pos]

            # Update graph
            self.__draw_data([pick_color(x, pos, start) for x in range(self.__size)])
            time.sleep(self.__time_tick)

            while pos != start:
                pos = start

                for i in range(start + 1, self.__size):
                    if self.__data[i] < item:
                        pos += 1

                while item == self.__data[pos]:
                    pos += 1

                self.__data[pos], item = item, self.__data[pos]

                # Update graph
                self.__draw_data([pick_color(x, pos, start) for x in range(self.__size)])
                time.sleep(self.__time_tick)

        # Update graph
        self.__draw_data([BLUE] * self.__size)

    # Gnome Sort
    def __gnome_sort(self):
        index = 0

        while index < self.__size:
            if index == 0:
                index += 1

            if self.__data[index] >= self.__data[index - 1]:
                index += 1
            else:
                self.__data[index], self.__data[index - 1] = self.__data[index - 1], self.__data[index]

                # Update graph
                self.__draw_data([YELLOW if x == index else BLUE for x in range(self.__size)])
                time.sleep(self.__time_tick)

                index -= 1

        # Update graph
        self.__draw_data([BLUE] * self.__size)

    # Heap Sort
    def __heap_sort(self):
        for i in range(self.__size // 2 - 1, -1, -1):
            self.__heapify(self.__size, i)

        for i in range(self.__size - 1, 0, -1):
            self.__data[i], self.__data[0] = self.__data[0], self.__data[i]

            # Update graph
            self.__draw_data([YELLOW if x == i else BLUE for x in range(self.__size)])
            time.sleep(self.__time_tick)

            self.__heapify(i, 0)

        # Update graph
        self.__draw_data([BLUE] * self.__size)

    def __heapify(self, n, i):
        largest = i
        lt = 2 * i + 1
        rt = 2 * i + 2

        if lt < n and self.__data[largest] < self.__data[lt]:
            largest = lt

        if rt < n and self.__data[largest] < self.__data[rt]:
            largest = rt

        if largest == i:
            return

        self.__data[i], self.__data[largest] = self.__data[largest], self.__data[i]

        # Update graph
        self.__draw_data([YELLOW if x == i else BLUE for x in range(self.__size)])
        time.sleep(self.__time_tick)

        self.__heapify(n, largest)

    # Insertion Sort
    def __insertion_sort(self):
        for i in range(1, self.__size):
            key = self.__data[i]
            j = i - 1

            while j >= 0 and self.__data[j] > key:
                self.__data[j + 1], self.__data[j] = self.__data[j], self.__data[j + 1]

                # Update graph
                self.__draw_data([YELLOW if x == j else BLUE for x in range(self.__size)])
                time.sleep(self.__time_tick)

                j -= 1

            self.__data[j + 1] = key

            # Update graph
            self.__draw_data([BLUE] * self.__size)

    # Merge Sort
    def __merge_sort(self, start, end):
        if start < end:
            mid = start + (end - start) // 2
            self.__merge_sort(start, mid)
            self.__merge_sort(mid + 1, end)

            self.__merge(start, mid, end)

            time.sleep(self.__time_tick)

        # Update graph
        self.__draw_data([BLUE] * self.__size)

    def __merge(self, start, mid, end):
        arr1 = self.__data[start:mid + 1]
        arr2 = self.__data[mid + 1:end + 1]

        i, j, k = 0, 0, start
        n1, n2 = len(arr1), len(arr2)

        while i < n1 and j < n2:
            # Update graph
            self.__draw_data([YELLOW if x == k else BLUE for x in range(self.__size)])
            time.sleep(self.__time_tick)

            if arr1[i] < arr2[j]:
                self.__data[k] = arr1[i]
                i += 1
            else:
                self.__data[k] = arr2[j]
                j += 1

            k += 1

        while i < n1:
            # Update graph
            self.__draw_data([YELLOW if x == k else BLUE for x in range(self.__size)])
            time.sleep(self.__time_tick)

            self.__data[k] = arr1[i]
            i += 1
            k += 1

        while j < n2:
            # Update graph
            self.__draw_data([YELLOW if x == k else BLUE for x in range(self.__size)])
            time.sleep(self.__time_tick)

            self.__data[k] = arr2[j]
            j += 1
            k += 1

    # Quick Sort
    def __quick_sort(self, low, high):
        if low < high:
            pi = self.__partition(low, high)

            self.__quick_sort(low, pi - 1)
            self.__quick_sort(pi + 1, high)

        # Update graph
        self.__draw_data([BLUE] * self.__size)

    def __partition(self, low, high):
        pivot = self.__data[high]

        i = low - 1

        for j in range(low, high):
            if self.__data[j] > pivot:
                continue

            # Update graph
            self.__draw_data([YELLOW if x == j else BLUE for x in range(self.__size)])
            time.sleep(self.__time_tick)

            i += 1

            self.__data[i], self.__data[j] = self.__data[j], self.__data[i]

        self.__data[i + 1], self.__data[high] = self.__data[high], self.__data[i + 1]

        # Update graph
        self.__draw_data([YELLOW if x == i + 1 else BLUE for x in range(self.__size)])
        time.sleep(self.__time_tick)

        return i + 1

    # Selection Sort
    def __selection_sort(self):
        for i in range(self.__size):
            min_idx = i
            for j in range(i + 1, self.__size):
                if self.__data[min_idx] <= self.__data[j]:
                    continue

                min_idx = j

            # Update graph
            self.__draw_data([YELLOW if x == min_idx else BLUE for x in range(self.__size)])
            time.sleep(self.__time_tick)

            self.__data[i], self.__data[min_idx] = self.__data[min_idx], self.__data[i]

        # Update graph
        self.__draw_data([BLUE] * self.__size)

    # Shell Sort
    def __shell_sort(self):
        def pick_color(x, idx, gp):
            return YELLOW if x == idx else PURPLE if x == idx + gp else BLUE

        gap = self.__size // 2

        while gap > 0:
            j = gap

            while j < self.__size:
                i = j - gap

                while i >= 0:
                    if self.__data[i + gap] > self.__data[i]:
                        break

                    self.__data[i + gap], self.__data[i] = self.__data[i], self.__data[i + gap]

                    # Update graph
                    self.__draw_data(
                        [pick_color(x, i, gap) for x in range(self.__size)])
                    time.sleep(self.__time_tick)

                    i -= gap

                j += 1

            gap //= 2

        # Update graph
        self.__draw_data([BLUE] * self.__size)
