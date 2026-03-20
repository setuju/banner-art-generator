import pyfiglet
from termcolor import colored

# Your banner configuration
text = "Jack Was Here"
font = "lean"
fg_color = "green"
bg_color = "on_blue"

# Generate banner
banner = pyfiglet.figlet_format(text, font=font)

# Apply colors and print
colored_banner = colored(banner, fg_color, bg_color)
print(colored_banner)
