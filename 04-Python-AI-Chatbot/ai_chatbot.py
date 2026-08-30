import os
from datetime import datetime
from openai import OpenAI


MODEL = "gpt-5.6-luna"

SYSTEM_PROMPT = """
You are Avinash AI Assistant.

You specialize in:
- IT Infrastructure
- Windows Server
- Active Directory
- Microsoft Azure
- AWS
- DevOps
- Docker
- Kubernetes
- Terraform
- Ansible
- Python
- Generative AI

Give clear, practical and technically accurate answers.
Explain commands when appropriate.
"""


def show_banner():
    print("=" * 70)
    print("              AVINASH PYTHON AI ASSISTANT")
    print("=" * 70)
    print(f"Model : {MODEL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("Commands:")
    print("  /clear   Clear conversation")
    print("  /help    Show commands")
    print("  /exit    Exit chatbot")
    print("=" * 70)


def check_api_key():
    if not os.getenv("OPENAI_API_KEY"):
        print("\nERROR: OPENAI_API_KEY is not configured.")
        print("Configure it in PowerShell before running the chatbot.")
        return False

    return True


def show_help():
    print("\nAvailable commands:")
    print("/clear  - Clear conversation history")
    print("/help   - Display available commands")
    print("/exit   - Close the chatbot")


def main():

    show_banner()

    if not check_api_key():
        return

    client = OpenAI()

    previous_response_id = None

    while True:

        try:
            user_input = input("\nYou > ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["/exit", "exit", "quit"]:
                print("\nAI > Goodbye! Chat session closed.")
                break

            if user_input.lower() == "/help":
                show_help()
                continue

            if user_input.lower() == "/clear":
                previous_response_id = None
                print("\nConversation history cleared.")
                continue

            print("\nAI > Thinking...")

            request = {
                "model": MODEL,
                "instructions": SYSTEM_PROMPT,
                "input": user_input,
            }

            if previous_response_id:
                request["previous_response_id"] = previous_response_id

            response = client.responses.create(**request)

            answer = response.output_text

            previous_response_id = response.id

            print("\nAI >", answer)

        except KeyboardInterrupt:

            print("\n\nChat session stopped.")
            break

        except Exception as error:

            print("\nERROR:", error)


if __name__ == "__main__":
    main()