import subprocess



user_type = input( "Voulez-vous créer une salle (1) ou en rejoindre une (2)\n-> " )

if user_type == "1":
    subprocess.run( ["python3", "create.py"] )
else:
    subprocess.run( ["python3", "join.py"] )