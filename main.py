import subprocess, time
from agentspan.agents import AgentRuntime
from agent import auditor


def start_agentspan_server():
    """Starts the AgentSpan server in the background."""
    print("Checking AgentSpan Server...")
    subprocess.Popen(["agentspan", "server", "start"], stdout=subprocess.DEVNULL)
    time.sleep(3)
    return True

def run_audit():
    if not start_agentspan_server():
        return

    print("Audit Initiated...")
    with AgentRuntime() as rt:
        handler = rt.start(auditor, "Check AAPL and MSFT for June dividends.")
        print("Listening to Agent Stream... (Check browser at http://localhost:6767)\n")

        try:
            for event in handler.stream():
                print(f"Event:: {event.type} \n {event}\n")
                if event.type == "WAITING_FOR_APPROVAL":
                    print(f"\n[ACTION REQUIRED]: {event.payload.get('message', 'Approval needed')}")
                    choice = input("Approve this move? (yes/no): ").strip().lower()
                    
                    if choice in ['yes', 'y']:
                        handler.approve()
                        print("Move Approved. Sending back to agent...")
                    else:
                        handler.reject("User declined the trade.")
                        print("Move Rejected. Notifying agent...")
                
                elif event.type == "TOOL_CALL":
                    print(f" -> Agent is running tool: {event.payload.get('name')}")

                elif event.type == "DONE":
                    print(f"\n================ FINAL REPORT ================\n{event.output}")
                    break
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Error::",e)


if __name__ == "__main__":
    run_audit()