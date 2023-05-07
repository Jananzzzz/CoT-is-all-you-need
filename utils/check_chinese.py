import re

def contains_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fff]')  # Unicode range for Chinese characters
    return bool(re.search(pattern, text))

# Example usage
text1 = "Hello, 你好!"
text2 = "This is a test."
text3 = "hafsdojhas d, asdfjk as;ldfkj, asfdhjl akjsdfal , sjkdfja, afsdkjk , thisi s a a googd guy,.咖啡。jkjjfaksd ."

print(contains_chinese(text1))  # True
print(contains_chinese(text2))  # False
print(contains_chinese(text3))  # True
