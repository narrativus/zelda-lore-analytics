import os

import openai


class LoreAnalyzer:
    def __init__(self, model="gpt-4o-mini"):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def prompt(self, excerpt: str, theme: str) -> dict:
        system = f"You are a Zelda lore expert. Identify any references to {theme}."
        user = f'Text:\n"""\n{excerpt}\n"""'
        return (
            self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                response_format={"type": "json_object"},
                max_tokens=200,
            )
            .choices[0]
            .message.json()
        )
