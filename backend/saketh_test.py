import re

def escape_newlines(code):
    return code.replace('print("\n', 'print("\\n')

def extract_code_from_mdd(markdown_text: str) -> str: 
    pattern = r'```(?:python)?\n(.*?)```'
    code_blocks = re.findall(pattern, markdown_text, re.DOTALL)
    
    result = '\n'.join(block.strip() for block in code_blocks)
    
    return result

text = """

```python
def Hello():
    print("\nHello")
```
"""


import re

def extract_code_from_md(markdown_text):
    pattern = r'```(?:python)?\n(.*?)```'
    code_blocks = re.findall(pattern, markdown_text, re.DOTALL)
    
    result = '\n'.join(block.replace('print("\n', 'print("\\n') for block in code_blocks)
    
    return result


print(extract_code_from_md(text))