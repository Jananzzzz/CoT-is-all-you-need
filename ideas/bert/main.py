import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the pre-trained T5 model and tokenizer
model_name = "mrm8488/t5-base-finetuned-question-generation-ap"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Set the model to device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print("Model is set to device: ", device)

# Function to generate questions from image captions
def generate_questions(caption):
    # Preprocess the input caption
    input_text = "generate questions: " + caption.strip() + " </s>"

    # Tokenize the input text
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)

    # Generate questions
    outputs = model.generate(
        input_ids=input_ids,
        max_length=64,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        num_return_sequences=20,
        early_stopping=True,
    )

    # Decode the generated questions
    generated_questions = []
    for output in outputs:
        output_text = tokenizer.decode(output, skip_special_tokens=True)
        generated_questions.append(output_text)

    for i in generated_questions:
        print(i[10:])

print("Generating questions...")
generate_questions("This photo is taken looking through the catcher’s glove.")
