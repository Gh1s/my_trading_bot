from cx_Freeze import setup, Executable
import sys

# On appelle la fonction setup
setup(
    name = "trading-bot",
    version = "1",
    description = "My first trading bot",
    executables = [Executable("main.py")],
)
