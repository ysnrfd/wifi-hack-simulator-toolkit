# Example custom plugin (save as wifi_plugins/example.py)
from plugin_base import PluginBase

class ExamplePlugin(PluginBase):
    def __init__(self):
        super().__init__()
        self.commands = {
            "hello": self.say_hello,
            "example": self.example_command
        }
    
    def say_hello(self, args):
        return "Hello from the example plugin!"
    
    def example_command(self, args):
        return f"You ran the example command with args: {args}"

def register():
    return ExamplePlugin()