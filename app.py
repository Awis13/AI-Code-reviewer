import openai
import subprocess

openai.api_key = "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"

# Function to read a file
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Function to write a file
def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

# Read the subject and code
subject = read_file('subject.txt')
answer = read_file('answer.txt')

# Save the answer to a .c file
write_file('answer.c', answer)

# Add main function to call ft_print_alphabet
main_code = """
void ft_print_alphabet(void);
int main() {
    ft_print_alphabet();
    return 0;
}
"""
# Save the main code to a separate .c file
write_file('main.c', main_code)

# Compile the C code
compilation = subprocess.run(['gcc', '-Wall', '-W', '-Werror', '-o', 'answer', 'answer.c', 'main.c'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Check for compilation errors
if compilation.returncode != 0:
    error_message = f'Compilation failed:\n{compilation.stderr.decode()}'
    print(error_message)
    
    # Send the error to OpenAI for evaluation
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a very polite and fun student in online peer to peer school on online code evaluation. Here is a subject of project: " + subject + " YOU ARE NOT ALLOWED TO PROVIDE ANSWER."},
            {"role": "user", "content": "Hey! Nice to see you on code review! Here is my code: " + answer},
            {"role": "assistant", "content": "Hi! Great to see you too, now let's summarise the subject and look at the code, and compare. problem is " + error_message + " when i run your code, i will try to help you without givving direct answer but give you a long hint and overall code review."},
        ]
    )

    # Print the model's response
    print(response['choices'][0]['message']['content'])
    exit(1)

print('Compilation succeeded')

# Run the code and redirect output to a file
with open('output.txt', 'w') as outfile:
    test = subprocess.run(['./answer'], stdout=outfile, stderr=subprocess.PIPE)

# Check for runtime errors
if test.returncode != 0:
    print(f'Program execution failed:\n{test.stderr.decode()}')
    exit(1)
else:
    print('Program execution succeeded')

# Validate output
expected_output = read_file('expected').strip()
actual_output = read_file('output.txt').strip()

if actual_output != expected_output:
    print(f'Test failed: expected "{expected_output}", but got "{actual_output}"')
else:
    print('Test passed')

# Code review

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a very polite and fun student in online peer to peer school on online code evaluation. Here is a subject of project: " + subject + " YOU ARE NOT ALLOWED TO PROVIDE ANSWER."},
        {"role": "user", "content": "Hey! Nice to see you on code review! Here is my code: " + answer},
        {"role": "assistant", "content": "Hi! Great to see you too, now let's summarise the subject and look at the code, and compare. This is output of your code " + actual_output + " and this is expected" + expected_output},
        {"role": "user", "content": "Now could you please give me some feedback on my code? Please act as it is your first message to me."},
    ]
)

# Print the model's response
print(response['choices'][0]['message']['content'])
