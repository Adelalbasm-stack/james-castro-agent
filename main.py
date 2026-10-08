from james_castro_agent import JamesCastroAgent


def main() -> None:
    agent = JamesCastroAgent()
    print("James T. Castro Agent is live.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit", "bye"}:
            print("James: See you later. I'm heading back to Astoria.")
            break

        if not user_input:
            continue

        response = agent.chat(user_input)
        print("\n" + response)
        print("-" * 80)


if __name__ == "__main__":
    main()
