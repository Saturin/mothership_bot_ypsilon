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
    life_support = True

    def __init__(self):
        if os.path.exists("./saves/action.json"):
            with open("./saves/action.json") as json_file:
                data = json.load(json_file)
                if 'action' in data:
                    self.actions = data['action']
                if 'auth' in data:
                    self.auth = data['auth']

                vars = ['airlock_docking_bay_1', 'airlock_docking_bay_2', 'airlock_mineshaft', 'shower_1', 'shower_2',
                        'shower_3', 'shower_4', 'shower_5', 'shower_1', 'shower_2', 'shower_3', 'shower_4', 'shower_5',
                        'life_support', 'auth']
                for v in vars:
                    if v in data:
                        exec("self." + v + "= " + str(data[v]))

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
        result = ''
        response = StationMsg()
        cmd = cmd.replace('>', '').lower()
        # komendy specjalne
        if cmd == 'station':
            self.actions = []
        elif cmd == 'insert sonya keycard':
            self.auth = True
            self.save()
            return  response.admin_msg(self.auth)
        elif cmd == "remove sonya keycard":
            self.auth = False
            self.save()
            return response.admin_msg(self.auth)
        elif cmd == 'insert admin keycard':
            self.auth = True
            self.save()
            return  response.admin_msg(self.auth)
        elif cmd == "remove admin keycard":
            self.auth = False
            self.save()
            return response.admin_msg(self.auth)

        # terminal opcje
        if len(self.actions) == 0:
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
                    result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                       self.airlock_mineshaft)
                elif cmd == "showers":
                    self.actions.append(cmd)
                    result = response.controll_shower(self.shower_1, self.shower_2, self.shower_3, self.shower_4,
                                                      self.shower_5)
                elif cmd == "system":
                    self.actions.append(cmd)
                    result = response.controll_system(self.auth)
                elif cmd == "insert sonya keycard":
                    self.auth = True
                    result = response.controll_system(self.auth)
                elif cmd == "remove sonya keycard":
                    self.auth = False
                    result = response.controll_system(self.auth)

                else:
                    self.error = True
                    result = response.syntax_error()
            elif self.actions[1] == 'comms':
                if cmd in ['hail heracles',"heracles",'hail rsv heracles','hail rsv the heracles']:
                    self.actions.append('heracles')
                    result = response.comms_heracles()
                elif cmd in ["grasshopper", 'hail grasshoper', 'hail imv grasshopper']:
                    self.actions.append("grasshopper")
                    result = response.comms_grasshoper()
                elif cmd == 'back':
                    result = response.comms_menu()
                    self.actions.pop()
                else:
                    self.error = True
                    result = response.syntax_error()
            elif self.actions[1] == "roster":
                if cmd == "back":
                    self.actions.pop()
                    result = response.menu_main()
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
            elif self.actions[1] == 'controls':
                if self.actions[2] == "airlocks":
                    if cmd in ["unlock mineshaft", "mineshaft unlock"]:
                        self.airlock_mineshaft = True
                        result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                           self.airlock_mineshaft)
                    elif cmd in ["unlock dock 1", "unlock docking bay 1", "dock 1 unlock", "docking bay 1 unlock"]:
                        self.airlock_docking_bay_1 = True
                        result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                           self.airlock_mineshaft)
                    elif cmd in ["unlock dock 2", "unlock docking bay 2", "dock 2 unlock", "docking bay 2 unlock"]:
                        self.airlock_docking_bay_2 = True
                        result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                           self.airlock_mineshaft)
                    elif cmd in ["lock mineshaft", "mineshaft lock"]:
                        self.airlock_mineshaft = False
                        result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                           self.airlock_mineshaft)
                    elif cmd in ["lock dock 1", "lock docking bay 1", "dock 1 lock", "docking bay 1 lock"]:
                        self.airlock_docking_bay_1 = False
                        result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                           self.airlock_mineshaft)
                    elif cmd in ["lock dock 2", "lock docking bay 2", "dock 2 lock", "docking bay 2 lock"]:
                        self.airlock_docking_bay_2 = False
                        result = response.controls_airlock(self.airlock_docking_bay_1, self.airlock_docking_bay_2,
                                                           self.airlock_mineshaft)
                    elif cmd == 'back':
                        result = response.menu_controls()
                        self.actions.pop()
                    else:
                        self.error = True
                        result = response.syntax_error()
                elif self.actions[2] == "showers":
                    if cmd == "shower 1 unlock":
                        self.shower_1 = True
                        result = response.controll_shower(self.shower_1, self.shower_2, self.shower_3, self.shower_4,
                                                          self.shower_5)
                    elif cmd == "shower 2 unlock":
                        self.shower_2 = True
                        result = response.controll_shower(self.shower_1, self.shower_2, self.shower_3, self.shower_4,
                                                          self.shower_5)
                    elif cmd == "shower 3 unlock":
                        self.shower_3 = True
                        result = response.controll_shower(self.shower_1, self.shower_2, self.shower_3, self.shower_4,
                                                          self.shower_5)
                    elif cmd == "shower 4 unlock":
                        self.shower_4 = True
                        result = response.controll_shower(self.shower_1, self.shower_2, self.shower_3, self.shower_4,
                                                          self.shower_5)
                    elif cmd == "shower 5 unlock":
                        self.shower_5 = True
                        result = response.controll_shower(self.shower_1, self.shower_2, self.shower_3, self.shower_4,
                                                          self.shower_5)
                    elif cmd == "shower 1 lock":
                        self.shower_1 = False
                        result = response.controll_shower(self.shower_1, self.shower_2, self.shower_3, self.shower_4,
                                                          self.shower_5)
                    elif cmd == "shower 2 lock":
                        self.shower_2 = False
                        result = response.controll_shower(self.shower_1, self.shower_2, self.shower_3, self.shower_4,
                                                          self.shower_5)
                    elif cmd == "shower 3 lock":
                        self.shower_3 = False
                        result = response.controll_shower(self.shower_1, self.shower_2, self.shower_3, self.shower_4,
                                                          self.shower_5)
                    elif cmd == "shower 4 lock":
                        self.shower_4 = False
                        result = response.controll_shower(self.shower_1, self.shower_2, self.shower_3, self.shower_4,
                                                          self.shower_5)
                    elif cmd == "shower 5 lock":
                        self.shower_5 = False
                        result = response.controll_shower(self.shower_1, self.shower_2, self.shower_3, self.shower_4,
                                                          self.shower_5)
                    elif cmd == 'back':
                        result = response.menu_controls()
                        self.actions.pop()
                    else:
                        self.error = True
                        result = response.syntax_error()
                elif self.actions[2] == "system":
                    if cmd == "life support":
                        self.actions.append(cmd)
                        if self.auth is True:
                            result = response.lifesupport(self.life_support)
                        else:
                            result = response.controll_system(self.auth)
                    elif cmd == "scuttle":
                        self.actions.append(cmd)
                        if self.auth is True:
                            result = response.scuttle()
                        else:
                            result = response.controll_system(self.auth)
                    elif cmd == "back":
                        result = response.menu_controls()
                        self.actions.pop()
                    elif cmd == "insert sonya keycard":
                        self.auth = True
                        result = response.controll_system(self.auth)
                    elif cmd == "remove sonya keycard":
                        self.auth = False
                        result = response.controll_system(self.auth)
                    else:
                        self.error = True
                        result = response.syntax_error()
            elif self.actions[1] == "comms":
                if self.actions[2] == "heracles" or self.actions[2] == "grasshopper":
                    if cmd == "end call" or cmd == "end":
                        self.actions.pop()
                        result = response.comms_menu()
                    else:
                        self.error = True
                        result = response.syntax_error()
        elif len(self.actions) == 4:
            if self.actions[3] == "life support":
                if cmd == 'back':
                    result = response.controll_system(self.auth)
                    self.actions.pop()
                elif cmd in ["life support off", "life support false"]:
                    self.life_support = False
                    result = response.lifesupport(self.life_support)
                elif cmd in ["life support on", "life support true"]:
                    self.life_support = True
                    result = response.lifesupport(self.life_support)
                else:
                    self.error = True
                    result = response.syntax_error()
            elif self.actions[3] == 'scuttle':
                if cmd == "scuttle":
                    result = response.autodestruction()
                elif cmd == "back":
                    result = response.controll_system(self.auth)
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
                'auth': self.auth,
                'airlock_docking_bay_1': self.airlock_docking_bay_1,
                'airlock_docking_bay_2': self.airlock_docking_bay_2,
                'airlock_mineshaft': self.airlock_mineshaft,
                'shower_1': self.shower_1,
                'shower_2': self.shower_2,
                'shower_3': self.shower_3,
                'shower_4': self.shower_4,
                'shower_5': self.shower_5,
                'life_support': self.life_support
            }, outfile)
