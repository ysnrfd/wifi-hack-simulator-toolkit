"""
WiFi Security Toolkit with Plugin System

Version: 5.0
Copyright (C) 2025 Y.S.N_R.F.D

Features:
- Extensible plugin architecture
- Realistic WiFi security simulations
- Educational content on network security
- Comprehensive ethical hacking guidelines
- Cross-platform support

Disclaimer:
This tool does not perform actual network intrusion. It's for educational purposes only.
Unauthorized network access is illegal.
"""

import os
import sys
import time
import random
import importlib.util
from datetime import datetime
from colorama import Fore, Style, init, Back
import platform

# Initialize colorama
init(autoreset=True)

# Plugin system infrastructure
class PluginManager:
    """Manages plugin loading and execution"""
    
    def __init__(self):
        self.plugins = {}
        self.plugin_dir = "wifi_plugins"
        self.create_plugin_dir()
    
    def create_plugin_dir(self):
        """Create plugin directory if it doesn't exist"""
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            print(f"Created plugin directory: {self.plugin_dir}")
    
    def load_plugins(self):
        """Discover and load plugins from directory"""
        print(f"\n{Fore.YELLOW}Loading plugins...{Style.RESET_ALL}")
        
        # Built-in plugins
        self.load_builtin_plugins()
        
        # External plugins
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                plugin_name = filename[:-3]
                self.load_plugin(plugin_name)
        
        print(f"Loaded {len(self.plugins)} plugins")
    
    def load_builtin_plugins(self):
        """Register built-in plugins"""
        builtins = {
            "scanner": ScannerPlugin(),
            "security_tester": SecurityTesterPlugin(),
            "educational": EducationalPlugin(),
            "settings": SettingsPlugin(),
            "help": HelpPlugin()
        }
        
        for name, plugin in builtins.items():
            self.plugins[name] = plugin
            print(f"  Loaded built-in plugin: {name}")
    
    def load_plugin(self, plugin_name):
        """Load an external plugin"""
        try:
            file_path = os.path.join(self.plugin_dir, f"{plugin_name}.py")
            spec = importlib.util.spec_from_file_location(plugin_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "register"):
                plugin = module.register()
                self.plugins[plugin_name] = plugin
                print(f"  Loaded external plugin: {plugin_name}")
            else:
                print(f"  Plugin {plugin_name} missing register function")
        except Exception as e:
            print(f"  {Fore.RED}Error loading {plugin_name}: {e}{Style.RESET_ALL}")
    
    def get_plugin(self, name):
        """Retrieve a plugin by name"""
        return self.plugins.get(name)
    
    def execute_command(self, command, args):
        """Execute a command through the appropriate plugin"""
        for plugin in self.plugins.values():
            if command in plugin.get_commands():
                return plugin.execute(command, args)
        return f"{Fore.RED}Unknown command: {command}{Style.RESET_ALL}"

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

class ScannerPlugin(PluginBase):
    """Simulates WiFi network scanning"""
    
    def __init__(self):
        super().__init__()
        self.commands = {
            "scan": self.scan_networks,
            "rescan": self.rescan_networks,
            "list": self.list_networks
        }
        self.networks = []
        self.last_scan = None
    
    def generate_networks(self):
        """Generate simulated WiFi networks"""
        common_ssids = ["HomeWiFi", "OfficeNet", "GuestNetwork", "FreeWiFi", 
                       "SecureNet", "TP-Link_123", "NETGEAR", "XfinityWiFi",
                       "Starbucks_WiFi", "Airport_Free_WiFi", "Library_Public", "Test", "ENV"]
        
        self.networks = []
        for i in range(random.randint(8, 15)):
            network = {
                "id": i + 1,
                "ssid": random.choice(common_ssids) + (f"_{random.randint(1, 100)}" if random.random() > 0.5 else ""),
                "bssid": ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)]),
                "power": random.randint(30, 90),
                "encryption": random.choice(["WPA2", "WPA3", "WPA2/WPA3", "WEP", "OPEN"]),
                "channel": random.randint(1, 11),
                "clients": random.randint(0, 15)
            }
            self.networks.append(network)
    
    def scan_networks(self, args):
        """Simulate network scanning process"""
        print(f"\n{Fore.BLUE}Scanning for WiFi networks...{Style.RESET_ALL}")
        self.simulate_progress(3)
        self.generate_networks()
        self.last_scan = datetime.now()
        return self.list_networks(args)
    
    def rescan_networks(self, args):
        """Rescan networks"""
        return self.scan_networks(args)
    
    def list_networks(self, args):
        """Display available networks"""
        if not self.networks:
            return f"{Fore.YELLOW}No networks found. Run 'scan' first.{Style.RESET_ALL}"
        
        output = [f"\n{Fore.CYAN}Available WiFi Networks (Scanned at {self.last_scan.strftime('%H:%M:%S')}):{Style.RESET_ALL}"]
        output.append(f"{Fore.YELLOW}{'ID':<4} {'SSID':<20} {'BSSID':<18} {'POWER':<6} {'ENCRYPTION':<12} {'CH':<3} {'CLIENTS'}{Style.RESET_ALL}")
        
        for network in self.networks:
            # Color coding based on security
            if network["encryption"] == "OPEN":
                sec_color = Fore.RED
            elif network["encryption"] in ["WEP", "WPA"]:
                sec_color = Fore.YELLOW
            else:
                sec_color = Fore.GREEN
                
            output.append(
                f"{network['id']:<4} {network['ssid'][:20]:<20} {network['bssid']}  {network['power']:>3}%  "
                f"{sec_color}{network['encryption']:<12}{Style.RESET_ALL}  {network['channel']:>2}  "
                f"{network['clients']:>3}"
            )
        
        return "\n".join(output)
    
    def simulate_progress(self, seconds):
        """Show progress animation"""
        for i in range(seconds * 2):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print()

class SecurityTesterPlugin(PluginBase):
    """Simulates WiFi security testing"""
    
    def __init__(self):
        super().__init__()
        self.commands = {
            "test": self.test_network,
            "audit": self.audit_network
        }
        self.scanner = None
    
    def set_scanner(self, scanner):
        """Set reference to scanner plugin"""
        self.scanner = scanner
    
    def test_network(self, args):
        """Test a specific network"""
        if not args:
            return f"{Fore.RED}Please specify network ID{Style.RESET_ALL}"
        
        try:
            network_id = int(args[0])
            if not self.scanner or not self.scanner.networks:
                return f"{Fore.YELLOW}No networks available. Run 'scan' first.{Style.RESET_ALL}"
            
            network = next((n for n in self.scanner.networks if n["id"] == network_id), None)
            if not network:
                return f"{Fore.RED}Network ID {network_id} not found{Style.RESET_ALL}"
            
            return self.simulate_test(network)
        except ValueError:
            return f"{Fore.RED}Invalid network ID{Style.RESET_ALL}"
    
    def audit_network(self, args):
        """Run comprehensive security audit"""
        return self.test_network(args) + "\n\n" + self.run_security_audit()
    
    def simulate_test(self, network):
        """Simulate security testing on a network"""
        output = [
            f"\n{Fore.BLUE}Starting security assessment of {network['ssid']} ({network['bssid']}){Style.RESET_ALL}",
            f"  Signal: {network['power']}%",
            f"  Encryption: {self.get_encryption_color(network['encryption'])}{network['encryption']}{Style.RESET_ALL}",
            f"  Channel: {network['channel']}",
            f"  Connected clients: {network['clients']}"
        ]
        
        self.simulate_progress(3)
        
        # Security analysis
        if network["encryption"] == "OPEN":
            output.append(f"\n{Fore.RED}CRITICAL: Network uses no encryption!{Style.RESET_ALL}")
            output.append("  All traffic is exposed and can be easily intercepted.")
        elif network["encryption"] == "WEP":
            output.append(f"\n{Fore.RED}HIGH RISK: WEP encryption is obsolete and vulnerable!{Style.RESET_ALL}")
            output.append("  This network can be compromised in minutes using available tools.")
        elif network["encryption"] == "WPA2":
            output.append(f"\n{Fore.YELLOW}MEDIUM RISK: WPA2 is generally secure{Style.RESET_ALL}")
            output.append("  but vulnerable to KRACK attacks if not properly configured.")
        elif network["encryption"] == "WPA3":
            output.append(f"\n{Fore.GREEN}LOW RISK: WPA3 provides strong security{Style.RESET_ALL}")
            output.append("  when properly implemented with strong passwords.")
        
        output.append(f"\n{Fore.BLUE}Simulating security tests...{Style.RESET_ALL}")
        self.simulate_progress(5)
        
        output.append(f"\n{Fore.GREEN}Simulation complete.{Style.RESET_ALL}")
        output.append("This tool does not perform actual penetration testing.")
        output.append("For real security assessments, use professional tools with proper authorization.")
        
        return "\n".join(output)
    
    def run_security_audit(self):
        """Run comprehensive security audit simulation"""
        output = [
            f"\n{Fore.CYAN}Running Comprehensive Security Audit{Style.RESET_ALL}",
            "Checking for common vulnerabilities:",
            "  - Weak encryption protocols",
            "  - Default credentials",
            "  - Rogue access points",
            "  - Misconfigured security settings",
            "  - Outdated firmware"
        ]
        
        self.simulate_progress(8)
        
        output.append(f"\n{Fore.GREEN}Audit completed. 3 potential vulnerabilities found.{Style.RESET_ALL}")
        output.append("Recommendations:")
        output.append("  1. Upgrade to WPA3 encryption")
        output.append("  2. Change default admin credentials")
        output.append("  3. Update router firmware to latest version")
        
        return "\n".join(output)
    
    def get_encryption_color(self, encryption):
        """Get color for encryption type"""
        if encryption == "OPEN":
            return Fore.RED
        elif encryption in ["WEP", "WPA"]:
            return Fore.YELLOW
        return Fore.GREEN
    
    def simulate_progress(self, seconds):
        """Show progress animation"""
        for i in range(seconds * 2):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print()

class EducationalPlugin(PluginBase):
    """Provides educational content on WiFi security"""
    
    def __init__(self):
        super().__init__()
        self.commands = {
            "learn": self.show_content,
            "guidelines": self.show_guidelines,
            "tutorial": self.show_tutorial
        }
        self.content = {
            "wpa": self.wpa_info,
            "wep": self.wep_info,
            "wps": self.wps_info,
            "encryption": self.encryption_info
        }
    
    def show_content(self, args):
        """Show educational content"""
        if not args:
            return self.list_topics()
        
        topic = args[0].lower()
        if topic in self.content:
            return self.content[topic]()
        return f"{Fore.RED}Unknown topic: {topic}{Style.RESET_ALL}"
    
    def wep_info(self):
        return f"""
    {Fore.CYAN}Understanding WEP Security{Style.RESET_ALL}

    {Fore.YELLOW}What is WEP?{Style.RESET_ALL}
    Wired Equivalent Privacy (WEP) was the first security protocol for WiFi networks.
    It is now considered obsolete due to serious security flaws.

    {Fore.RED}Security Warning:{Style.RESET_ALL}
    - WEP can be cracked in minutes with basic tools
    - Should never be used in any modern network
    - Always prefer WPA2 or WPA3

    {Fore.GREEN}Recommendation:{Style.RESET_ALL}
    Upgrade to WPA2 or WPA3 immediately if your network still uses WEP.
    """

    def wps_info(self):
        return f"""
    {Fore.CYAN}Understanding WPS (Wi-Fi Protected Setup){Style.RESET_ALL}

    {Fore.YELLOW}What is WPS?{Style.RESET_ALL}
    WPS (Wi-Fi Protected Setup) is a network security standard designed to make it easier 
    for users to connect devices to a secure wireless network without entering the password manually.

    {Fore.YELLOW}WPS Connection Methods:{Style.RESET_ALL}
    1. Push Button (physical button on router)
    2. PIN entry (8-digit code on router or device)
    3. NFC or USB (rare and legacy options)

    {Fore.RED}Security Risks:{Style.RESET_ALL}
    - **Vulnerable PIN method**: The 8-digit WPS PIN is highly susceptible to brute-force attacks.
    - **Reaver attack**: Tools like Reaver can break WPS PINs in a few hours.
    - **Limited protection**: Many routers do not properly throttle repeated failed attempts.

    {Fore.GREEN}Security Recommendations:{Style.RESET_ALL}
    - Disable WPS in your router settings if you don’t need it.
    - Use strong WPA2/WPA3 passphrases instead of WPS.
    - Avoid using the WPS PIN method — it is the most vulnerable.

    {Fore.MAGENTA}Reminder:{Style.RESET_ALL}
    Convenience should never come at the cost of security.
    """
    
    def list_topics(self):
        """List available educational topics"""
        output = [f"\n{Fore.CYAN}Available Educational Topics:{Style.RESET_ALL}"]
        for topic in self.content.keys():
            output.append(f"  - {topic}")
        output.append("\nUse 'learn [topic]' to explore a topic")
        return "\n".join(output)
    
    def show_guidelines(self, args):
        """Display ethical hacking guidelines"""
        guidelines = [
            f"\n{Fore.CYAN}Ethical Hacking Guidelines:{Style.RESET_ALL}",
            "1. Always obtain explicit written permission before testing any network",
            "2. Clearly define the scope of testing with the network owner",
            "3. Respect privacy and confidentiality of network users",
            "4. Do not attempt to access or modify data without authorization",
            "5. Report all discovered vulnerabilities to the network owner",
            "6. Securely delete any collected data after testing",
            "7. Use your skills to improve security, not exploit vulnerabilities",
            "8. Stay updated on relevant laws and regulations",
            "9. Maintain professional integrity at all times",
            "10. Educate others about responsible security practices"
        ]
        return "\n".join(guidelines)
    
    def show_tutorial(self, args):
        """Show basic security tutorial"""
        return f"""
{Fore.CYAN}Basic WiFi Security Tutorial{Style.RESET_ALL}

{Fore.YELLOW}1. Understanding Encryption Protocols{Style.RESET_ALL}
  - WEP: Obsolete and easily compromised (Avoid)
  - WPA: Better than WEP but still vulnerable
  - WPA2: Current standard (AES encryption)
  - WPA3: Newest standard with enhanced security

{Fore.YELLOW}2. Strong Password Practices{Style.RESET_ALL}
  - Use at least 12 characters
  - Combine uppercase, lowercase, numbers, and symbols
  - Avoid dictionary words and personal information
  - Change passwords periodically

{Fore.YELLOW}3. Router Security Settings{Style.RESET_ALL}
  - Change default admin credentials
  - Disable WPS (WiFi Protected Setup)
  - Enable network firewall
  - Disable remote administration
  - Keep firmware updated

{Fore.YELLOW}4. Network Monitoring{Style.RESET_ALL}
  - Regularly check connected devices
  - Set up alerts for unauthorized access
  - Use network segmentation for sensitive devices

{Fore.GREEN}Remember: Security is an ongoing process, not a one-time setup{Style.RESET_ALL}
"""
    
    def wpa_info(self):
        """Information about WPA security"""
        return f"""
{Fore.CYAN}Understanding WPA Security{Style.RESET_ALL}

{Fore.YELLOW}What is WPA?{Style.RESET_ALL}
Wi-Fi Protected Access (WPA) is a security protocol designed to secure 
wireless computer networks. It was created to replace the insecure WEP protocol.

{Fore.YELLOW}Versions:{Style.RESET_ALL}
1. WPA (2003): 
   - Uses TKIP encryption
   - Vulnerable to various attacks
   
2. WPA2 (2004):
   - Uses AES encryption (CCMP)
   - Current industry standard
   - Vulnerable to KRACK attack (2017)
   
3. WPA3 (2018):
   - Enhanced security with SAE (Simultaneous Authentication of Equals)
   - Protects against offline dictionary attacks
   - Mandatory encryption for open networks

{Fore.YELLOW}Best Practices:{Style.RESET_ALL}
- Always use WPA2 or WPA3
- Choose a strong, unique passphrase
- Disable WPS (Wi-Fi Protected Setup)
- Regularly update router firmware
"""

    def encryption_info(self):
        """General encryption information"""
        return f"""
{Fore.CYAN}Wireless Encryption Explained{Style.RESET_ALL}

{Fore.YELLOW}Types of Wireless Encryption:{Style.RESET_ALL}

{Fore.RED}1. OPEN (No Encryption){Style.RESET_ALL}
   - No security whatsoever
   - All data transmitted in clear text
   - Should never be used for sensitive data

{Fore.YELLOW}2. WEP (Wired Equivalent Privacy){Style.RESET_ALL}
   - Introduced in 1997
   - Easily compromised in minutes
   - Completely insecure - avoid at all costs

{Fore.GREEN}3. WPA/WPA2/WPA3 (Wi-Fi Protected Access){Style.RESET_ALL}
   - Successively more secure protocols
   - WPA2 is current standard
   - WPA3 is the future with enhanced security

{Fore.YELLOW}Key Security Features:{Style.RESET_ALL}
- Encryption: Scrambles data to prevent eavesdropping
- Authentication: Verifies device identity
- Integrity Checking: Ensures data hasn't been modified

{Fore.CYAN}Always use the strongest encryption available on your devices{Style.RESET_ALL}
"""

class SettingsPlugin(PluginBase):
    """Manages application settings"""
    
    def __init__(self):
        super().__init__()
        self.commands = {
            "settings": self.show_settings,
            "set": self.change_setting,
            "plugins": self.list_plugins
        }
        self.settings = {
            "color_scheme": "default",
            "scan_interval": "5",
            "verbosity": "normal"
        }
    
    def show_settings(self, args):
        """Display current settings"""
        output = [f"\n{Fore.CYAN}Current Settings:{Style.RESET_ALL}"]
        for key, value in self.settings.items():
            output.append(f"  {key}: {value}")
        return "\n".join(output)
    
    def change_setting(self, args):
        """Change a setting"""
        if len(args) < 2:
            return f"{Fore.RED}Usage: set [setting] [value]{Style.RESET_ALL}"
        
        setting = args[0]
        value = args[1]
        
        if setting in self.settings:
            self.settings[setting] = value
            return f"{Fore.GREEN}Setting updated: {setting} = {value}{Style.RESET_ALL}"
        return f"{Fore.RED}Unknown setting: {setting}{Style.RESET_ALL}"
    
    def list_plugins(self, args):
        """List loaded plugins"""
        # This will be implemented in the main app

class HelpPlugin(PluginBase):
    """Provides help information"""
    
    def __init__(self):
        super().__init__()
        self.commands = {
            "help": self.show_help,
            "commands": self.list_commands,
            "all_cmds": self.show_all_commands  # Added command
        }
        self.all_commands = {}  # Will store all commands from all plugins

    def set_all_commands(self, commands):
        """Set the complete command list"""
        self.all_commands = commands
    
    def show_all_commands(self, args):
        """Display all available commands from all plugins"""
        if not self.all_commands:
            return f"{Fore.YELLOW}Command list not initialized.{Style.RESET_ALL}"
        
        output = [f"\n{Fore.CYAN}All Available Commands:{Style.RESET_ALL}"]
        for plugin_name, commands in self.all_commands.items():
            output.append(f"\n{Fore.YELLOW}{plugin_name} Plugin:{Style.RESET_ALL}")
            for cmd in sorted(commands):
                output.append(f"  - {cmd}")
        
        return "\n".join(output)
    
    def show_help(self, args):
        """Show general help"""
        return f"""
{Fore.CYAN}WiFi Security Toolkit Help{Style.RESET_ALL}

{Fore.YELLOW}Core Commands:{Style.RESET_ALL}
  scan       - Scan for available WiFi networks
  rescan     - Rescan networks
  list       - List discovered networks
  test [id]  - Test security of a specific network
  audit [id] - Run comprehensive security audit
  learn      - Show educational content
  guidelines - Display ethical hacking guidelines
  tutorial   - Basic security tutorial
  settings   - Show current settings
  plugins    - List loaded plugins
  exit       - Exit the application
  all_cmds   - Show all available commands from Core and Plugins

{Fore.YELLOW}Plugin System:{Style.RESET_ALL}
- Place custom plugins in 'wifi_plugins' directory
- Plugins must implement a register() function
- They will be automatically loaded at startup

{Fore.GREEN}Type 'commands' for full command list{Style.RESET_ALL}
"""
    
    def list_commands(self, args):
        """List all available commands"""
        # This will be implemented in the main app

class WiFiSecurityToolkit:
    """Main application class"""
    
    def __init__(self):
        self.plugin_manager = PluginManager()
        self.running = True
        self.color_scheme = "default"
        
    def show_banner(self):
        """Display application banner"""
        banner = f"""
{Fore.GREEN}
██╗    ██╗██╗███████╗██╗    ███████╗ ██████╗███████╗███╗   ██╗███████╗████████╗
██║    ██║██║██╔════╝██║    ██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝╚══██╔══╝
██║ █╗ ██║██║█████╗  ██║    █████╗  ██║     █████╗  ██╔██╗ ██║█████╗     ██║   
██║███╗██║██║██╔══╝  ██║    ██╔══╝  ██║     ██╔══╝  ██║╚██╗██║██╔══╝     ██║   
╚███╔███╔╝██║██║     ██║    ██║     ╚██████╗███████╗██║ ╚████║███████╗   ██║   
 ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝    ╚═╝      ╚═════╝╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝     YSN_RFD
                                                                                
{Style.RESET_ALL}"""
        print(banner)
        print(f"{Fore.YELLOW}WiFi Security Simulation Toolkit v5.0{Style.RESET_ALL}")
        print(f"{Fore.RED}Developed By YSNRFD{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Educational Use Only - Not for Actual Security Testing{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Platform: {platform.system()} {platform.release()} | Python {sys.version.split()[0]}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Type 'help' for assistance, 'commands' for available commands{Style.RESET_ALL}\n")
    
    def initialize_plugins(self):
        """Initialize and cross-link plugins"""
        self.plugin_manager.load_plugins()
        
        # Cross-link plugins if needed
        scanner = self.plugin_manager.get_plugin("scanner")
        security_tester = self.plugin_manager.get_plugin("security_tester")
        if scanner and security_tester:
            security_tester.set_scanner(scanner)
        
        # Pass all commands to HelpPlugin
        help_plugin = self.plugin_manager.get_plugin("help")
        if help_plugin:
            help_plugin.set_all_commands(self.get_all_commands_grouped())
    
    def get_all_commands(self):
        """Get all available commands from plugins"""
        commands = {}
        for name, plugin in self.plugin_manager.plugins.items():
            for cmd in plugin.get_commands():
                commands[cmd] = name
        return commands
    
    def get_all_commands_grouped(self):
        """Get all commands grouped by plugin"""
        commands_dict = {}
        for plugin_name, plugin in self.plugin_manager.plugins.items():
            commands_dict[plugin_name] = plugin.get_commands()
        return commands_dict
    
    def run(self):
        """Main application loop"""
        self.show_banner()
        self.initialize_plugins()
        
        all_commands = self.get_all_commands()
        
        while self.running:
            try:
                user_input = input(f"\n{Fore.GREEN}wifi-toolkit>{Style.RESET_ALL} ").strip()
                if not user_input:
                    continue
                
                parts = user_input.split()
                command = parts[0].lower()
                args = parts[1:]
                
                if command == "exit":
                    print("Exiting WiFi Security Toolkit...")
                    self.running = False
                    continue
                elif command == "commands":
                    print(f"\n{Fore.CYAN}Available Commands:{Style.RESET_ALL}")
                    for cmd, plugin in sorted(all_commands.items()):
                        print(f"  {cmd:12} ({plugin} plugin)")
                    continue
                elif command == "plugins":
                    print(f"\n{Fore.CYAN}Loaded Plugins:{Style.RESET_ALL}")
                    for name in self.plugin_manager.plugins.keys():
                        print(f"  - {name}")
                    continue
                
                result = self.plugin_manager.execute_command(command, args)
                print(result)
                
            except KeyboardInterrupt:
                print("\nExiting WiFi Security Toolkit...")
                self.running = False
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    # Check for supported platforms
    supported_platforms = ["linux", "darwin", "win32"]
    if sys.platform not in supported_platforms:
        print(f"{Fore.RED}Unsupported platform: {sys.platform}{Style.RESET_ALL}")
        print("Supported platforms: Linux, macOS, Windows")
        sys.exit(1)
    
    app = WiFiSecurityToolkit()
    app.run()