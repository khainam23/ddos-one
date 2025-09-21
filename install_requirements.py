import subprocess
import sys

def install_package(package):
    """Cài đặt package qua pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    print("🔧 Installing required packages for Stealth DDoS...")
    print("=" * 50)
    
    packages = [
        "requests",
        "aiohttp",
        "urllib3",
        "flask"  # Cho web interface
    ]
    
    success_count = 0
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            success_count += 1
    
    print("=" * 50)
    print(f"✅ Installation completed: {success_count}/{len(packages)} packages installed")
    
    if success_count == len(packages):
        print("🎉 All packages installed successfully!")
        print("You can now run: python stealth_ddos.py")
    else:
        print("⚠️ Some packages failed to install. Please install them manually.")

if __name__ == "__main__":
    main()