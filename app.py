import tkinter
from tkinter import *
from tkinter import messagebox
import os

from datetime import datetime
from datetime import timedelta
from functools import partial
from win10toast import ToastNotifier
from lang import *

ROOT_HEIGHT = 440
ROOT_WIDTH = 445
BG_COLOR = "#E8E8E8"
BUTTON_COLOR = "#F7B054"
FONT = "Calibri"


class App:
    firstColumnPositionX = 35
    secondColumnPositionX = 250
    labelCountdownMode = None
    labelOperationTitle = None
    radioButtonInputType = []
    button = buttonStop = None
    displayedNotification = False
    isActiveCountDown = False
    inputTime = {}
    radioButtonOperationType = []
    timeNow = timeEnd = drawTimeToEndActive = labelHourEndTitle = labelHourEnd = None

    def __init__(self):
        self.Langs = Languages()
        # general
        self.toaster = ToastNotifier()
        self.root = tkinter.Tk()
        self.win_init()
        self.menu_init()
        # program title
        self.labelTitle = Label(self.root, text=self.Langs.get("title"), font=(FONT, 22), bg=BG_COLOR)
        self.labelTitle.place(relx=0.5, rely=0.08, anchor=CENTER)
        # buttons && inputs
        self.timeMode = IntVar()
        self.modeChoice = IntVar()
        self.radio_button_input_type_init()
        self.radio_button_operation_type_init()
        self.button_init()
        # counter
        self.labelCounterTitle = Label(self.root, text="", font=(FONT, 15), bg=BG_COLOR)
        self.labelCounter = Label(self.root, text=self.remaining_time_to_end(), font=(FONT, 25), bg=BG_COLOR)

    def win_init(self):
        self.root.geometry(str(ROOT_WIDTH) + 'x' + str(ROOT_HEIGHT))
        self.root.resizable(width=False, height=False)
        self.root.title(self.Langs.get("title"))
        self.root.configure(bg=BG_COLOR)

    def button_init(self):
        self.button = Button(self.root, text=self.Langs.get("startCountdown"), pady=10, padx=0, width=17, fg="white",
                             font=(FONT, 12), bg="#10B13D", borderwidth=0, command=self.activate_countdown)
        self.button.place(x=self.secondColumnPositionX + 2, y=230)

    def radio_button_input_type_init(self):
        self.labelCountdownMode = Label(self.root, text=self.Langs.get("countdownMode"), font=(FONT, 11),
                                        bg=BG_COLOR)
        self.labelCountdownMode.place(x=self.secondColumnPositionX, y=85)
        self.radioButtonInputType.append(
            Radiobutton(self.root, text=self.Langs.get("radioButtonInputType1"), variable=self.timeMode, value=0,
                        bg=BG_COLOR, font=(FONT, 10)))
        self.radioButtonInputType.append(
            Radiobutton(self.root, text=self.Langs.get("radioButtonInputType2"), variable=self.timeMode, value=1,
                        bg=BG_COLOR, font=(FONT, 10)))
        self.radioButtonInputType[0].place(x=self.secondColumnPositionX, y=120)
        self.radioButtonInputType[1].place(x=self.secondColumnPositionX, y=155)
        self.inputTime["label"] = Label(self.root, text=self.Langs.get("time"), bg=BG_COLOR, font=(FONT, 11))
        self.inputTime["label"].place(x=self.secondColumnPositionX, y=190)
        self.inputTime["hour"] = Entry(self.root, width=5, font=(FONT, 10), borderwidth=1)
        self.inputTime["hour"].insert(0, "1")
        self.inputTime["hour"].place(x=self.secondColumnPositionX + 50, y=194)
        Label(self.root, text=":", font=(FONT, 11), bg=BG_COLOR).place(x=self.secondColumnPositionX + 90, y=190)
        self.inputTime["min"] = Entry(self.root, width=5, font=(FONT, 10), borderwidth=1)
        self.inputTime["min"].insert(0, "0")
        self.inputTime["min"].place(x=self.secondColumnPositionX + 103, y=194)

        self.radioButtonInputType.append(
            Radiobutton(self.root, text=self.Langs.get("radioButtonInputType2"), variable=self.timeMode, value=1,
                        bg=BG_COLOR))

    def radio_button_operation_type_init(self):
        self.labelOperationTitle = Label(self.root, text=self.Langs.get("taskTitle"), bg=BG_COLOR, font=(FONT, 11))
        self.labelOperationTitle.place(x=self.firstColumnPositionX, y=85)
        MODES = self.Langs.get("modes")
        i = 0
        for text in MODES:
            self.radioButtonOperationType.append(
                Radiobutton(self.root, text=text, variable=self.modeChoice, value=i, bg=BG_COLOR, font=(FONT, 10)))
            self.radioButtonOperationType[i].place(x=self.firstColumnPositionX - 2, y=115 + i * 35)
            i += 1

    def menu_init(self):
        menu = Menu(self.root)
        self.root.config(menu=menu, background=BG_COLOR)
        optionsMenu = Menu(menu, tearoff=0, background=BG_COLOR)
        menu.add_cascade(label="Options", menu=optionsMenu)
        langMenu = Menu(menu, tearoff=0)
        optionsMenu.add_cascade(label="Language", menu=langMenu)
        for i in self.Langs.availableLanguages:
            langMenu.add_command(label=i.upper(), command=partial(self.change_language, i))

    def set_time_end(self, hour, minute):
        self.timeNow = datetime.now()
        if self.timeMode.get() == 0:
            self.timeEnd = self.timeNow + timedelta(hours=hour, minutes=minute)
        elif self.timeMode.get() == 1:
            self.timeEnd = self.timeNow
            while self.timeEnd.hour != hour or self.timeEnd.minute != minute:
                self.timeEnd = self.timeEnd + timedelta(minutes=1)
            self.timeEnd = self.timeEnd - timedelta(seconds=self.timeNow.second)

    def activate_countdown(self):
        try:
            hour = int(self.inputTime["hour"].get())
            minute = int(self.inputTime["min"].get())
            if hour < 0 or minute < 0 or (hour == 0 and minute == 0) or hour > 23 or minute > 59:
                messagebox.showwarning(title=self.Langs.get("warningTitle"),
                                       message=self.Langs.get("warningIncorrectInput"))
                return
            self.isActiveCountDown = True
            self.change_button()
            self.set_time_end(hour, minute)
            self.draw_counter()
            self.draw_execution_time()
            self.draw_counter_title()
            if self.modeChoice.get() == 4:
                messagebox.showwarning(title=self.Langs.get("warningTitle"),
                                       message=self.Langs.get("hibernateWarning"))
        except ValueError:
            messagebox.showwarning(title=self.Langs.get("warningTitle"),
                                   message=self.Langs.get("warningIncorrectInput"))
            return

    def change_button(self):
        if self.isActiveCountDown:
            self.button['text'] = self.Langs.get("cancelCountdown")
            self.button['command'] = self.stop_counter
            self.button['bg'] = "#C7261C"
            return
        self.button['text'] = self.Langs.get("startCountdown")
        self.button['command'] = self.activate_countdown
        self.button['bg'] = "#10B13D"

    def stop_counter(self):
        self.isActiveCountDown = False
        self.timeEnd = None
        self.timeNow = None
        self.root.after_cancel(self.drawTimeToEndActive)
        self.drawTimeToEndActive = None
        self.displayedNotification = False
        self.labelCounterTitle.place_forget()
        self.labelCounter.place_forget()
        self.labelHourEndTitle.place_forget()
        self.labelHourEnd.place_forget()
        self.change_button()

    def draw_counter_title(self):
        self.labelCounterTitle.place_forget()
        self.labelCounterTitle = Label(self.root,
                                       text=f"{self.Langs.get('timeTo1')} {str(self.operation_name())}{self.Langs.get('timeTo2')}:",
                                       font=(FONT, 14), bg=BG_COLOR)
        self.labelCounterTitle.place(x=self.firstColumnPositionX, y=305)
        self.labelHourEndTitle = Label(self.root, text=self.Langs.get("executionTime"), font=(FONT, 14),
                                       bg=BG_COLOR)
        self.labelHourEndTitle.place(x=self.firstColumnPositionX, y=365)

    def draw_counter(self):
        if not self.isActiveCountDown:
            self.root.after_cancel(self.drawTimeToEndActive)
            self.labelCounter.place_forget()
            return
        self.labelCounter.place_forget()
        self.labelCounter = Label(self.root, text=self.remaining_time_to_end(), font=(FONT, 18), bg=BG_COLOR)
        self.labelCounter.place(x=self.firstColumnPositionX, y=330)
        self.drawTimeToEndActive = self.root.after(1000, self.draw_counter)

    def draw_execution_time(self):
        hour = self.timeEnd.hour
        minutes = self.timeEnd.minute
        self.labelHourEnd = Label(self.root, text=str(hour).zfill(2) + ":" + str(minutes).zfill(2), font=(FONT, 18),
                                  bg=BG_COLOR)
        self.labelHourEnd.place(x=self.firstColumnPositionX, y=390)

    def remaining_time_to_end(self):
        if not self.isActiveCountDown:
            return
        now = datetime.now()
        result = self.timeEnd - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
        self.system_notification(result)
        if self.timeEnd > now:
            return str(result.hour).zfill(2) + ":" + str(result.minute).zfill(2) + ":" + str(result.second).zfill(2)
        else:
            self.operation()

    def system_notification(self, data):
        if data.hour == 0 and data.minute <= 2 and not self.displayedNotification:
            self.toaster.show_toast(self.Langs.get("title"), self.Langs.get("notificationMessage"),
                                    threaded=True)
            self.displayedNotification = True

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

    def operation_name(self):
        if self.modeChoice.get() == 0:
            return self.Langs.get("shutdown")
        elif self.modeChoice.get() == 1:
            return self.Langs.get("shutdown")
        elif self.modeChoice.get() == 2:
            return self.Langs.get("reboot")
        elif self.modeChoice.get() == 3:
            return self.Langs.get("logout")
        elif self.modeChoice.get() == 4:
            return self.Langs.get("hibernate")

    def change_language(self, langName):
        self.Langs.change_language(langName)
        self.labelTitle.config(text=self.Langs.get("title"))
        self.labelCountdownMode.config(text=self.Langs.get("countdownMode"))
        self.inputTime["label"].config(text=self.Langs.get("time"))
        self.labelOperationTitle.config(text=self.Langs.get("taskTitle"))
        MODES = self.Langs.get("modes")
        i = 0
        for text in MODES:
            self.radioButtonOperationType[i].config(text=text)
            i += 1
        self.radioButtonInputType[0].config(text=self.Langs.get("radioButtonInputType1"))
        self.radioButtonInputType[1].config(text=self.Langs.get("radioButtonInputType2"))

        if self.isActiveCountDown:
            self.labelCounterTitle.config(
                text=f"{self.Langs.get('timeTo1')} {str(self.operation_name())}{self.Langs.get('timeTo2')}:")
            self.button.config(text=self.Langs.get("cancelCountdown"))
            self.labelHourEndTitle.config(text=self.Langs.get("executionTime"))
        else:
            self.button.config(text=self.Langs.get("startCountdown"))
