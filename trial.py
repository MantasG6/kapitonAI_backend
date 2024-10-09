from groq import Groq

client = Groq()
completion = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "How can you help me?"
        }
    ],
    temperature=1,
    max_tokens=8000,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
