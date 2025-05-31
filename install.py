import os
import subprocess
import sys
import venv

def create_virtualenv(env_name="venv"):
    if not os.path.isdir(env_name):
        print("[+] Creating virtual environment...")
        venv.create(env_name, with_pip=True)
    else:
        print("[✓] Virtual environment already exists.")

def install_requirements(env_name="venv"):
    pip_path = os.path.join(env_name, "Scripts" if os.name == "nt" else "bin", "pip")
    
    if not os.path.isfile("requirements.txt"):
        print("[!] requirements.txt not found.")
        return
    
    print("[+] Installing dependencies from requirements.txt...")
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
    print("[✓] All dependencies installed.")

def run_lima():
    print("\n[✓] LIMA is set up. You can now run it using:")
    print("    source venv/Scripts/activate" if os.name == "nt" else "    source venv/bin/activate")
    print("    python main.py\n")

def main():
    print("==== LIMA SETUP STARTED ====")
    create_virtualenv()
    install_requirements()
    run_lima()
    print("==== LIMA SETUP COMPLETE ====")

if __name__ == "__main__":
    main()
