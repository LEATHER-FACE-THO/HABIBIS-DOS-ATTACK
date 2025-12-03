import os
import sys
import subprocess
import shutil

def compile_project():
    print("🚀 Iniciando compilación del proyecto...")
    
    try:
        import PyInstaller
    except ImportError:
        print("📥 Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    main_file = "THO DOS WEB.py"
    icon_path = os.path.join("assets", "icon.ico")
    
    if not os.path.exists(icon_path):
        print("❌ Error: No se encuentra el archivo icon.ico en la carpeta assets")
        return
    
    compile_command = [
        "pyinstaller",
        "--noconfirm",  
        "--onefile",    
        "--noconsole",  
        "--icon=" + icon_path,
        "--add-data", "assets/*;assets",  
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui",
        "--hidden-import=PySide6.QtWidgets",
        "--name=THO_DOS_ATTACK",
        main_file
    ]
    
    print("🔨 Compilando el proyecto...")
    try:
        subprocess.run(compile_command, check=True)
        
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("THO_DDS_ATTACK.spec"):
            os.remove("THO_DOS_ATTACK.spec")
            
        print("\n✅ Compilación completada exitosamente!")
        print("📁 El ejecutable se encuentra en la carpeta 'dist' como 'THO_HABIBIS_DOS_ATTACK.exe'")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la compilación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    compile_project()

