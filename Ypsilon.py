import os
from hashlib import md5
import json
from tabulate import tabulate

class Ypsilon:
    save_file = "./game_save.json"
    message = None

    init_msg = """```
 _   __        _ _               _____ _        _   _             
\ \ / /       (_) |             /  ___| |      | | (_)            
 \ V / __  ___ _| | ___  _ __   \ `--.| |_ __ _| |_ _  ___  _ __  
  \ / '_ \/ __| | |/ _ \| '_ \   `--. \ __/ _` | __| |/ _ \| '_ \ 
  | | |_) \__ \ | | (_) | | | | /\__/ / || (_| | |_| | (_) | | | |
  \_/ .__/|___/_|_|\___/|_| |_| \____/ \__\__,_|\__|_|\___/|_| |_|
    | |                                                           
    |_|              
    FLEET COMMODORE SYSTEMS © 2246 - GUILD LICENSE
    PROGRAM OPERATION GROUP SOFTWARE (P.O.G.S.)
    ----------
    WARNING - LICENSE EXPIRED
    CONTACT SYSTEMS ADMINISTRATOR
    ----------
    YPSILON 14 CONTROL TERMINAL:
        >DIAGNOSTICS
        >SCHEDULE
        >CONTROLS
        >ROSTER
        >COMMS
    ```"""

    # main_menu = """```
    # ----------------------------
    # YPSILON 14 CONTROL TERMINAL:
    #     >DIAGNOSTICS
    #     >SCHEDULE
    #     >CONTROLS
    #     >ROSTER
    #     >COMMS
    # ----------------------------
    # ```"""
    def main_menu(self):
        menu = [
            ["1","DIAGNOSTICS"],
            ["2","SCHEDULE"],
            ["3","CONTROLS"],
            ["4","ROSTER"],
            ["5","COMMS"],
        ]
        return "```YPSILON 14 CONTROL TERMINAL: \n" + tabulate(menu,tablefmt='grid') + "```"

    def __init__(self, message):
        if message.find(" ") > -1:
            self.message = message.split(' ')
        else:
            self.message = [message]
        if ~os.path.isfile(self.save_file):
            with open(self.save_file, 'a'):
                os.utime(self.save_file, None)

    def action(self):
        data = None
        msg = False

        with open(self.save_file) as f:
            data = json.load(f)

        if 'action' in data:
            if len(self.message) == 1:
                msg = self.init_msg
                self.save('init')
            else:
                cmd = self.message[1]
                action = data['action']
                if action == 'init':
                    msg = eval("self." + cmd + "()")
                else:
                    if action.find("diagnostics") > -1:
                        msg = self.diagnostics(cmd,action)
                    elif action.find('schedule') > -1:
                        msg = self.schedule(cmd)
        else:
            msg = self.init_msg
            self.save('init')

        if msg is False:
            msg = "SYNTAX ERROR"
        return msg

    def save(self, action: str):
        with open(self.save_file, 'w') as outfile:
            json.dump({'action': action}, outfile)

    def diagnostics(self, step='', save = ''):
        if step == '':
            self.save('diagnostics')
            msg = """```
DIAGNOSTICS
    > LAYOUT
    > STATUS
    < BACK```"""
        elif step == "layout":
            self.save('diagnostics,layout')

            msg = """```
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓__   _____  ___ ___ _    ___  _  _   _ _ _  ▓
▓\ \ / / _ \/ __|_ _| |  / _ \| \| | / | | | ▓
▓ \ V /|  _/\__ \| || |_| (_) | .` | | |_  _|▓
▓  |_| |_|  |___/___|____\___/|_|\_| |_| |_| ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓ | DOCK 1| DOCK 2|         ▓▓GUILD LICENSE▓▓▓
▓    ] [     ] [            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓  ___X_______X___     ______    _________   ▓
▓ |      =C=      |   |8 |9|0|  | ooo /\  |  ▓
▓ |   WORKSPACE   |___|7     |__| MESS    |  ▓
▓ |               ____     _____  ooo  0  |  ▓
▓ |    \----/     |   |_    1|  |_________|  ▓
▓ |    /MINE\     |   |6   |_|__|  WASH ~~|  ▓
▓ |    \----/     |   |5    ____   ROOM ~~|  ▓
▓ |_______________|   |4|3|2 |  |_|_|_|_|_|  ▓
▓        o↑           QUARTERS               ▓
▓       _o↓_          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓      X___|MINESHAFT ▓        ROSTER        ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 1 SONYA    6 MORGAN  ▓
▓-------LEGEND--------▓ 2 ASHRAF   7 RIE     ▓
▓  X    AIRLOCK       ▓ 3 DANA     8 ROSA    ▓
▓ =C=  COMPUTER       ▓ 4 JEROME   9 MIKE    ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 5 KANTARO  0 N/A     ▓
▓                     ▓                      ▓
▓  DOCK 1  ▓  DOCK 2  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓          ▓          ▓                      ▓
▓ HERACLES ▓ RESUPPLY ▓VERSION SOFTWARE 2.25B▓
▓          ▓          ▓                      ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  >DOWNLOAD     >BACK```"""
        elif step == "download":
            if save == 'diagnostics,layout':
                self.save('diagnostics,download')
                msg = """```
DOWNLOADING...
.
.
.
DOWNLOAD COMPLETE.

DIAGNOSTICS
         > LAYOUT
         > STATUS
         < BACK
```"""
            else:
                msg = False
        elif step == "back":
            if save == "diagnostics":
                self.save('init')
                msg = self.main_menu()
            else :
                self.save('diagnostics')
                msg = """```
 DIAGNOSTICS
     > LAYOUT
     > STATUS
     < BACK```"""

        elif step == "status":
            self.save('diagnostics,status')
            msg = """```
╔══════════════════════════════════════════════════╗           
║ WARNING: AIR FILTERS LAST REPLACED 455 DAYS AGO  ║
╟−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−╢ 
║          (255 DAYS PAST RECOMMENDATION)          ║
╠══════════════════════════════════════════════════╣
║ WARNING: SHOWER 5 OUT OF ORDER AS OF 1 DAY AGO   ║
╠══════════════════════════════════════════════════╣
║ WARNING: MINESHAFT ELEVATOR LAST MAINTAINED      ║
║          455 DAYS AGO                            ║
╟−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−╢
║          (255 DAYS PAST RECOMMENDATION)          ║
╠══════════════════════════════════════════════════╣
║ WARNING: AIRFLOW 82%                             ║
╟−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−╢
║ (SUBOPTIMAL: REPLACE FILTERS AND CHECK VENTS     ║
║  FOR BLOCKAGES)                                  ║
╠══════════════════════════════════════════════════╣
║ ALL SYSTEMS WITHIN ACCEPTABLE OPERATING          ║
║ CONDITIONS                                       ║
╚══════════════════════════════════════════════════╝
< BACK```"""

        return msg

    def schedule(self, step = ''):
        if step == '':
            self.save('schedule')
            return """```
SCHEDULE:
2255-07-02 06:33 - IMV GRASSHOPPER    - RESUPPLY - DOCKING BAY 2 - DOCK
2255-06-04 08:34 - RSV THE HERACLES   - RESEARCH - DOCKING BAY 1 - DOCK
2255-06-02 12:23 - CTV HORN OV PLENTY - RESUPPLY - DOCKING BAY 2 - DEPART
2255-06-01 16:04 - CTV HORN OV PLENTY - RESUPPLY - DOCKING BAY 2 - DOCK
2255-05-02 08:32 - MV VASQUEZ XV      - PICKUP   - DOCKING BAY 1 - DEPART
2255-05-01 06:02 - MV VASQUEZ XV      - PICKUP   - DOCKING BAY 1 - DOCK
2255-04-02 13:02 - CTV HORN OV PLENTY - RESUPPLY - DOCKING BAY 2 - DEPART
2255-04-01 15:54 - CTV HORN OV PLENTY - RESUPPLY - DOCKING BAY 2 - DOCK
2255-03-02 08:33 - MV VAZQUEZ XV      - PICKUP   - DOCKING BAY 1 - DEPART
2255-03-01 06:04 - MV VAZQUEZ XV      - PICKUP   - DOCKING BAY 1 - DOCK
< BACK```"""
        else:
            self.save('init')
            return self.main_menu()
