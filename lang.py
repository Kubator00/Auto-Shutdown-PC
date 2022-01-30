class Languages:
    def __init__(self):
        self.availableLanguages = ["polish", "english"]
        self.currentLanguage = self.availableLanguages[1]
        self.title = {"polish": "Automatyczne wyłączanie PC", "english": "Auto Shutdown PC"}
        self.exit = {"polish": "Wyjście", "english": "Quit"}
        self.modes = {"polish": ["Twarde wyłączenie komputera", "Wyłącz komputer", "Uruchom Ponownie", "Wyloguj",
                                 "Hibernacja"], "english": ["Force shut down", "Shut down", "Reboot", "Logout",
                                                            "Hibernate"]}
        self.startCountdown = {"polish": "Uruchom odliczanie", "english": "Start countdown"}
        self.cancelCountdown = {"polish": "Anuluj odliczanie", "english": "Cancel countdown"}
        self.radioButtonInputType1 = {"polish": "CZAS DO WYKONANIA OPERACJI",
                                      "english": "Time from now"}
        self.radioButtonInputType2 = {"polish": "GODZINA WYKONANIA OPERACJI",
                                      "english": "Specified time"}
        self.taskTitle = {"polish": "Zadanie:", "english": "Task:"}
        self.hour1 = {"polish": "Godzin:", "english": "Hours:"}
        self.minute1 = {"polish": "Minut:", "english": "Minutes:"}
        self.hour2 = {"polish": "Godzina:", "english": "Hour:"}
        self.minute2 = {"polish": "Minuta:", "english": "Minute:"}
        self.shutdown = {"polish": "wyłączenia komputera", "english": "shutdown"}
        self.reboot = {"polish": "uruchomienia ponownie ", "english": "reboot"}
        self.logout = {"polish": "wylogowania", "english": "logout"}
        self.hibernate = {"polish": "hibernacji ", "english": "hibernate"}
        self.timeTo1 = {"polish": "Czas do", "english": "Computer will"}
        self.timeTo2 = {"polish": "", "english": " in"}
        self.author = {"polish": "Autor", "english": "Author"}
        self.executionTime = {"polish": "Czas wykonania operacji ", "english": "Execution time"}
        self.notificationTitle = {"polish": "Uwaga!", "english": "Warning!"}
        self.notificationMessage = {"polish": "Do wykonania operacji pozostało mniej niż 2 minuty",
                                    "english": "Operation will execute within 2 minutes"}
        self.warningTitle = {"polish": "Uwaga!", "english": "Warning!"}
        self.warningCancelCountDown = {"polish": "Musisz anulować bieżące odliczanie",
                                       "english": "You must cancel the current countdown"}
        self.warningIncorrectInput = {"polish": "Wpisano niepoprawne wartości", "english": "Incorrect input"}
        self.hibernateWarning = {
            "polish": "Jeśli hibernacja w systemie nie jest włączona, operacja nie zakończy się pomyślnie",
            "english": "If system hibernation is not enabled, the operation won't be successful"}

        self.dict = {"title": self.title,
                     "exit": self.exit,
                     "modes": self.modes,
                     "startCountdown": self.startCountdown,
                     "cancelCountdown": self.cancelCountdown,
                     "radioButtonInputType1": self.radioButtonInputType1,
                     "radioButtonInputType2": self.radioButtonInputType2,
                     "taskTitle": self.taskTitle,
                     "hour1": self.hour1,
                     "minute1": self.minute1,
                     "hour2": self.hour2,
                     "minute2": self.minute2,
                     "shutdown": self.shutdown,
                     "reboot": self.reboot,
                     "logout": self.logout,
                     "hibernate": self.hibernate,
                     "timeTo1": self.timeTo1,
                     "timeTo2": self.timeTo2,
                     "author":  self.author,
                     "executionTime": self.executionTime,
                     "notificationTitle": self.notificationTitle,
                     "notificationMessage": self.notificationMessage,
                     "warningTitle": self.warningTitle,
                     "warningCancelCountDown": self.warningCancelCountDown,
                     "warningIncorrectInput": self.warningIncorrectInput,
                     "hibernateWarning": self.hibernateWarning
                     }

    def change_language(self, langName):
        self.currentLanguage = langName

    def get(self, elementName):
        return self.dict[elementName][self.currentLanguage]
