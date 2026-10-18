# Virtual Desktop Manager

A lightweight Windows desktop application for managing virtual desktops and tracking time spent on each workspace.

## Features

- **Workspace Management:** Create, switch between, rename, and remove Windows virtual desktops.
- **Automatic Time Tracking:** Track time spent on each virtual desktop as you work.
- **Live History:** View tracked time by date and desktop, with filtering options.
- **SQLite Database:** Store tracking history locally in a database.
- **Excel Reports:** Automatically generate an Excel report from the database.
- **System Tray:** Minimize the application to the system tray and keep tracking in the background.
- **Portable Application:** Run the packaged Windows executable without installing Python.

## How It Works

The application detects the active Windows virtual desktop and records the time spent on it. Tracking pauses when the workstation is locked.

SQLite is the single source of truth for tracking data. The application reads history from the database and generates the Excel report from the same data.

## Getting Started

### Option 1: Portable Executable

1. Download the Windows executable from the project's Releases page, when available.
2. Run the executable.
3. The application creates its database and Excel report alongside the executable.
4. Use the **WORKSPACES** tab to manage virtual desktops and the **HISTORY** tab to review tracked time.

### Option 2: Run from Source

Requirements: Windows, Python, and the dependencies listed in `requirements.txt`.

1. Clone or download this repository.
2. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Run the application:

   ```powershell
   python desktop_manager.py
   ```

## Data and Privacy

Tracking data is stored locally in `tracker.db`. The Excel report, `DesktopTimeTracker.xlsx`, is generated from the database. These files are created beside the application and are not intended to be committed to the repository.

## Technology Stack

- Python
- PySide6
- SQLite
- OpenPyXL
- PyVDA
- PyInstaller

## Platform

Windows 10/11.

## License

License information will be added once a project license has been selected.
