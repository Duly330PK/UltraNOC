from app.cli.commands.base_response import CLIResponse

async def handle_command(session, command: str) -> CLIResponse:
    cmd = command.strip().lower()

    if session.mode == "exec":
        if cmd == "enable":
            session.mode = "privileged"
            session.prompt = "#"
            return CLIResponse(output="Entering privileged mode")
        elif cmd == "show ip interface brief":
            return CLIResponse(output=(
                "Interface              IP-Address      OK? Method Status                Protocol\n"
                "GigabitEthernet0/0     10.0.0.1        YES manual up                    up"
            ))
        elif cmd == "conf t":
            session.mode = "config"
            session.prompt = "(config)#"
            return CLIResponse(output="Enter configuration mode")
        else:
            return CLIResponse(output="Unknown command", error=True)

    elif session.mode == "config":
        if cmd.startswith("interface"):
            intf = cmd.split()[-1]
            session.push_context(f"interface {intf}")
            session.mode = "config-if"
            session.prompt = f"(config-if-{intf})#"
            return CLIResponse(output=f"Configuring interface {intf}")
        elif cmd == "exit":
            session.mode = "exec"
            session.prompt = ">"
            session.context_stack = []
            return CLIResponse(output="Exiting config mode")
        else:
            return CLIResponse(output="Command not supported in config mode", error=True)

    elif session.mode.startswith("config-if"):
        if cmd.startswith("ip address"):
            return CLIResponse(output=f"IP address assigned")
        elif cmd == "no shutdown":
            return CLIResponse(output="Interface enabled")
        elif cmd == "exit":
            session.pop_context()
            session.mode = "config"
            session.prompt = "(config)#"
            return CLIResponse(output="Returning to config mode")
        else:
            return CLIResponse(output="Unsupported interface command", error=True)

    return CLIResponse(output="Invalid state", error=True)
