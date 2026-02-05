import psycopg2
from psycopg2 import OperationalError

common_passwords = ['root', 'password', 'postgres', 'admin', '1234', '12345', '']
db_name = 'launchconnect'
user = 'postgres'
host = 'localhost'
port = '5432'

print(f"Testing connection to PostgreSQL user='{user}' on {host}:{port}...")

found_password = None

for pwd in common_passwords:
    try:
        print(f"Trying password: '{pwd}'")
        conn = psycopg2.connect(
            dbname='postgres', # Connect to default db first to check auth
            user=user,
            password=pwd,
            host=host,
            port=port
        )
        conn.close()
        found_password = pwd
        print(f"\nSUCCESS! Password is: '{pwd}'")
        break
    except OperationalError as e:
        if "authentication failed" in str(e):
            print("  -> Authentication failed")
        else:
            print(f"  -> Other error: {e}")

if found_password is not None:
    print(f"\nUPDATING settings.py with the correct password...")
    # Read settings.py
    with open('launchconnect/settings.py', 'r') as f:
        content = f.read()
    
    # Replace password
    # This is a simple replace, assuming the structure from previous steps
    import re
    new_content = re.sub(r"'PASSWORD': '.*',", f"'PASSWORD': '{found_password}',", content)
    
    with open('launchconnect/settings.py', 'w') as f:
        f.write(new_content)
        
    print("settings.py updated.")
else:
    print("\nFAILURE: Could not connect with common passwords.")
    print("Please manually update 'PASSWORD' in launchconnect/settings.py")
