import os
import time
import json

from StationMsg import StationMsg


class Ypsilon:
    actions = []
    timestamp = None
    error = False
    # Zerowanie zapisu akcji po podanym czasie
    terminal_waitinf = 300
    auth = False
    # zmienne
    airlock_docking_bay_1 = False
    airlock_docking_bay_2 = False
    airlock_mineshaft = False
    shower_1 = False
    shower_2 = False
    shower_3 = False
    shower_4 = False
    shower_5 = False

    def __init__(self):
        print("FIFLAK")
        if os.path.exists("./saves/action.json"):
            with open("./saves/action.json") as json_file:
                data = json.load(json_file)
                if 'action' in data:
                    self.actions = data['action']
                if 'auth' in data:
                    self.auth = data['auth']

                vars = ['airlock_docking_bay_1','airlock_docking_bay_2','airlock_mineshaft','shower_1','shower_2','shower_3','shower_4','shower_5']
                for v in vars:
                    if v in data:
                        exec("self."+v + "= " + str(data[v]))

                if 'timestamp' in data:
                    self.timestamp = data['timestamp']
                else:
                    self.timestamp = time.time()
        else:
            with open("./saves/action.json", 'w') as outfile:
                json.dump({'action': [], 'timestamp': time.time()}, outfile)

        if self.timestamp + self.terminal_waitinf < time.time():
            self.timestamp = time.time()
            self.actions = []
            with open("./saves/action.json", 'w') as outfile:
                json.dump({'action': [], 'timestamp': time.time(), 'auth': False}, outfile)

    def action(self, cmd):
        response = StationMsg()
        cmd = cmd.replace('>', '').lower()
        # komendy specjalne
        if cmd == 'station':
            self.actions = []
        result = ''
        # terminal  options
        if len(self.actions) == 0 :
            result = response.hello()
            self.actions.append('init')
        elif len(self.actions) == 1:
            if cmd == "diagnostics":
                self.actions.append(cmd)
                result = response.menu_diagnostics()
            elif cmd == "controls":
                self.actions.append(cmd)
                result = response.menu_controls()
            elif cmd == "schedule":
                self.actions.append(cmd)
                result = response.schedule()
            elif cmd == 'roster':
                self.actions.append(cmd)
                result = response.roster()
            elif cmd == "comms":
                self.actions.append(cmd)
                result = response.comms_menu()
            elif cmd == "back":
                result = response.menu_main()
                self.actions.pop()
            else:
                self.error = True
                result = response.syntax_error()
        elif len(self.actions) == 2:
            if self.actions[1] == "diagnostics":
                if cmd == "layout":
                    self.actions.append(cmd)
                    result = response.layout()
                elif cmd == "status":
                    self.actions.append(cmd)
                    result = response.diag_status()
                elif cmd == "back":
                    result = response.menu_main()
                    self.actions.pop()
                else:
                    self.error = True
                    result = response.syntax_error()
            elif self.actions[1] == "schedule":
                if cmd == "back":
                    result = response.menu_main()
                    self.actions.pop()
                else:
                    self.error = True
                    result = response.syntax_error()
            elif self.actions[1] == 'controls':
                if cmd == 'back':
                    result = response.menu_main()
                    self.actions.pop()
                elif cmd == "airlocks":
                    self.actions.append(cmd)
                    result = response.controls_airlock(self.airlock_docking_bay_1,self.airlock_docking_bay_2,self.airlock_mineshaft)
                elif cmd == "showers":
                    self.actions.append(cmd)
                    result = response.controll_shower()
                elif cmd == "system":
                    # self.actions.append(cmd)
                    result = response.controll_system(self.auth)
                elif cmd == "insert sonya keycard":
                    self.auth = True
                    result = response.controll_system(self.auth)
                else:
                    self.error = True
                    result = response.syntax_error()
        elif len(self.actions) == 3:
            if self.actions[1] == "diagnostics":
                if self.actions[2] == "status":
                    if cmd == "back":
                        result = response.menu_diagnostics()
                        self.actions.pop()
                    elif cmd == "back":
                        result = response.menu_main()
                        self.actions.pop()
                    else:
                        self.error = True
                        result = response.syntax_error()
                elif self.actions[2] == "layout":
                    if cmd == "download":
                        self.actions.pop()
                        result = [response.download(), response.menu_diagnostics()]
                    elif cmd == "back":
                        result = response.menu_diagnostics()
                        self.actions.pop()
                    else:
                        self.error = True
                        result = response.syntax_error()
                elif cmd == 'back':
                    result = response.menu_main()
                    self.actions.pop()
                else:
                    self.error = True
                    result = response.syntax_error()
            if self.actions[1] == 'controls':
                print(cmd)
                if self.actions[2] == "airlocks":
                    if cmd == "unlock mineshaft":
                        self.airlock_mineshaft = True
                        result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                           self.airlock_mineshaft)
                    elif cmd == "unlock dock 1" or cmd == "unlock docking bay 1":
                        self.airlock_docking_bay_1 = True
                        result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                           self.airlock_mineshaft)
                    elif cmd == "unlock dock 2" or cmd == "unlock docking bay 2":
                        self.airlock_docking_bay_2 = True
                        result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                           self.airlock_mineshaft)
                    elif cmd == "lock mineshaft":
                        self.airlock_mineshaft = False
                        result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                           self.airlock_mineshaft)
                    elif cmd == "lock dock 1" or cmd == "lock docking bay 1":
                        self.airlock_docking_bay_1 = False
                        result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                           self.airlock_mineshaft)
                    elif cmd == "lock dock 2" or cmd == "lock docking bay 2":
                        self.airlock_docking_bay_2 = False
                        result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                           self.airlock_mineshaft)
                    elif cmd == 'back':
                        result = response.menu_controls()
                        self.actions.pop()
                    else:
                        self.error = True
                        result = response.syntax_error()


        if self.error is not True:
            self.save()

        return result

    def save(self):
        with open("./saves/action.json", 'w') as outfile:
            json.dump({
                'action': self.actions,
                'timestamp': time.time(),
                'airlock_docking_bay_1':self.airlock_docking_bay_1,
                'airlock_docking_bay_2':self.airlock_docking_bay_2,
                'airlock_mineshaft':self.airlock_mineshaft,
            }, outfile)
