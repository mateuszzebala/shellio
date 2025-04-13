from main import ShellIO

shell = ShellIO('bash', [])

shell.set_cwd('/home/mateuszzebala/windows/Desktop/shellio')

shell.run()

shell.put('nano codes.py').enter()

while True:
    for t, o in shell.get_output(timeout=1):
        if t is None:
            print(o, end='')