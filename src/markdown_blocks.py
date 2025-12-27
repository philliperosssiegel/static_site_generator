from enum import Enum
from functools import reduce

class BlockType(Enum):
    PARAGRAPH = "paragraph",
    HEADING = "heading",
    CODE = "code",
    QUOTE = "quote",
    UNORDERED_LIST = "unordered_list",
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block: str) -> BlockType:
    reduce_and = lambda x, y: x and y
    try:

        if (reduce(reduce_and, [char=="#" for char in markdown_block.split()[0]])):
            return BlockType.HEADING
        elif (markdown_block[:3] == "```" and markdown_block[-3:] == "```"):
            return BlockType.CODE
        elif (reduce(reduce_and, [line[0]==">" for line in markdown_block.split("\n")])):
            return BlockType.QUOTE
        elif (reduce(reduce_and, [line[:2]=="- " for line in markdown_block.split("\n")])):
            return BlockType.UNORDERED_LIST
        # elif (reduce(reduce_and, [line[0].isdigit() and line[1:3]==". " for line in markdown_block.split("\n")])):
        #     for char in [line[0] for line in markdown_block.split("\n")]:
        previous_num = None
        is_ordered = True

        for line in markdown_block.split("\n"):
            # require ". " to even consider it ordered
            if ". " not in line:
                is_ordered = False
                break

            num_section = line.split(". ")[0]

            if num_section.isdigit():
                num_section = int(num_section)
                if previous_num is None:
                    if num_section == 1:
                        previous_num = num_section
                    else:
                        is_ordered = False
                        break
                else:
                    if num_section == previous_num + 1:
                        previous_num = num_section
                    else:
                        is_ordered = False
                        break
            else:
                is_ordered = False
                break

        if is_ordered:
            return BlockType.ORDERED_LIST

        return BlockType.PARAGRAPH

    except Exception:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str):
    markdown_blocks = []
    for block in markdown.split("\n\n"): #presumed that all input markdown is "well-formed" --> double newline block separation
        clean_block = block.strip()
        if not (clean_block in ["", "\n"]):
            markdown_blocks.append(clean_block)
    
    return markdown_blocks