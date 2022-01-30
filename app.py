import tkinter
from tkinter import *
from tkinter import messagebox
import os

from datetime import datetime
from datetime import timedelta
from functools import partial
from win10toast import ToastNotifier
from lang import *

ROOT_HEIGHT = 500
ROOT_WIDTH = 800
BG_COLOR = "#459CF5"
BUTTON_COLOR = "#F7B054"
FONT = "ARIAL"


class App:
    def __init__(self):
        self.Langs = Languages()
        # general
        self.toaster = ToastNotifier()
        self.root = tkinter.Tk()
        self.win_init()
        self.menu_init()
        self.labelTitle = Label(self.root, text=self.Langs.get("title"), font=(FONT, 19), bg=BG_COLOR)
        self.labelTitle.place(relx=0.5, rely=0.08, anchor=CENTER)
        # buttons && inputs
        self.labelOperationTitle = None
        self.radioButtonInputType = []
        self.timeMode = IntVar()
        self.InputType = {"timeTo": {}, "specifiedTime": {}}
        self.radio_button_input_type_init()

        self.buttonRun = self.buttonStop = self.buttonExit = None
        self.button_init()

        self.modeChoice = IntVar()
        self.radioButtonOperationType = []
        self.radio_button_operation_type_init()

        # counter
        self.isActiveCountDown = self.timeNow = self.timeEnd = self.drawTimeToEndActive = self.labelHourEndTitle = self.labelHourEnd = None
        self.displayedNotification = False
        self.labelCounterTitle = Label(self.root, text="", font=(FONT, 15), bg=BG_COLOR)
        self.labelCounter = Label(self.root, text=self.remaining_time_to_end(), font=(FONT, 25), bg=BG_COLOR)

        self.labelAuthor = Label(self.root, text=f"{self.Langs.get('author')}: Jakub Więcek", font=(FONT, 10),
                                 bg=BG_COLOR)
        self.labelAuthor.place(x=640, y=470)

    def win_init(self):
        self.root.geometry(str(ROOT_WIDTH) + 'x' + str(ROOT_HEIGHT))
        self.root.resizable(width=False, height=False)
        self.root.title(self.Langs.get("title"))
        self.root.configure(bg=BG_COLOR)

    def button_init(self):
        self.buttonRun = Button(self.root, text=self.Langs.get("startCountdown"), pady=15, width=22, fg="black",
                                bg=BUTTON_COLOR,
                                command=self.set_time_mode)
        self.buttonRun.place(x=600, y=100)

        self.buttonStop = Button(self.root, text=self.Langs.get("cancelCountdown"), pady=15, width=22, fg="black",
                                 bg=BUTTON_COLOR,
                                 command=self.stop_counter)
        self.buttonStop.place(x=600, y=200)

        self.buttonExit = Button(self.root, text=self.Langs.get("exit"), pady=15, width=22, fg="black", bg=BUTTON_COLOR,
                                 command=self.quit)
        self.buttonExit.place(x=600, y=300)

    def radio_button_input_type_init(self):
        self.radioButtonInputType.append(
            Radiobutton(self.root, text=self.Langs.get("radioButtonInputType1"), variable=self.timeMode, value=0,
                        bg=BG_COLOR))
        self.radioButtonInputType[0].place(x=15, y=80)
        self.InputType["timeTo"]["labelHour"] = Label(self.root, text=self.Langs.get("hour1"), bg=BG_COLOR)
        self.InputType["timeTo"]["labelHour"].place(x=15, y=120)
        self.InputType["timeTo"]["entryHour"] = Entry(self.root, width=5, borderwidth=3)
        self.InputType["timeTo"]["entryHour"].insert(0, "1")
        self.InputType["timeTo"]["entryHour"].place(x=90, y=120)

        self.InputType["timeTo"]["labelMin"] = Label(self.root, text=self.Langs.get("minute1"), bg=BG_COLOR)
        self.InputType["timeTo"]["labelMin"].place(x=140, y=120)
        self.InputType["timeTo"]["entryMin"] = Entry(self.root, width=5, borderwidth=3)
        self.InputType["timeTo"]["entryMin"].insert(0, "0")
        self.InputType["timeTo"]["entryMin"].place(x=205, y=120)

        self.radioButtonInputType.append(
            Radiobutton(self.root, text=self.Langs.get("radioButtonInputType2"), variable=self.timeMode, value=1,
                        bg=BG_COLOR))
        self.radioButtonInputType[1].place(x=15, y=170)

        self.InputType["specifiedTime"]["labelHour"] = Label(self.root, text=self.Langs.get("hour2"), bg=BG_COLOR)
        self.InputType["specifiedTime"]["labelHour"].place(x=15, y=200)
        self.InputType["specifiedTime"]["entryHour"] = Entry(self.root, width=5, borderwidth=3)
        self.InputType["specifiedTime"]["entryHour"].insert(0, "1")
        self.InputType["specifiedTime"]["entryHour"].place(x=90, y=200)

        self.InputType["specifiedTime"]["labelMin"] = Label(self.root, text=self.Langs.get("minute2"), bg=BG_COLOR)
        self.InputType["specifiedTime"]["labelMin"].place(x=140, y=200)
        self.InputType["specifiedTime"]["entryMin"] = Entry(self.root, width=5, borderwidth=3)
        self.InputType["specifiedTime"]["entryMin"].insert(0, "0")
        self.InputType["specifiedTime"]["entryMin"].place(x=205, y=200)

    def radio_button_operation_type_init(self):
        self.labelOperationTitle = Label(self.root, text=self.Langs.get("taskTitle"), bg=BG_COLOR)
        self.labelOperationTitle.place(x=350, y=75)
        MODES = self.Langs.get("modes")
        i = 0
        for text in MODES:
            self.radioButtonOperationType.append(
                Radiobutton(self.root, text=text, variable=self.modeChoice, value=i, bg=BG_COLOR))
            self.radioButtonOperationType[i].place(x=350, y=100 + i * 25)
            i += 1

    def menu_init(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        optionsMenu = Menu(menu, tearoff=0)
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

    def set_time_mode(self):
        if self.isActiveCountDown:
            messagebox.showwarning(title=self.Langs.get("warningTitle"),
                                   message=self.Langs.get("warningCancelCountDown"))
            return
        inputType = "timeTo"
        if self.timeMode.get() == 1:
            inputType = "specifiedTime"
        self.activate_countdown(inputType)

    def activate_countdown(self, inputType):
        try:
            hour = int(self.InputType[inputType]["entryHour"].get())
            minute = int(self.InputType[inputType]["entryMin"].get())
            if hour < 0 or minute < 0 or (hour == 0 and minute == 0) or hour > 23 or minute > 59:
                messagebox.showwarning(title=self.Langs.get("warningTitle"),
                                       message=self.Langs.get("warningIncorrectInput"))
                return
            self.isActiveCountDown = True
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

    def stop_counter(self):
        if not self.isActiveCountDown:
            return
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

    def draw_execution_time(self):
        hour = self.timeEnd.hour
        minutes = self.timeEnd.minute
        self.labelHourEnd = Label(self.root, text=str(hour).zfill(2) + ":" + str(minutes).zfill(2), font=(FONT, 25),
                                  bg=BG_COLOR)
        self.labelHourEnd.place(x=15, y=390)

    def draw_counter_title(self):
        self.labelCounterTitle.place_forget()
        self.labelCounterTitle = Label(self.root,
                                       text=f"{self.Langs.get('timeTo1')} {str(self.operation_name())}{self.Langs.get('timeTo2')}:",
                                       font=(FONT, 15), bg=BG_COLOR)
        self.labelCounterTitle.place(x=15, y=280)
        self.labelHourEndTitle = Label(self.root, text=self.Langs.get("executionTime"), font=(FONT, 15),
                                       bg=BG_COLOR)
        self.labelHourEndTitle.place(x=15, y=360)

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

    def quit(self):
        self.root.destroy()

    def change_language(self, langName):
        self.Langs.change_language(langName)
        self.labelTitle.config(text=self.Langs.get("title"))
        self.labelOperationTitle.config(text=self.Langs.get("taskTitle"))
        MODES = self.Langs.get("modes")
        i = 0
        for text in MODES:
            self.radioButtonOperationType[i].config(text=text)
            i += 1

        self.buttonRun.config(text=self.Langs.get("startCountdown"))
        self.buttonStop.config(text=self.Langs.get("cancelCountdown"))
        self.buttonExit.config(text=self.Langs.get("exit"))
        self.radioButtonInputType[0].config(text=self.Langs.get("radioButtonInputType1"))
        self.radioButtonInputType[1].config(text=self.Langs.get("radioButtonInputType2"))
        self.InputType["timeTo"]["labelHour"].config(text=self.Langs.get("hour1"))
        self.InputType["timeTo"]["labelMin"].config(text=self.Langs.get("minute1"))
        self.InputType["specifiedTime"]["labelHour"].config(text=self.Langs.get("hour2"))
        self.InputType["specifiedTime"]["labelMin"].config(text=self.Langs.get("minute2"))
        self.labelAuthor.config(text=f"{self.Langs.get('author')}: Jakub Więcek")

        if self.isActiveCountDown:
            self.labelCounterTitle.config(
                text=f"{self.Langs.get('timeTo1')} {str(self.operation_name())}{self.Langs.get('timeTo2')}:")
            self.labelHourEndTitle.config(text=self.Langs.get("executionTime"))
