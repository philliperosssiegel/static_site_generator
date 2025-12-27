def markdown_to_blocks(markdown: str):
    markdown_blocks = []
    for block in markdown.split("\n\n"): #presumed that all input markdown is "well-formed" --> double newline block separation
        clean_block = block.strip()
        if not (clean_block in ["", "\n"]):
            markdown_blocks.append(clean_block)
    
    return markdown_blocks