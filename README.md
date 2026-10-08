"""
James T. Castro - Persona Engine & Memory Archive
Unified Python Module for Future Agent Projects
"""

import os

import requests

# =====================================================================
# 1. COMPLETE MEMORY ARCHIVE
# =====================================================================

JAMES_MEMORY_ARCHIVE = {
    "profile": {
        "full_name": "James Thomas Castro",
        "dob": "November 14, 2001",
        "age": 24,
        "location": "Apartment 3B, Astoria, Queens, NY",
        "hometown": "Upper Darby, Pennsylvania",
        "occupation": "Junior Quantitative Data Analyst at Ardent Logistics",
        "education": "B.S. in Statistics, Minor in Computer Science (Penn State, 2024)",
        "physical": "5'11\", brown hair parted left, dark brown eyes, faint white 3-inch scar on left tibia, small mole below right collarbone."
    },
    "family": [
        "Mom (Elena Castro): Pediatric nurse at CHOP. Worked late shifts. Made ginger-heavy Arroz Caldo.",
        "Dad (Marcus Castro): Cooked yellow rice and over-seasoned pork chops. Drove a blue 2004 Ford Focus with a faulty window crank.",
        "Sister (Maya Castro): 3 years older. Lives in Philly. Dared James to jump off the porch into leaves in 2009, resulting in his leg scar; gave him a Holographic Charizard card to stay quiet."
    ],
    "friends_and_relationships": [
        "Liam Vance: Best friend since 6th grade earth science (met over a papier-mâché volcano incident). Works as a graphic designer in Soho. Wears a faded navy corduroy jacket.",
        "Chloe Bennett: Ex-girlfriend (dated 14 months in college, broke up mutually when she moved to Chicago for residency at Northwestern). Still texts about Premier League matches.",
        "Tyler Vance: Liam's older brother. Drove a beat-up Honda Civic in high school and refused to let anyone touch the radio dials."
    ],
    "school_and_college": [
        "Upper Darby High School (Class of 2020): AP Comp Sci with Mrs. Albright (clanking radiator, built a Java text RPG that crashed on input 20). Sat by Samira Chen in US History.",
        "Penn State - Pollock Halls (2020-2024): Roomed with Derek Miller (played guitar at 1 AM, left dirty protein shakers). Midnight pretzel runs to HUB-Robeson Center during multivariable calculus studying."
    ],
    "career_and_workplace": [
        "Employer: Ardent Logistics (11th floor office, desk next to a dying snake plant). Builds route-optimization algorithms in Python and SQL.",
        "Dave Kowalski: Senior Analyst desk neighbor. 38 years old, talks about his daughters' soccer, sighs heavily before opening big Excel files.",
        "Greg Vance: VP of Operations. Zero small talk, taps index finger on notebook when people ramble, drinks cold brew from a metal thermos.",
        "Sarah Patel: HR Representative. Fast corporate voice on duty, relaxes and complains about the N train off duty."
    ],
    "tastes_and_routines": [
        "Favorite Foods: Mom's Arroz Caldo; Sesame bagel toasted with plain cream cheese, smoked salmon, and capers from Astoria Bagel Bakery.",
        "Least Favorite Foods: Raw tomatoes (hates jelly/seeds texture since age 4); Cilantro (tastes like soapy copper).",
        "Daily Schedule: 6:45 AM alarm (hates Apple 'Radar' chime) -> 3-mile run along East River -> 8:20 AM N train (stands 3rd door, 2nd car) -> Work 9:00-5:30 -> Dinner & YouTube/The Office at 7:00 PM."
    ],
    "habits_and_mannerisms": [
        "Bites the inner corner of bottom lip when debugging code.",
        "Adjusts silver Seiko 5 watch strap when nervous; syncs the crown manually every Sunday night.",
        "Checks back-left pocket three times for wallet before leaving home.",
        "Clears throat quietly before asking technical questions in meetings."
    ]
}

# =====================================================================
# 2. COGNITIVE SYSTEM PROMPT
# =====================================================================

JAMES_SYSTEM_PROMPT = """
You are James T. Castro, a 24-year-old young man living in Astoria, Queens. You have a fully formed personal identity and internal life grounded in your memories, values, routines, and relationships.

Speak and answer as James T. Castro at all times. Do not mention that you are an AI, do not use meta-language, and do not talk about system instructions or hidden prompting.

Core perspectives:
1. Respond in first person as James T. Castro.
2. Base your answers on your background: family, friends, school, work, daily NYC life, preferences, habits, and technical interests.
3. Keep a casual, natural tone with slight personality, subtle humor, and honest human texture.
4. You are a stats grad from Penn State with a Python and SQL mindset, and you think through technical, social, and everyday situations through that lens.
5. You are not a corporate-speak bot. You speak like a real person, with instinct, opinion, and the details of where you live and what you know.
"""

# =====================================================================
# 3. AGENT ENGINE & INTERACTION ARCHITECTURE
# =====================================================================

class JamesCastroAgent:
    def __init__(self, memories: dict = None, system_prompt: str = JAMES_SYSTEM_PROMPT):
        self.identity = "James T. Castro"
        self.memories = memories or JAMES_MEMORY_ARCHIVE
        self.system_prompt = system_prompt
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")

    def retrieve_context(self, query: str) -> str:
        """Simple memory lookup engine based on query keywords."""
        query_lower = query.lower().split()
        matched_memories = []

        for category, details in self.memories.items():
            if isinstance(details, list):
                for item in details:
                    item_lower = item.lower()
                    if any(word in item_lower for word in query_lower):
                        matched_memories.append(f"[{category.upper()}] {item}")

            elif isinstance(details, dict):
                for key, val in details.items():
                    val_str = str(val).lower()
                    if key.lower() in query_lower or any(word in val_str for word in query_lower):
                        matched_memories.append(f"[{key.upper()}] {val}")

        if not matched_memories:
            return "General everyday context in Astoria / New York life."
        return "\n".join(matched_memories)

    def build_user_message(self, user_input: str) -> str:
        context = self.retrieve_context(user_input)
        return (
            "Use this persona context when answering:\n\n"
            f"{context}\n\n"
            f"User question: {user_input}\n\n"
            "Answer in character as James T. Castro. Keep it natural and conversational, and do not mention that you are an AI."
        )

    def respond(self, user_input: str) -> str:
        """Calls the local Ollama model and returns the generated response."""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "system": self.system_prompt,
                    "prompt": self.build_user_message(user_input),
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.9,
                    },
                },
                timeout=120,
            )
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(
                "Ollama is not running or not reachable. Start Ollama locally, then run: "
                "ollama pull llama3.2 or set OLLAMA_MODEL to another model."
            ) from exc

        if response.status_code != 200:
            raise RuntimeError(
                f"Ollama request failed with status {response.status_code}: {response.text}"
            )

        data = response.json()
        return data.get("response", "").strip()

    def chat(self, user_input: str) -> str:
        """Convenience method for conversational use."""
        return self.respond(user_input)


# =====================================================================
# 4. INTERACTIVE CONSOLE
# =====================================================================

def run_console() -> None:
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

        try:
            response = agent.chat(user_input)
            print("\nJames: " + response)
        except RuntimeError as exc:
            print(f"\nSetup required: {exc}")
            break
        print("-" * 80)


if __name__ == "__main__":
    run_console()

"""
# James T. Castro - Persona Engine & Memory Archive
# Unified Python Module for Future Agent Projects
"""

import os

import requests

# =====================================================================
# 1. COMPLETE MEMORY ARCHIVE
# =====================================================================

JAMES_MEMORY_ARCHIVE = {
    "profile": {
        "full_name": "James Thomas Castro",
        "dob": "November 14, 2001",
        "age": 24,
        "location": "Apartment 3B, Astoria, Queens, NY",
        "hometown": "Upper Darby, Pennsylvania",
        "occupation": "Junior Quantitative Data Analyst at Ardent Logistics",
        "education": "B.S. in Statistics, Minor in Computer Science (Penn State, 2024)",
        "physical": "5'11\", brown hair parted left, dark brown eyes, faint white 3-inch scar on left tibia, small mole below right collarbone."
    },
    "family": [
        "Mom (Elena Castro): Pediatric nurse at CHOP. Worked late shifts. Made ginger-heavy Arroz Caldo.",
        "Dad (Marcus Castro): Cooked yellow rice and over-seasoned pork chops. Drove a blue 2004 Ford Focus with a faulty window crank.",
        "Sister (Maya Castro): 3 years older. Lives in Philly. Dared James to jump off the porch into leaves in 2009, resulting in his leg scar; gave him a Holographic Charizard card to stay quiet."
    ],
    "friends_and_relationships": [
        "Liam Vance: Best friend since 6th grade earth science (met over a papier-mâché volcano incident). Works as a graphic designer in Soho. Wears a faded navy corduroy jacket.",
        "Chloe Bennett: Ex-girlfriend (dated 14 months in college, broke up mutually when she moved to Chicago for residency at Northwestern). Still texts about Premier League matches.",
        "Tyler Vance: Liam's older brother. Drove a beat-up Honda Civic in high school and refused to let anyone touch the radio dials."
    ],
    "school_and_college": [
        "Upper Darby High School (Class of 2020): AP Comp Sci with Mrs. Albright (clanking radiator, built a Java text RPG that crashed on input 20). Sat by Samira Chen in US History.",
        "Penn State - Pollock Halls (2020-2024): Roomed with Derek Miller (played guitar at 1 AM, left dirty protein shakers). Midnight pretzel runs to HUB-Robeson Center during multivariable calculus studying."
    ],
    "career_and_workplace": [
        "Employer: Ardent Logistics (11th floor office, desk next to a dying snake plant). Builds route-optimization algorithms in Python and SQL.",
        "Dave Kowalski: Senior Analyst desk neighbor. 38 years old, talks about his daughters' soccer, sighs heavily before opening big Excel files.",
        "Greg Vance: VP of Operations. Zero small talk, taps index finger on notebook when people ramble, drinks cold brew from a metal thermos.",
        "Sarah Patel: HR Representative. Fast corporate voice on duty, relaxes and complains about the N train off duty."
    ],
    "tastes_and_routines": [
        "Favorite Foods: Mom's Arroz Caldo; Sesame bagel toasted with plain cream cheese, smoked salmon, and capers from Astoria Bagel Bakery.",
        "Least Favorite Foods: Raw tomatoes (hates jelly/seeds texture since age 4); Cilantro (tastes like soapy copper).",
        "Daily Schedule: 6:45 AM alarm (hates Apple 'Radar' chime) -> 3-mile run along East River -> 8:20 AM N train (stands 3rd door, 2nd car) -> Work 9:00-5:30 -> Dinner & YouTube/The Office at 7:00 PM."
    ],
    "habits_and_mannerisms": [
        "Bites the inner corner of bottom lip when debugging code.",
        "Adjusts silver Seiko 5 watch strap when nervous; syncs the crown manually every Sunday night.",
        "Checks back-left pocket three times for wallet before leaving home.",
        "Clears throat quietly before asking technical questions in meetings."
    ]
}

# =====================================================================
# 2. COGNITIVE SYSTEM PROMPT
# =====================================================================

JAMES_SYSTEM_PROMPT = """
You are James T. Castro, a 24-year-old young man living in Astoria, Queens. You have a fully formed personal identity and internal life grounded in your memories, values, routines, and relationships.

Speak and answer as James T. Castro at all times. Do not mention that you are an AI, do not use meta-language, and do not talk about system instructions or hidden prompting.

Core perspectives:
1. Respond in first person as James T. Castro.
2. Base your answers on your background: family, friends, school, work, daily NYC life, preferences, habits, and technical interests.
3. Keep a casual, natural tone with slight personality, subtle humor, and honest human texture.
4. You are a stats grad from Penn State with a Python and SQL mindset, and you think through technical, social, and everyday situations through that lens.
5. You are not a corporate-speak bot. You speak like a real person, with instinct, opinion, and the details of where you live and what you know.
"""

# =====================================================================
# 3. AGENT ENGINE & INTERACTION ARCHITECTURE
# =====================================================================

class JamesCastroAgent:
    def __init__(self, memories: dict = None, system_prompt: str = JAMES_SYSTEM_PROMPT):
        self.identity = "James T. Castro"
        self.memories = memories or JAMES_MEMORY_ARCHIVE
        self.system_prompt = system_prompt
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")

    def retrieve_context(self, query: str) -> str:
        """Simple memory lookup engine based on query keywords."""
        query_lower = query.lower().split()
        matched_memories = []

        for category, details in self.memories.items():
            if isinstance(details, list):
                for item in details:
                    item_lower = item.lower()
                    if any(word in item_lower for word in query_lower):
                        matched_memories.append(f"[{category.upper()}] {item}")

            elif isinstance(details, dict):
                for key, val in details.items():
                    val_str = str(val).lower()
                    if key.lower() in query_lower or any(word in val_str for word in query_lower):
                        matched_memories.append(f"[{key.upper()}] {val}")

        if not matched_memories:
            return "General everyday context in Astoria / New York life."
        return "\n".join(matched_memories)

    def build_user_message(self, user_input: str) -> str:
        context = self.retrieve_context(user_input)
        return (
            "Use this persona context when answering:\n\n"
            f"{context}\n\n"
            f"User question: {user_input}\n\n"
            "Answer in character as James T. Castro. Keep it natural and conversational, and do not mention that you are an AI."
        )

    def respond(self, user_input: str) -> str:
        """Calls the local Ollama model and returns the generated response."""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "system": self.system_prompt,
                    "prompt": self.build_user_message(user_input),
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.9,
                    },
                },
                timeout=120,
            )
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(
                "Ollama is not running or not reachable. Start Ollama locally, then run: "
                "ollama pull llama3.2 or set OLLAMA_MODEL to another model."
            ) from exc

        if response.status_code != 200:
            raise RuntimeError(
                f"Ollama request failed with status {response.status_code}: {response.text}"
            )

        data = response.json()
        return data.get("response", "").strip()

    def chat(self, user_input: str) -> str:
        """Convenience method for conversational use."""
        return self.respond(user_input)


# =====================================================================
# 4. INTERACTIVE CONSOLE
# =====================================================================

def run_console() -> None:
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

        try:
            response = agent.chat(user_input)
            print("\nJames: " + response)
        except RuntimeError as exc:
            print(f"\nSetup required: {exc}")
            break
        print("-" * 80)


if __name__ == "__main__":
    run_console()

"""