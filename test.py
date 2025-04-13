import openai

# Make sure to replace this with your actual OpenAI API key
client = openai.OpenAI(api_key="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")

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": "Tell me a joke"}],
    max_tokens=200
)

print(response.choices[0].message.content)
