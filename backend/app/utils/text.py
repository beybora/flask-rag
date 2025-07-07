def split_text(text, chunk_size=1000, chunk_overlap=20):
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        
        if end == text_length:
            break
        
        start = end - chunk_overlap

    return chunks
