import subprocess
import os
import sys

# --- Settings ---
REPO_URL = "https://github.com/ViduraVijerathne/hello-rasberry.git"
# URL එකෙන් repository එකේ නම ස්වයංක්‍රීයව ලබා ගැනීම
REPO_DIR = REPO_URL.split('/')[-1].replace('.git', '')


# --- Helper Function ---
def run_command(command, cwd=None):
    """
    Command එකක් run කර, එහි output එක සහ වැරදි (errors) print කිරීමට
    සහ command එක සාර්ථකද අසාර්ථකද යන්න return කිරීමට.
    """
    print(f"\n🚀 Running Command: {' '.join(command)}")
    try:
        # 'check=True' මගින් command එක fail වුවහොත් error එකක් raise කරයි
        # 'text=True' මගින් output එක string එකක් ලෙස ලබාදෙයි
        result = subprocess.run(
            command,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd  # Command එක run කළ යුතු directory එක (current working directory)
        )

        # සාර්ථක output එක පෙන්වීම
        if result.stdout:
            print("✅ Success Output:")
            print(result.stdout)

        # යම් warning එකක් හෝ stderr output එකක් ඇත්නම් පෙන්වීම
        if result.stderr:
            print("⚠️ Standard Error (Warnings):")
            print(result.stderr)

        return True  # Command එක සාර්ථකයි

    except subprocess.CalledProcessError as e:
        # Command එක fail වුවහොත්
        print(f"❌ Command Failed: {' '.join(command)}")
        print("--- Error Output ---")
        print(e.stderr)
        print("--- Standard Output (if any) ---")
        print(e.stdout)
        return False  # Command එක අසාර්ථකයි
    except FileNotFoundError:
        # 'git' හෝ 'python' වැනි command එකක් සොයාගත නොහැකි නම්
        print(f"❌ Error: '{command[0]}' command එක සොයාගත නොහැක.")
        print("   කරුණාකර 'Git' සහ 'Python' ඔබේ system PATH එකේ තිබේදැයි පරීක්ෂා කරන්න.")
        return False


# --- Main Logic ---
def main():
    # 1. Repository එක Clone කිරීම හෝ Pull කිරීම

    # 'sys.executable' මගින් ඔබ දැනට run කරන Python interpreter එකම භාවිතා කිරීම සහතික කරයි
    # මෙය virtual environments සමග වැඩ කිරීමේදී ඉතා වැදගත් වේ
    PYTHON_EXE = sys.executable

    if os.path.isdir(REPO_DIR):
        print(f"📂 '{REPO_DIR}' folder එක දැනටමත් තිබේ. Latest updates 'pull' කරමින්...")
        # REPO_DIR එක *තුළ* 'git pull' command එක run කිරීම
        if not run_command(["git", "pull"], cwd=REPO_DIR):
            print("❌ Git pull කිරීම අසාර්ථක විය. Program එක නතර කෙරේ.")
            return
    else:
        print(f"📥 Repository එක '{REPO_URL}' වෙතින් 'clone' කරමින්...")
        if not run_command(["git", "clone", REPO_URL]):
            print("❌ Git clone කිරීම අසාර්ථක විය. Program එක නතර කෙරේ.")
            return

    print("-" * 40)

    # 2. Dependencies Install කිරීම
    requirements_path = os.path.join(REPO_DIR, "requirements.txt")

    if os.path.isfile(requirements_path):
        print(f"📦 '{requirements_path}' file එකෙන් dependencies install කරමින්...")
        # 'pip' install command එක run කිරීම
        if not run_command([PYTHON_EXE, "-m", "pip", "install", "-r", requirements_path]):
            print("❌ Dependencies install කිරීම අසාර්ථක විය. Program එක නතර කෙරේ.")
            return
    else:
        print(f"🤷 'requirements.txt' file එක හමු නොවීය. Dependencies install කිරීම මඟ හැරේ.")

    print("-" * 40)

    # 3. main.py එක Run කිරීම
    main_py_path = os.path.join(REPO_DIR, "main.py")

    if os.path.isfile(main_py_path):
        print(f"▶️ '{main_py_path}' program එක run කරමින්...")
        # 'main.py' file එක, එය අඩංගු directory එක *තුළ* සිට run කිරීම
        # (එමගින් 'main.py' හට එහි ඇති අනෙකුත් files පහසුවෙන් access කළ හැක)
        if not run_command([PYTHON_EXE, "main.py"], cwd=REPO_DIR):
            print(f"❌ '{main_py_path}' run කිරීමේදී දෝෂයක් ඇතිවිය.")
    else:
        print(f"❌ Error: '{main_py_path}' file එක හමු නොවීය. Program එක run කළ නොහැක.")


if __name__ == "__main__":
    main()