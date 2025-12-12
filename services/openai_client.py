from openai import OpenAI

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 # Mets ta clé ici

def call_openai(prompt: str, model="gpt-4o-mini"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Tu réponds en français, clair et structuré."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erreur OpenAI : {e}"
