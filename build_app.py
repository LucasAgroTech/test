import os
import sys
import subprocess
import shutil
from datetime import datetime

def build_executable():
    """
    Script para empacotar o aplicativo Pipeline EMBRAPII SRInfo usando PyInstaller.
    """
    print("=" * 80)
    print("EMPACOTAMENTO DO PIPELINE EMBRAPII SRINFO")
    print("=" * 80)
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("\n1. Verificando ambiente...")
    
    # Verificar se o PyInstaller está instalado
    try:
        import PyInstaller
        print("   ✓ PyInstaller encontrado.")
    except ImportError:
        print("   ✗ PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("   ✓ PyInstaller instalado com sucesso.")
    
    # Verificar se o arquivo spec existe
    if not os.path.exists("pipeline.spec"):
        print("   ✗ Arquivo pipeline.spec não encontrado.")
        sys.exit(1)
    else:
        print("   ✓ Arquivo pipeline.spec encontrado.")
    
    # Verificar se o arquivo gui_main.py existe
    if not os.path.exists("gui_main.py"):
        print("   ✗ Arquivo gui_main.py não encontrado.")
        sys.exit(1)
    else:
        print("   ✓ Arquivo gui_main.py encontrado.")
    
    print("\n2. Limpando diretórios anteriores...")
    # Limpar diretórios anteriores
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"   ✓ Diretório {dir_name} removido.")
            except Exception as e:
                print(f"   ✗ Erro ao remover diretório {dir_name}: {str(e)}")
                sys.exit(1)
    
    print("\n3. Executando PyInstaller...")
    # Executar PyInstaller
    try:
        subprocess.run(["pyinstaller", "pipeline.spec"], check=True)
        print("   ✓ PyInstaller executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Erro ao executar PyInstaller: {str(e)}")
        sys.exit(1)
    
    # Verificar se o executável foi criado
    exe_path = os.path.join("dist", "pipeline_embrapii_srinfo")
    if os.path.exists(exe_path):
        print("\n4. Verificando o executável...")
        print(f"   ✓ Executável criado em: {os.path.abspath(exe_path)}")
    else:
        print("\n4. Verificando o executável...")
        print(f"   ✗ Executável não encontrado em: {os.path.abspath(exe_path)}")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("EMPACOTAMENTO CONCLUÍDO COM SUCESSO!")
    print("=" * 80)
    print(f"Finalizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"\nO executável está disponível em: {os.path.abspath(exe_path)}")
    print("\nPara executar o aplicativo:")
    print(f"1. Navegue até {os.path.abspath(exe_path)}")
    print("2. Execute o arquivo 'Pipeline EMBRAPII SRInfo.exe'")
    print("\nObservações:")
    print("- Certifique-se de que o arquivo .env está presente no mesmo diretório do executável")
    print("- O Microsoft Edge deve estar instalado no sistema para o WebDriver funcionar")
    print("=" * 80)

if __name__ == "__main__":
    build_executable()
