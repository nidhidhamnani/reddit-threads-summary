from anthropic import Anthropic

client = Anthropic(api_key="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")

def get_prompt_for_style(text, style):
    base_intro = "Summarize the following Reddit thread (title, post, and top comments)"

    if style == "Neutral":
        prompt = f"{base_intro} in a clear and concise way while preserving the key information:\n\n{text}"
    elif style == "Funny / Commentary":
        prompt = f"{base_intro}, but make it funny, sarcastic, or meme-like. Channel a humorous Redditor:\n\n{text}"
    elif style == "Analytical":
        prompt = f"{base_intro} by breaking down arguments, viewpoints, and extracting key takeaways. Think like a journalist or analyst:\n\n{text}"
    elif style == "Poetic":
        prompt = f"{base_intro}, but rewrite it in a poetic or lyrical form — a Reddit thread turned into verse:\n\n{text}"
    else:
        prompt = f"{base_intro}:\n\n{text}"

    return prompt

def summarize_text(text, style, max_tokens=500):
    prompt = get_prompt_for_style(text, style)

    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=max_tokens,
        temperature=0.3,
        system="Provide a concise summary of the text.",
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text
