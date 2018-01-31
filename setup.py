from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Mp_galafaleague",
    version = "1",
    description = "Projet application cloud",
    executables = [Executable("CloudAppMongo.py")],
)