import subprocess
from app.cli.commands.base_response import CLIResponse

async def handle_command(session, command: str) -> CLIResponse:
    if command.strip() == "":
        return CLIResponse(output="")

    try:
        # Sicherheit: Keine schädlichen Kommandos zulassen
        if any(forbidden in command for forbidden in ["rm", "shutdown", "reboot", ":(){", "mkfs"]):
            return CLIResponse(output="Command blocked for safety.", error=True)

        result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=3)
        output = result.stdout.strip() or result.stderr.strip()
        return CLIResponse(output=output)
    except subprocess.TimeoutExpired:
        return CLIResponse(output="Command timeout", error=True)
    except Exception as e:
        return CLIResponse(output=f"Error: {str(e)}", error=True)
