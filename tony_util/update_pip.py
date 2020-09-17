import os


def update_pip():
    """Routine to update all your pip installations"""

    # Concept from:
    # https://stackoverflow.com/questions/2720014/how-to-upgrade-all-python-packages-with-pip/33667992#33667992

    fn_before_update = 'pip_versions_before.txt'
    fn_requirements = 'pip_requirements.txt'
    fn_before_after = 'pip_versions_after.txt'
    os.system(f'pip freeze > {fn_before_update}')
    # This will create a file with the head of
    # altgraph==0.17
    # argon2-cffi==20.1.0
    # ...
    # parse the output file and find all version names
    with open(fn_before_update, "r") as f_in, open(fn_requirements, "w") as f_out:
        for line in f_in:
            line_out = line.replace("==", ">=")
            f_out.write(line_out)
    exit()
    # I actually ran this from the command line to see the output rather than the line below
    # pip install -r requirements_file_name.txt --upgrade
    os.system(f'pip install -r {fn_requirements} --upgrade')


if __name__ == "__main__":
    update_pip()

