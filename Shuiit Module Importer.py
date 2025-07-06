import sys
import subprocess
import pkg_resources

required = {
    'kivymd==1.0.2',
    'cvzone',
    'mediapipe',
    'tensorflow==2.11.0'
}

# Normalize installed package names
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = {pkg for pkg in required if pkg.split('==')[0].lower() not in installed}

if missing:
    print("Installing missing modules...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
else:
    print("All required modules already installed.")

print("\nAll Shuiit modules successfully installed.")
