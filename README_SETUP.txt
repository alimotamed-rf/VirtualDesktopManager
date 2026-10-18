VIRTUAL DESKTOP TIME TRACKER
============================

Required:
- Windows 10
- Python 3.14.7
- Microsoft Excel
- Internet access only for installing Python packages

Install dependencies:
    python -m pip install -r requirements.txt

Create database:
    python database.py

Create Excel report:
    python excel_report.py

Test Windows lock detection:
    python lock_test.py

Run tracker:
    python desktop_tracker.py

Files generated automatically:
    tracker.db
    DesktopTimeTracker.xlsx

Current functionality:
- Tracks active Windows Virtual Desktop
- Uses desktop names
- Empty desktop names become "Desktop N"
- Multiple desktops with the same name accumulate into one record
- SQLite persistent daily storage
- Live Excel report
- Excel updates every 5 seconds
- Excel can remain open while the tracker updates it
- Current session is saved on Ctrl+C
- Windows lock pauses timing
- Windows unlock resumes timing

IMPORTANT:
The current project is the completed time-tracking component.
The later "Task Workspace Manager" features (senior dashboard,
task assignment, automatic desktop creation, task-controlled
desktop closure, archive workflow) have been designed but
have NOT yet been implemented in these files.
