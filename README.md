# James T. Castro Agent

This repository contains a lightweight persona-based AI agent inspired by the character profile and memory archive for James T. Castro.

## What this project includes
- A memory archive with personal background, relationships, habits, and work details
- A system prompt that frames the agent as James T. Castro
- A Python class (`JamesCastroAgent`) that builds context from a user query
- A simple terminal chat loop so you can interact with the agent locally

## Run it

```bash
python main.py
```

## Example interactions
- "Where do you work?"
- "Tell me about your friend Liam."
- "What are your favorite foods?"
- "What do you think about the N train?"

## Notes
This version is a self-contained, local prototype. It intentionally simulates the agent loop and can later be replaced with an actual LLM API integration (OpenAI, Anthropic, Azure, etc.).
