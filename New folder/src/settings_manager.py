"""
Task Logger
Settings Manager
"""

import os
import json
import sys



class SettingsManager:


    def __init__(self):

        self.settings_file = self.get_settings_path()



    def get_base_path(self):

        if getattr(
            sys,
            "frozen",
            False
        ):

            return os.path.dirname(
                sys.executable
            )

        else:

            return os.path.abspath(

                os.path.join(

                    os.path.dirname(__file__),

                    ".."

                )

            )



    def get_settings_path(self):

        return os.path.join(

            self.get_base_path(),

            "config",

            "settings.json"

        )



    def load(self):

        if not os.path.exists(
            self.settings_file
        ):

            raise FileNotFoundError(

                "Settings file not found:\n"
                +
                self.settings_file

            )


        with open(

            self.settings_file,

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)



    def save(self, settings):

        os.makedirs(

            os.path.dirname(
                self.settings_file
            ),

            exist_ok=True

        )


        with open(

            self.settings_file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                settings,

                f,

                indent=4

            )



    def get_roots(self):

        settings = self.load()

        return settings.get(

            "tracked_roots",

            []

        )



    def set_roots(self, roots):

        self.save(

            {

                "tracked_roots": roots

            }

        )