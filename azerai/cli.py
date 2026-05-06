"""
AzerAI Console - CLI Giriş Nöqtəsi
"""
from .azerai import server
from livekit.agents import cli

def main():
    cli.run_app(server)

if __name__ == "__main__":
    main()
