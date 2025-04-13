from typing import Literal, Any
import pty
import os
import subprocess
from threading import Thread
import time
from queue import Queue, Empty
from codes import TERMINAL_CODES, SPECIAL_KEYS

Shells = Literal["sh", "bash", "zsh"]

class ShellIO:
    def __init__(self, shell_type: Shells, args: list[str]) -> None:
        self.shell_type: Shells = shell_type
        self.args: list[str] = args
        self.program = [self.shell_type, *self.args]
        self.line_queue = Queue()
        self.commands: Commands = Commands(self)
        self.cwd = None
    
    def set_cwd(self, path: str) -> None:
        self.cwd = path
    
    def enqueue_output(self, queue: Queue) -> None:
        while True:
            out = os.read(self.master, 128)
            if not out: time.sleep(0.1) 
            else: queue.put(out)
    
    def run(self) -> None:
        
        args = []
        
        env = os.environ.copy()
            
        if self.shell_type == 'bash':
            args = ['--rcfile', '~/.bashrc', '--login']
        elif self.shell_type == 'sh':
            args = ['-i', '--login', '--init-file', '~/.bashrc', ]
            env["PS1"] = "sh$ "
        elif self.shell_type == 'zsh':
            args = ['--interactive']
        else:
            raise Exception('Shell should be sh, bash or zsh')
        
        self.program = [self.shell_type, *args, *self.args]
        self.master, self.slave = pty.openpty()
        self.process = subprocess.Popen(
            self.program,
            stdin=self.slave,
            stdout=self.slave,
            stderr=self.slave,
            text=False,
            shell=True,
            bufsize=0,
            cwd=self.cwd,
            env=env,
            preexec_fn=os.setsid
        )
        self.thread = Thread(target=self.enqueue_output, args=(self.line_queue,))
        self.thread.daemon = True
        self.thread.start()
        
    def put(self, stdin: str) -> 'Commands':
        os.write(self.master, stdin.encode())
        return self.commands
    
    def get(self, timeout: float = 0.1):
        output = b""
        while True:
            try:
                output += self.line_queue.get(timeout=timeout)
            except Empty:
                break
        return output.decode(errors="replace")
    
    def get_output(self, timeout: float = 0.1) -> list[tuple[str | None, str]]:
        output = b""
        while True:
            try:
                output += self.line_queue.get(timeout=timeout)
            except Empty:
                break
        return ShellIO.recognize(output)
    
    @staticmethod
    def recognize(output: bytes):
        result = []
        text = output.decode(errors='ignore')
        i = 0
        sorted_codes = sorted(TERMINAL_CODES.items(), key=lambda kv: -len(kv[1])) 

        while i < len(text):
            matched = False
            for name, seq in sorted_codes:
                if text.startswith(seq, i):
                    result.append((name, seq))
                    i += len(seq)
                    matched = True
                    break
            if not matched:
                result.append((None, text[i]))
                i += 1
        return result


class Commands:
    def __init__(self, shell: ShellIO):
        self.shell = shell
    
    def window_size(self, width: int, height: int):
        ...
    
    def enter(self):
        self.shell.put(SPECIAL_KEYS['ENTER'])
        
        
