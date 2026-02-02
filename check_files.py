import os

def list_my_files():
    # Folders we want to look at
    folders_to_show = ['auth', 'email_engine', 'config', 'database']
    files_in_root = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    print("--- PROJECT STRUCTURE ---")
    for f in files_in_root:
        print(f"  [Root] -> {f}")
        
    for folder in folders_to_show:
        if os.path.exists(folder):
            print(f"\n  [{folder}/]")
            for f in os.listdir(folder):
                if not f.startswith('__pycache__'):
                    print(f"    |-- {f}")

if __name__ == "__main__":
    list_my_files()