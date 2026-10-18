"""
WorkLogger
Path Resolver
"""

import os



def find_file_in_roots(filename, roots):

    for root in roots:

        for folder, _, files in os.walk(root):

            if filename in files:

                return os.path.join(
                    folder,
                    filename
                )


    return None