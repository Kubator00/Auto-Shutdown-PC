# autor: Jakub Więcek
# 18.08.2021r
import tkinter
from tkinter import *
from tkinter import messagebox
import os

from datetime import datetime
from datetime import timedelta

ROOT_HEIGHT = 500
ROOT_WIDTH = 800
BG_COLOR = "bisque"
FONT = "ARIAL"


class App:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry(str(ROOT_WIDTH) + 'x' + str(ROOT_HEIGHT))
        self.root.resizable(width=False, height=False)
        self.root.title("Automatyczne Wyłączanie PC")
        self.root.configure(bg=BG_COLOR)

        # title
        self.labelTitle = Label(self.root, text="AUTOMATYCZNE WYŁĄCZANIE KOMPUTERA", font=(FONT, 19), bg=BG_COLOR)
        self.labelTitle.place(relx=0.5, rely=0.08, anchor=CENTER)

        self.labelAuthor = Label(self.root, text="Autor: Jakub Więcek", font=(FONT, 10), bg=BG_COLOR)
        self.labelAuthor.place(x=650, y=470)
        # buttons
        self.buttonRun = Button(self.root, text="Uruchom odliczanie", pady=15, width=22, fg="white", bg="green",
                                command=self.set_time_mode)
        self.buttonRun.place(x=600, y=100)

        self.buttonStop = Button(self.root, text="Anuluj odliczanie", pady=15, width=22, fg="white", bg="green",
                                 command=self.stop_counter)
        self.buttonStop.place(x=600, y=200)

        self.buttonExit = Button(self.root, text="Wyjście", pady=15, width=22, fg="white", bg="green",
                                 command=self.quit)
        self.buttonExit.place(x=600, y=300)

        # radio buttons
        MODES = ["Twarde wyłączenie komputera", "Wyłącz komputer", "Uruchom Ponownie", "Wyloguj", "Hibernacja"]
        self.modeChoice = IntVar()
        i = 0
        for text in MODES:
            Radiobutton(self.root, text=text, variable=self.modeChoice, value=i, bg=BG_COLOR) \
                .place(x=350, y=100 + i * 25)
            i += 1

        # entry 1
        self.timeMode = IntVar()
        Radiobutton(self.root, text="WPISZ CZAS DO WYLĄCZENIA KOMPUTERA", variable=self.timeMode, value=0,
                    bg=BG_COLOR).place(x=15, y=80)

        self.labelHour1 = Label(self.root, text="GODZIN: ", bg=BG_COLOR)
        self.labelHour1.place(x=15, y=120)
        self.entryHour1 = Entry(self.root, width=5, borderwidth=3)
        self.entryHour1.insert(0, "1")
        self.entryHour1.place(x=90, y=120)

        self.labelMinute1 = Label(self.root, text="MINUT: ", bg=BG_COLOR).place(x=140, y=120)
        self.entryMinute1 = Entry(self.root, width=5, borderwidth=3)
        self.entryMinute1.insert(0, "0")
        self.entryMinute1.place(x=205, y=120)

        # entry 2
        Radiobutton(self.root, text="WPISZ GODZINĘ WYLĄCZENIA KOMPUTERA", variable=self.timeMode, value=1,
                    bg=BG_COLOR).place(x=15, y=170)

        self.labelHour2 = Label(self.root, text="GODZINA: ", bg=BG_COLOR).place(x=15, y=200)
        self.entryHour2 = Entry(self.root, width=5, borderwidth=3)
        self.entryHour2.insert(0, "1")
        self.entryHour2.place(x=90, y=200)

        self.labelMinute2 = Label(self.root, text="MINUTA: ", bg=BG_COLOR).place(x=140, y=200)
        self.entryMinute2 = Entry(self.root, width=5, borderwidth=3)
        self.entryMinute2.insert(0, "0")
        self.entryMinute2.place(x=205, y=200)

        # count_down
        self.isActiveCountDown = False
        self.timeNow = None
        self.timeEnd = None
        self.drawTimeToEndActive = None

        self.labelCounterTitle = Label(self.root, text="", font=(FONT, 15), bg=BG_COLOR)
        self.labelCounter = Label(self.root, text=self.remaining_time_to_end(), font=(FONT, 25), bg=BG_COLOR)

        self.labelHourEndTitle = Label(self.root, text="Godzina wykonania operacji: ", font=(FONT, 15), bg=BG_COLOR)
        self.labelHourEnd = Label(self.root, text="", font=(FONT, 25), bg=BG_COLOR)

    def set_time_end(self, hour, minute):
        self.timeNow = datetime.now()
        if self.timeMode.get() == 0:
            self.timeEnd = self.timeNow + timedelta(hours=hour, minutes=minute)
        elif self.timeMode.get() == 1:
            self.timeEnd = self.timeNow
            while self.timeEnd.hour != hour or self.timeEnd.minute != minute:
                self.timeEnd = self.timeEnd + timedelta(minutes=1)
            self.timeEnd = self.timeEnd - timedelta(seconds=self.timeNow.second)

    def set_time_mode(self):
        if self.isActiveCountDown:
            messagebox.showwarning(title="Błąd", message="Musisz anulować bieżące odliczanie")
            return

        if self.timeMode.get() == 0:
            self.activate_countdown_to_time()
        elif self.timeMode.get() == 1:
            self.activate_countdown_to_hour()

    # aktywuje odliczanie jeśli wpiszemy za ile chcemy wyłączyć pc
    def activate_countdown_to_time(self):
        try:
            hour = int(self.entryHour1.get())
            minute = int(self.entryMinute1.get())
            if hour < 0 or minute < 0 or (hour == 0 and minute == 0) or hour > 23 or minute > 59:
                messagebox.showwarning(title="Błąd", message="Wpisano błędną wartość")
                return
            self.isActiveCountDown = True
            self.set_time_end(hour, minute)
            self.draw_counter()
            self.draw_end_hour_and_title()
            self.draw_counter_title()
            if self.modeChoice.get() == 4:
                messagebox.showwarning(title="Uwaga",
                                       message="Jeśli hibernacja w systemie nie jest włączona, operacja nie zakończy się pomyślnie")

        except ValueError:
            messagebox.showwarning(title="Błąd", message="Podana wartość nie jest liczba")
            return

    # aktywuje odliczanie jeśli wpiszemy o której chcemy wyłączyć pc
    def activate_countdown_to_hour(self):
        try:
            hour = int(self.entryHour2.get())
            minute = int(self.entryMinute2.get())
            if hour < 0 or minute < 0 or (hour == 0 and minute == 0) or hour > 23 or minute > 59:
                messagebox.showwarning(title="Błąd", message="Wpisano błędną wartość")
                return
            self.isActiveCountDown = True
            self.set_time_end(hour, minute)
            self.draw_counter()
            self.draw_end_hour_and_title()
            self.draw_counter_title()
            if self.modeChoice.get() == 4:
                messagebox.showwarning(title="Uwaga",
                                       message="Jeśli hibernacja w systemie nie jest włączona, operacja nie zakończy się pomyślnie")

        except ValueError:
            messagebox.showwarning(title="Błąd", message="Podana wartość nie jest liczba")
            return

    def stop_counter(self):
        if not self.isActiveCountDown:
            return
        self.isActiveCountDown = False
        self.timeEnd = None
        self.timeNow = None
        self.root.after_cancel(self.drawTimeToEndActive)
        self.drawTimeToEndActive = None

        self.labelCounterTitle.place_forget()
        self.labelCounter.place_forget()
        self.labelHourEndTitle.place_forget()
        self.labelHourEnd.place_forget()

    def __del__(self):
        print("Usunieto input_window")

    def quit(self):
        self.root.destroy()

    def draw_end_hour_and_title(self):
        self.labelHourEndTitle = Label(self.root, text="Godzina wykonania operacji: ", font=(FONT, 15), bg=BG_COLOR)
        self.labelHourEndTitle.place(x=15, y=360)
        hour = self.timeEnd.hour
        minutes = self.timeEnd.minute
        self.labelHourEnd = Label(self.root, text=str(hour).zfill(2) + ":" + str(minutes).zfill(2), font=(FONT, 25),
                                  bg=BG_COLOR)
        self.labelHourEnd.place(x=15, y=390)

    def draw_counter_title(self):
        self.labelCounterTitle.place_forget()
        self.labelCounterTitle = Label(self.root, text="Czas do " + str(self.operation_translate()) + ": ",
                                       font=(FONT, 15), bg=BG_COLOR)
        self.labelCounterTitle.place(x=15, y=280)

    def draw_counter(self):
        if not self.isActiveCountDown:
            self.root.after_cancel(self.drawTimeToEndActive)
            self.labelCounter.place_forget()
            return
        self.labelCounter.place_forget()
        self.labelCounter = Label(self.root, text=self.remaining_time_to_end(), font=(FONT, 25), bg=BG_COLOR)
        self.labelCounter.place(x=15, y=310)
        self.drawTimeToEndActive = self.root.after(1000, self.draw_counter)

    def remaining_time_to_end(self):
        if not self.isActiveCountDown:
            return
        now = datetime.now()
        if self.timeEnd > now:
            result = self.timeEnd - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
            if result.hour == 0 and result.minute == 1 and result.second == 0:
                messagebox.showwarning(title="Uwaga",
                                       message="Do " + str(self.operation_translate()) + " pozostała 1 minuta!")

            return str(result.hour).zfill(2) + ":" + str(result.minute).zfill(2) + ":" + str(result.second).zfill(2)
        else:
            self.operation()

    def operation(self):
        self.root.destroy()
        if self.modeChoice.get() == 0:
            os.system("shutdown /p /f")
        elif self.modeChoice.get() == 1:
            os.system("shutdown /s ")
        elif self.modeChoice.get() == 2:
            os.system("shutdown /r -t 0")
        elif self.modeChoice.get() == 3:
            os.system("shutdown /l")
        elif self.modeChoice.get() == 4:
            os.system("shutdown /h")

    def operation_translate(self):
        if self.modeChoice.get() == 0:
            return "wyłączenia komputera"
        elif self.modeChoice.get() == 1:
            return "wyłączenia komputera"
        elif self.modeChoice.get() == 2:
            return "uruchomienia ponownie"
        elif self.modeChoice.get() == 3:
            return "wylogowania"
        elif self.modeChoice.get() == 4:
            return "hibernacji"


def main():
    A = App()
    A.root.mainloop()


if __name__ == "__main__":
    main()
