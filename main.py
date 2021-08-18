# autor: Jakub Więcek
# 18.08.2021r
import tkinter
from tkinter import *
from tkinter import messagebox
import os

from datetime import datetime
from datetime import timedelta

ROOT_HEIGHT = 400
ROOT_WIDTH = 600
BG_COLOR = "bisque"
FONT = "ARIAL"


class App:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry(str(ROOT_WIDTH) + 'x' + str(ROOT_HEIGHT))
        self.root.resizable(width=False, height=False)
        self.root.configure(bg=BG_COLOR)
        self.labelTitle = Label(self.root, text="AUTOMATYCZNE WYLĄCZANIE KOMPUTERA", font=(FONT, 19), bg=BG_COLOR)
        self.labelTitle.place(relx=0.5, rely=0.08, anchor=CENTER)
        self.buttonExit = Button(self.root, text="Wyjście", pady=15, width=20, fg="white", bg="green",
                                 command=self.quit)
        self.buttonExit.place(x=50, y=320)

    def quit(self):
        self.root.destroy()


class InputWindow(App):
    def __init__(self):
        super().__init__()
        self.timeChoice = IntVar()

        Radiobutton(self.root, text="WPISZ CZAS DO WYLĄCZENIA KOMPUTERA", variable=self.timeChoice, value=0,
                    bg=BG_COLOR).place(x=15, y=80)

        self.buttonRun = Button(self.root, text="Włącz odliczanie", pady=15, width=22, fg="white", bg="green",
                                command=self.click)
        self.buttonRun.place(x=380, y=320)
        self.CountObject = None
        self.InputObject = None
        self.labelHour1 = Label(self.root, text="GODZIN: ", bg=BG_COLOR)
        self.labelHour1.place(x=15, y=ROOT_HEIGHT / 3)
        self.entryHour1 = Entry(self.root, width=5, borderwidth=3)
        self.entryHour1.insert(0, "0")
        self.entryHour1.place(x=ROOT_WIDTH / 6.5, y=ROOT_HEIGHT / 3)
        self.labelMinute1 = Label(self.root, text="MINUT: ", bg=BG_COLOR).place(x=ROOT_WIDTH / 4, y=ROOT_HEIGHT / 3)
        self.entryMinute1 = Entry(self.root, width=5, borderwidth=3)
        self.entryMinute1.insert(0, "0")
        self.entryMinute1.place(x=ROOT_WIDTH / 2.9, y=ROOT_HEIGHT / 3)

        MODES = ["Twarde wyłączenie komputera", "Wyłącz komputer", "Uruchom Ponownie", "Wyloguj", "Hibernacja"]
        self.modeChoice = IntVar()
        i = 0
        for text in MODES:
            Radiobutton(self.root, text=text, variable=self.modeChoice, value=i, bg=BG_COLOR) \
                .place(x=ROOT_WIDTH / 1.5, y=120 + i * 25)
            i += 1

        Radiobutton(self.root, text="WPISZ GODZINĘ WYLĄCZENIA KOMPUTERA", variable=self.timeChoice, value=1,
                    bg=BG_COLOR).place(x=15, y=200)
        self.labelHour2 = Label(self.root, text="GODZIA: ", bg=BG_COLOR).place(x=15, y=240)
        self.entryHour2 = Entry(self.root, width=5, borderwidth=3)
        self.entryHour2.insert(0, "0")
        self.entryHour2.place(x=93, y=240)
        self.labelMinute2 = Label(self.root, text="MINUTA: ", bg=BG_COLOR).place(x=150, y=240)
        self.entryMinute2 = Entry(self.root, width=5, borderwidth=3)
        self.entryMinute2.insert(0, "0")
        self.entryMinute2.place(x=220, y=240)
        self.root.mainloop()

    def click(self):
        if self.timeChoice.get() == 0:
            return self.click1()
        if self.timeChoice.get() == 1:
            self.click2()

    def click1(self):
        try:
            hour = int(self.entryHour1.get())
            minute = int(self.entryMinute1.get())
            if hour < 0 or minute < 0 or (hour == 0 and minute == 0) or hour > 23 or minute > 59:
                messagebox.showwarning(title="Błąd", message="Wpisaną błędną wartość")
                return

            self.root.destroy()
            self.CountObject = Couting(hour, minute, 0, self.modeChoice.get(), self.InputObject)
        except ValueError:
            messagebox.showwarning(title="Błąd", message="Podana wartość nie jest liczba")
            return

    def click2(self):
        try:
            hour = int(self.entryHour2.get())
            minute = int(self.entryMinute2.get())
            if hour < 0 or minute < 0 or (hour == 0 and minute == 0) or hour > 23 or minute > 59:
                messagebox.showwarning(title="Błąd", message="Wpisaną błędną wartość")
                return
            self.root.destroy()
            self.CountObject = Couting(hour, minute, 1, self.modeChoice.get(), self.InputObject)
        except ValueError:
            messagebox.showwarning(title="Błąd", message="Podana wartość nie jest liczba")
            return

    def __del__(self):
        print("Usunieto input_window")

    def loop(self):
        self.root.mainloop()


class Couting(App):
    def __init__(self, hour, minute, timeChoice, modeChoice, inputObject):
        super().__init__()
        self.InputObject = inputObject
        self.timeNow = datetime.now()
        self.timeEnd = IntVar()
        self.modeChoice = modeChoice
        self.drawTimeToEndActive = None
        # 0 oznacza czas za ile zostanie wyłączony komputer a 1 oznacza godzinę o której zostanie wyłączony komputer
        self.timeChoice = timeChoice
        if self.timeChoice == 0:
            self.timeEnd = self.timeNow + timedelta(hours=hour, minutes=minute)
        if self.timeChoice == 1:
            self.timeEnd = self.timeNow
            while self.timeEnd.hour != hour or self.timeEnd.minute != minute:
                self.timeEnd = self.timeEnd + timedelta(minutes=1)
            self.timeEnd = self.timeEnd - timedelta(seconds=self.timeNow.second)

        self.buttonStop = Button(self.root, text="Anuluj odliczanie", padx=30, pady=15, fg="white", bg="green",
                                 command=self.back_to_input_window)
        self.buttonStop.place(x=ROOT_WIDTH / 1.5, y=320)
        self.draw_time_to_end()

        Label(self.root, text="Pozostały czas do " + self.operation_translate() + ": ",
              font=(FONT, 15), bg=BG_COLOR).place(x=25, y=100)

        Label(self.root, text="Operacja zostanie wykonana o godzinie: ",
              font=(FONT, 15), bg=BG_COLOR).place(x=25, y=175)
        self.draw_end_time()

    def back_to_input_window(self):
        self.root.destroy()
        self.root.after_cancel(self.drawTimeToEndActive)
        InputWindow()

    def draw_end_time(self):
        hour = self.timeEnd.hour
        min = self.timeEnd.minute
        lab = Label(self.root, text=str(hour).zfill(2) + ":" + str(min).zfill(2), font=(FONT, 25), bg=BG_COLOR)
        lab.place(x=25, y=200)

    def draw_time_to_end(self):
        lab = Label(self.root, text=self.remaining_time(), font=(FONT, 25), bg=BG_COLOR)
        lab.place(x=25, y=125)
        self.drawTimeToEndActive = self.root.after(1000, self.draw_time_to_end)

    def remaining_time(self):
        now = datetime.now()

        if self.timeEnd > now:
            result = self.timeEnd - timedelta(hours=now.hour, minutes=now.minute,
                                              seconds=now.second)

            return str(result.hour).zfill(2) + ":" + str(result.minute).zfill(2) + ":" + str(result.second).zfill(2)
        else:
            self.root.destroy()
            self.operation()

    def operation(self):
        if self.modeChoice == 0:
            os.system("shutdown /p /f")
        elif self.modeChoice == 1:
            os.system("shutdown /s")
        elif self.modeChoice == 2:
            os.system("shutdown /r -t 0")
        elif self.modeChoice == 3:
            os.system("shutdown /l")
        elif self.modeChoice == 4:
            os.system("shutdown /h")

    def operation_translate(self):
        if self.modeChoice == 0:
            return "wyłączenia komputera"
        elif self.modeChoice == 1:
            return "wyłączenia komputera"
        elif self.modeChoice == 2:
            return "uruchomienia ponownie"
        elif self.modeChoice == 3:
            return "wylogowanie"
        elif self.modeChoice == 4:
            return "hibernacji"

    def __del__(self):
        print("Usunieto counting_window")


def main():
    A = InputWindow()


if __name__ == "__main__":
    main()
