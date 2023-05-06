print("enter your multiline text:")
lines = []
while True:
    line = input()
    if line:
        lines.append(line)
    else:
        break

multiline_text = '\n'.join(lines)
print(multiline_text)
