import os
import json


SETTINGS_FILE = "config/settings.json"


def load_roots():

    with open(SETTINGS_FILE, "r") as file:
        settings = json.load(file)

    return settings["tracked_roots"]



def find_project(path):

    if not path:
        return None


    roots = load_roots()


    for root in roots:

        root = os.path.normpath(root)
        path = os.path.normpath(path)


        if path.startswith(root):

            relative = os.path.relpath(path, root)


            if relative == ".":
                return None


            project = relative.split(os.sep)[0]


            return {
                "root": root,
                "project": project
            }


    return None