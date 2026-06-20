def split_text(text: str, chunk_size: int = 800) -> list[str]:

    chunks = []

    current_chunk = ""

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if len(current_chunk) + len(line) > chunk_size:
            chunks.append(current_chunk)

            current_chunk = line

        else:
            current_chunk += "\n" + line

    if current_chunk:

        chunks.append(current_chunk)

    return chunks
