import json
with open('D:\CoT-is-all-you-need\ideas\gpt_vilt\chain-of-thought.json', 'r') as f:
    # count json items
    data = json.load(f)
    print(len(data))