import sys, os

from tool_wrapper import ToolWrapper

class XploitFramework:
    def __init__(self):
        self.exploits = {}
        self.sessions = []

    def register_exploit(self, name: str, exploit_class):
        self.exploits[name] = exploit_class
        print(f' [+] Loaded {name} ')

    def list_exploit(self):
        print('Available Exploits:')
        for name in sorted(self.exploits.keys()):
            print(f' {name} ')

    def run_exploit(self, name:str, target: str, **kwargs):
        if name not in self.exploits:
            print(f' [!] Exploit {name} is not Found ')
            return None
        exploit = self.exploits[name](target, **kwargs)
        return exploit.execute()

if __name__ == "__main__":
    xploit = XploitFramework()
    xploit.list_exploit()
