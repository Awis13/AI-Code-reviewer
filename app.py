from flask import Flask, request, render_template
import openai
import subprocess

app = Flask(__name__)

openai.api_key = "sk-xxxxxx"

# Function to read a file
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Function to write a string to a file
def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def run_c_code(subject, answer):
    # Initialize all variables
    compile_output = ''
    execution_output = ''
    error_message = ''
    expected_output = ''
    actual_output = ''

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

    # Capture the output from the compiler
    compile_output = compilation.stdout.decode()

    # Check for compilation errors
    if compilation.returncode != 0:
        error_message = f'Compilation failed:\n{compilation.stderr.decode()}'
    else:
        # Run the code and redirect output to a file
        with open('output.txt', 'w') as outfile:
            test = subprocess.run(['./answer'], stdout=outfile, stderr=subprocess.PIPE)

        # Capture the execution output
        execution_output = read_file('output.txt').strip()

        # Check for runtime errors
        if test.returncode != 0:
            error_message = f'Program execution failed:\n{test.stderr.decode()}'
        else:
            # Validate output
            expected_output = read_file('expected.txt').strip()
            actual_output = read_file('output.txt').strip()

            if actual_output != expected_output:
                error_message = f'Test failed: expected "{expected_output}", but got "{actual_output}"'

    # Code review
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a very polite and fun student in online peer to peer school on online code evaluation. Here is a subject of project: " + subject + " YOU ARE NOT ALLOWED TO PROVIDE ANSWER."},
            {"role": "user", "content": "Hey! Nice to see you on code review! Here is my code: " + answer},
            {"role": "assistant", "content": "Hi! Great to see you too, now let's summarise the subject and look at the code, and compare. This is output of your code " + actual_output + ", this is expected " + expected_output + ", and the error message is " + error_message},
            {"role": "user", "content": "Now could you please give me some feedback on my code? Please act as it is your first message to me and please do not give me actual code."},
        ]
    )

    # Instead of just returning the assistant's message, return a tuple with the additional information
    return (response['choices'][0]['message']['content'], compile_output, execution_output, error_message, actual_output, expected_output)



@app.route('/', methods=['GET', 'POST'])
def index():
    subject = read_file('subject.txt')
    if request.method == 'POST':
        answer = request.form['answer']
        result, compile_output, execution_output, error_message, actual_output, expected_output = run_c_code(subject, answer)
        return render_template('result.html', result=result, compile_output=compile_output, execution_output=execution_output, error_message=error_message, actual_output=actual_output, expected_output=expected_output)
    else:
        return render_template('index.html', subject=subject)

if __name__ == '__main__':
    app.run(debug=True)
