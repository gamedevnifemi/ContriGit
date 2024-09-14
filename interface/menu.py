from git_operations.find_git_repos import find_git_repos
from git_operations.commit_statistics import sort_all_repos
from git_operations.contribution_graph import generate_contribution_graph

from blessed import Terminal

term = Terminal()

def get_user_input(prompt):
    print(term.move_xy(0, term.height - 1) + term.clear_eol + prompt, end='', flush=True)
    user_input = []
    while True:
        key = term.inkey()
        if key.name == 'KEY_ENTER':
            break
        elif key.name == 'KEY_BACKSPACE':
            if user_input:
                user_input.pop()
                print(term.move_left() + term.clear_eol, end='', flush=True)
        else:
            user_input.append(key)
            print(key, end='', flush=True)
    return ''.join(user_input)

def display_menu():
    options = [
        "Reveal Git Repositories",
        "Generate Contribution Graph",
        "Process All Repositories",
        "Exit"
    ]
    current_option = 0

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        while True:
            print(term.home + term.clear)
            print(term.bold_bright_blue("Git Contribution Tool\n"))
            for i, option in enumerate(options):
                if i == current_option:
                    print(term.on_blue("> " + option))
                else:
                    print("  " + option)

            key = term.inkey()
            if key.name == "KEY_UP":
                current_option = (current_option - 1) % len(options)
            elif key.name == "KEY_DOWN":
                current_option = (current_option + 1) % len(options)
            elif key.name == "KEY_ENTER":
                if current_option == 0:
                    path = get_user_input("Enter the path to search for Git repositories: ")
                    repos = find_git_repos(path)
                    print(term.clear)
                    print(term.bold("Found Git Repositories:\n"))
                    for repo in repos:
                        print(repo)
                    get_user_input("Press Enter to return to the menu.")
                elif current_option == 1:
                    path = get_user_input("Enter the path to a Git repository: ")
                    repos = find_git_repos(path)
                    if repos:
                        repo = repos
                        commit_data = sort_all_repos(repo)
                        print(term.clear)
                        print(term.bold(f"Contribution graph for repository: {repo}\n"))
                        print(commit_data)
                        generate_contribution_graph(commit_data)
                    else:
                        print(term.red("No repositories found!"))
                    get_user_input("Press Enter to return to the menu.")
                elif current_option == 2:
                    path = get_user_input("Enter the path to search for Git repositories: ")
                    repos = find_git_repos(path)
                    all_commit_data = sort_all_repos(repos)
                    for repo, data in all_commit_data.items():
                        print(term.clear)
                        print(term.bold(f"Contribution graph for repository: {repo}\n"))
                        generate_contribution_graph(data)
                    get_user_input("Press Enter to return to the menu.")
                elif current_option == 3:
                    print(term.home + term.clear)
                    print(term.bold_bright_green("Goodbye!\n"))
                    break