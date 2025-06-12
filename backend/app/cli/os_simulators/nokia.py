from app.cli.commands.base_response import CLIResponse

async def handle_command(session, command: str) -> CLIResponse:
    cmd = command.strip().lower()

    if session.mode == "exec":
        if cmd == "enable-admin":
            session.mode = "config"
            session.prompt = "[admin@base]>"
            return CLIResponse(output="Admin mode enabled")
        elif cmd == "show router interface":
            return CLIResponse(output=(
                "Interface     Admin Oper Address         MTU  Encapsulation\n"
                "to-pe1        Up    Up    192.168.0.1     1500 null"
            ))
        elif cmd == "configure router":
            session.mode = "router-config"
            session.prompt = "[admin@router]#"
            return CLIResponse(output="Router configuration mode")
        else:
            return CLIResponse(output="Unrecognized command", error=True)

    elif session.mode == "router-config":
        if cmd.startswith("interface"):
            return CLIResponse(output="Entering interface context (simulated)")
        elif cmd.startswith("area"):
            return CLIResponse(output="OSPF area set")
        elif cmd == "exit":
            session.mode = "exec"
            session.prompt = ">"
            return CLIResponse(output="Exited configuration mode")
        else:
            return CLIResponse(output="Unknown router command", error=True)

    return CLIResponse(output="Unsupported or invalid command context", error=True)
