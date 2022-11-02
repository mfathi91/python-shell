import subprocess
import os


def exec_command(command: str):
    try:
        subprocess.run(command.split())
    except Exception:
        print(f'Unable to run "{command}"')


def exec_piped_input(user_input: str):
    # Keep the input and output to restore them later
    s_in = os.dup(0)
    s_out = os.dup(1)

    commands = user_input.split(' | ')

    # Set read_fd to the standard input, so it get the correct input for the first iteration
    read_fd = os.dup(s_in)
    for idx, command in enumerate(commands):
        # Set the input of the command to the previous read file descriptor
        os.dup2(read_fd, 0)
        os.close(read_fd)

        if idx < len(commands) - 1:
            # If it is not the last command, create a pipe and set the write_fd equal to it
            # read_fd will be used for the next iteration
            read_fd, write_fd = os.pipe()
            os.dup2(write_fd, 1)
            os.close(write_fd)
        else:
            # If it is the last command,
            os.dup2(s_out, 1)
            os.close(s_out)

        exec_command(command)

    os.dup2(s_in, 0)
    os.close(s_in)


def exec_cd(command: str):
    path = command.split()[1]
    try:
        os.chdir(path)
    except Exception:
        print(f'Unable to execute "{command}"')


def main():
    while True:
        user_input = input('> ')
        user_input = user_input.strip()
        if ' | ' in user_input:
            exec_piped_input(user_input)
        elif user_input.startswith('cd'):
            exec_cd(user_input)
        elif user_input == 'exit':
            break
        else:
            exec_command(user_input)


if __name__ == '__main__':
    main()
