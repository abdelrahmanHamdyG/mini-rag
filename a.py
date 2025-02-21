import cohere

co = cohere.Client("XL1OoRhBkXTTfeXYNiDF2wFhLFCQxJZhKkzxNmlO")
response = co.embed(
    model="embed-english-v3.0",
    texts=["Hello, world!"],
    input_type="search_document",
)
print(response.embeddings)