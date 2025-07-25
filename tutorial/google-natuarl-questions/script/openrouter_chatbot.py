from openai import OpenAI

if __name__ == "__main__":
    # Suggest: change to os.getenv() read api_key
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )

    # Prepare context and query
    context = """[1] Question: who produces the most wool in the world
    Answer: Wool Global wool production is about 2 million tonnes per year, of which 60% goes into apparel. 
    Wool comprises ca 3% of the global textile market, but its value is higher owing to dying and other modifications of the material.
    [1] Australia is a leading producer of wool which is mostly from Merino sheep but has been eclipsed by China in terms of total weight.
    [30] New Zealand (2016) is the third-largest producer of wool, and the largest producer of crossbred wool. 
    Breeds such as Lincoln, Romney, Drysdale, and Elliotdale produce coarser fibers, and wool from these sheep is usually used for making carpets.
    """

    query = "who produces the most wool in the world"

    # vuild prompt format
    prompt = f"""Context:
    {context}

    Question:
    {query}

    Answer:
    """

    completion = client.chat.completions.create(
        model="qwen/qwen3-coder:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    print("Answer:\n", completion.choices[0].message.content)
