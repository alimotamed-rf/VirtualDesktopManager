"""
Task Logger
Application Initializer
"""

import os
import json
import sys


class Initializer:

    @staticmethod
    def base_path():

        if getattr(sys, "frozen", False):

            return os.path.dirname(sys.executable)

        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                ".."
            )
        )


    @classmethod
    def initialize(cls):

        base = cls.base_path()

        config = os.path.join(
            base,
            "config"
        )

        data = os.path.join(
            base,
            "data"
        )

        os.makedirs(
            config,
            exist_ok=True
        )

        os.makedirs(
            data,
            exist_ok=True
        )

        settings = os.path.join(
            config,
            "settings.json"
        )

        if not os.path.exists(settings):

            with open(
                settings,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(

                    {
                        "tracked_roots": []
                    },

                    f,

                    indent=4

                )