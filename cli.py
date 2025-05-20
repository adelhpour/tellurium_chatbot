#!/usr/bin/env python3

from llm_service import llm_service

def run_cli():
    """
    Simple command-line chat loop. Type 'exit' or 'quit' to end.
    """
    history = []
    print(f"Tellurium Chatbot CLI (Model: {llm_service.get_model_name()}). Type 'exit' or 'quit' to end.\n")
    while True:
        try:
            prompt = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not prompt or prompt.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        # record user message
        history.append({"role": "user", "content": prompt})

        # send to your service
        print("Assistant is thinking…")
        reply = llm_service.send_message(prompt)

        # show and record assistant reply
        print(f"Assistant: {reply}\n")
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    run_cli()
