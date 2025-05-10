from typing import Literal
import pty
import os
import subprocess
from threading import Thread
from collections import defaultdict
import time
from queue import Queue, Empty
import re
import atexit

Shells = Literal["sh", "bash", "zsh"]

class ShellIO:
    
    shells: list['ShellIO'] = []
    
    def __init__(self, shell_type: Shells, args: list[str]) -> None:
        self.shell_type: Shells = shell_type
        self.args: list[str] = args
        self.program = [self.shell_type, *self.args]
        self.line_queue = Queue()
        self.events = defaultdict(list)
        self.cwd = None
        self.shells.append(self)
    
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
            args = []
            env["PS1"] = "$ "
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
            shell=False,
            bufsize=0,
            cwd=self.cwd,
            env=env,
            preexec_fn=os.setsid
        )
        self.thread = Thread(target=self.enqueue_output, args=(self.line_queue,))
        self.thread.daemon = True
        self.thread.start()
        
    def put(self, stdin: str) -> None:
        os.write(self.master, stdin.encode())
        
    def get(self, timeout: float = 0.1):
        output = b""
        while True:
            try:
                output += self.line_queue.get(timeout=timeout)
            except Empty:
                break
        return output.decode(errors="replace")
    
    def get_output(self, timeout: float = 0.1) -> list[bytes]:
        output = b""
        while True:
            try:
                output += self.line_queue.get(timeout=timeout)
            except Empty:
                break
  
        return ShellIO.split_bytes_ansi(output)
    
    @staticmethod
    def split_bytes_ansi(data: bytes) -> list[bytes]:
        ansi_pattern = re.compile(rb'\x1b\[[0-9;?]*[a-zA-Z]')
        
        result = []
        i = 0
        while i < len(data):
            match = ansi_pattern.match(data, i)
            if match:
                result.append(match.group())
                i = match.end()
            else:
                result.append(data[i:i+1])
                i += 1
        
        return result
    
    @staticmethod
    def kill_all_shells():
        for shell in ShellIO.shells:
            if shell.process.poll() is None:
                shell.process.terminate()
    
atexit.register(ShellIO.kill_all_shells)


        
