import ollama

batch=ollama.embed(
    model='embeddinggemma',
    input=[
        'The quick brown fox jumps over the lazy dog.',
        # 'The five boxing wizards jump quickly.',
        # 'Jackdaws love my big sphinx of quartz.',
    ]
)

print(batch.embeddings)