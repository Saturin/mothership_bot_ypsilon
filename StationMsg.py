class StationMsg:
    msg_path = "./msg/"

    # ╠ ╣ ╗ ╚ ╔ ╝ ╦ ╩ ║ ╬ ═
    def _read_and_format(self, file: str):
        """
        read message file and  add apo's
        :param file:
        :return:
        """
        f = open(self.msg_path + file, encoding="utf8")
        a = f.read()
        a = """```""" + a + """```"""
        return a

    def hello(self):
        file = "hello.txt"
        return self._read_and_format(file)

    def menu_main(self):
        file = "menu_main.txt"
        return self._read_and_format(file)

    def menu_diagnostics(self):
        file = "menu_diagnostics.txt"
        return self._read_and_format(file)

    def layout(self):
        file = "layout.txt"
        return self._read_and_format(file)

    def diag_status(self):
        file = "diag_status.txt"
        return self._read_and_format(file)

    def download(self):
        return "DOWNLOADING... \n . \n . \n DOWNLOAD COMPLETE."

    def schedule(self):
        file = "schedule.txt"
        return self._read_and_format(file)

    def menu_controls(self):
        file = "menu_controls.txt"
        return self._read_and_format(file)

    def controls_airlock(self, airlock_docking_bay_1 , airlock_docking_bay_2 , airlock_mineshaft ):
        """
        #airlock_docking_bay_1#
        #airlock_docking_bay_2#
        #airlock_mineshaft#
        :return:
        """
        file = "airlocks.txt"
        txt = self._read_and_format(file)
        txt = txt.replace("#airlock_docking_bay_1#", "UNLOCK" if airlock_docking_bay_1 else "LOCK")
        txt = txt.replace("#airlock_docking_bay_2#", "UNLOCK" if airlock_docking_bay_2 else "LOCK")
        txt = txt.replace("#airlock_mineshaft#", "UNLOCK" if airlock_mineshaft else "LOCK")
        return txt

    def controll_system(self, auth):
        if auth:
            file = "system_auth.txt"
        else:
            file = "system_no_auth.txt"
        return self._read_and_format(file)

    def controll_shower(self, shower_1,shower_2,shower_3,shower_4,shower_5):
        file = "showers.txt"
        txt = self._read_and_format(file)
        txt = txt.replace("#shower_1#", "UNLOCK" if shower_1 else "LOCK")
        txt = txt.replace("#shower_2#", "UNLOCK" if shower_2 else "LOCK")
        txt = txt.replace("#shower_3#", "UNLOCK" if shower_3 else "LOCK")
        txt = txt.replace("#shower_4#", "UNLOCK" if shower_4 else "LOCK")
        txt = txt.replace("#shower_5#", "UNLOCK" if shower_5 else "LOCK")

        return txt

    def lifesupport(self, life_support):
        file = "lifesupport.txt"
        txt = self._read_and_format(file)
        txt = txt.replace("#life_support#", str(life_support))
        return txt

    def scuttle(self):
        file = "scuttle.txt"
        return self._read_and_format(file)

    def autodestruction(self):
        file = "autodestruction.txt"
        return self._read_and_format(file)

    def roster(self):
        file = "roster.txt"
        return self._read_and_format(file)

    def comms_menu(self):
        file = "menu_comms.txt"
        return self._read_and_format(file)

    def comms_heracles(self):
        file = "heracles.txt"
        return self._read_and_format(file)

    def comms_grasshoper(self):
        file = "grasshopper.txt"
        return self._read_and_format(file)

    def syntax_error(self):
        file = "syntax_error.txt"
        return self._read_and_format(file)

    def admin_msg(self, auth):
        if auth is True:
            file = "admin_hello.txt"
        else:
            file = 'bye_admin.txt'

        return self._read_and_format(file)