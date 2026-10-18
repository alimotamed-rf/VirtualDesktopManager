"""
====================================================
WorkLogger
Main Application Entry Point

Author: Ali & ChatGPT
Version: 1.0.0 (Development)
====================================================
"""

from detector import Detector


def main():

    print("=" * 60)
    print("WorkLogger")
    print("Starting...")
    print("=" * 60)

    detector = Detector()

    detector.run()


if __name__ == "__main__":
    main()