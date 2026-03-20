import pyfiglet
from termcolor import colored

# Your banner configuration
text = "Jack Was Here"
font = "bigmono9"
fg_color = "magenta"
bg_color = "on_green"

# Generate banner
banner = pyfiglet.figlet_format(text, font=font)

# Apply colors and print
colored_banner = colored(banner, fg_color, bg_color)
print(colored_banner)
