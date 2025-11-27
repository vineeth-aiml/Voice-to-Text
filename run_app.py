import subprocess, sys
from pathlib import Path

def main():
    app_path = Path("app/ui/main.py").resolve()
    subprocess.call([sys.executable, "-m", "streamlit", "run", str(app_path)])

if __name__ == "__main__":
    main()
