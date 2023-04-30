from transformers import T5Tokenizer, T5ForConditionalGeneration

# Define the question and answer pair
question = "Where is the cat sleeping?"
answer = "On the sofa."

# Initialize the T5 tokenizer and model
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')

# Format the input as a T5 task
input_str = 'summarize: ' + question + ' answer: ' + answer

# Tokenize the input and generate the summary
input_ids = tokenizer.encode(input_str, return_tensors='pt')
output_ids = model.generate(input_ids)

# Decode the summary output and print it
summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print(summary)  # Output: "The cat is sleeping on the sofa."