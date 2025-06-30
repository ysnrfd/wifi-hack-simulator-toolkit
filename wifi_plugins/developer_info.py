"""Developer Information Plugin for WiFi Security Toolkit"""

from colorama import Fore, Style
from plugin_base import PluginBase

class DeveloperInfoPlugin(PluginBase):
    """Displays developer information"""
    
    def __init__(self):
        super().__init__()
        self.commands = {
            "dev": self.show_developer_info,
            "developer": self.show_developer_info,
            "info": self.show_developer_info
        }
    
    def show_developer_info(self, args):
        """Display developer information"""
        return f"""
{Fore.CYAN}# ----------------------------------------------
# Developer Information
# ----------------------------------------------
# Developed by: Yasin (YSNRFD)
# Telegram: @ysnrfd
# GitHub: https://github.com/ysnrfd
# Project: [WIFI HACK SIMULATOR TOOLKIT]
# Version: 5.0.0
# Description: This tool was developed with passion and precision
#              to serve as a powerful and flexible solution.
#              Feel free to contribute, report issues, or suggest features.
#              THANKS FOR SUPPORT ME.
#
# License: Open-Source
# ----------------------------------------------{Style.RESET_ALL}
"""

def register():
    """Register the plugin"""
    return DeveloperInfoPlugin()