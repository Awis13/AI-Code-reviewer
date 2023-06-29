import openai

openai.api_key = "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"

# Function to read a file
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Function to write a file
def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

# Read the subject
subject = read_file('subject.txt')

# Send the subject to OpenAI for interpretation
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a student tasked to make tests for a following subject: " + subject},
        {"role": "assistant", "content": "Here are all tests and all edge cases for this subject in one main c function without any MD."},
    ]
)

# Write the assistant's response to 'test.c'
write_file('test.c', response['choices'][0]['message']['content'])
