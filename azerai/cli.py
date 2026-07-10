"""
AzerAI Console - CLI Giriş Nöqtəsi
"""
try:
    from .azerai import server, LIVEKIT_AGENT_NAME
except ImportError:
    from .azerai.azerai import server, LIVEKIT_AGENT_NAME

from livekit.agents import cli

try:
    from .auto_run import run_manager_script_in_background
except ImportError:
    try:
        from .azerai.auto_run import run_manager_script_in_background
    except ImportError:
        run_manager_script_in_background = None

def main():
    import sys
    if run_manager_script_in_background and any(arg in sys.argv for arg in ["start", "dev"]):
        run_manager_script_in_background(target_agent=LIVEKIT_AGENT_NAME)
    cli.run_app(server)

if __name__ == "__main__":
    main()
