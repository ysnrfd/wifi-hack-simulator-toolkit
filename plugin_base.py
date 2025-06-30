"""Base plugin class for WiFi Security Toolkit"""

class PluginBase:
    """Base class for all plugins"""
    
    def __init__(self):
        self.commands = {}
    
    def get_commands(self):
        """Return list of commands this plugin handles"""
        return list(self.commands.keys())
    
    def execute(self, command, args):
        """Execute a command"""
        if command in self.commands:
            return self.commands[command](args)
        return f"Command not implemented: {command}"