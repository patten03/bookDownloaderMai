# BookDownloaderMai

## Requirements

- Python 3.12.0
- pip 23.2.1

## Dependencies

- pillow 10.4.0
- pyinstaller 6.10.0
- beautifulsoup4 4.12.3
- requests 2.32.3

## Build

Make virtual environment for project:

```powershell
python -m venv ./.venv
```

Activate virtual environment, for instance by powershell file:

```powershell
.\.venv\Scripts\Activate.ps1
```

Check is virtual environment working correctly by checking python location:

```powershell
where.exe python
```

If you see this line, virtual environment was made successefully

```powershell
{path-to-project}\bookDownloaderMai\.venv\Scripts\python.exe
```

Next install all libraries:

```powershell
pip install requests;
pip install beautifulsoup4;
pip install pillow;
pip install pyinstaller;
```

Not necessary step, but if want to build .exe file, use this command:

```powershell
pyinstaller.exe --name=BookStealer --onefile --icon=Blu_Eye.ico main.py
```
