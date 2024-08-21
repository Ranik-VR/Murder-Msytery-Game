from openai import OpenAI

client = OpenAI(api_key="API Security Key")


# Generate the next line in a conversation
def text_generation(conversation):
    response = client.chat.completions.create(
        messages=conversation,
        model="gpt-4o",
        max_tokens=200,
        # frequency_penalty=0.0,          # Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
        # presence_penalty=0.0,           # Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
        # temperature=1.0,                # What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
        # seed=0
    )
    response_text = response.choices[0].message.content
    return response_text


