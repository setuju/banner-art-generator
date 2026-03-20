#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Banner Maker with pyfiglet and termcolor
----------------------------------------
A fun interactive tool to generate colorful ASCII art banners
with custom fonts and colors, plus exportable Python code.

Author: Jack
GitHub: https://github.com/setuju
License: MIT

Features:
- Random welcome banner "Jack" with random font and colors (each run)
- Shows which font and colors were used for the random banner
- Prevents foreground and background from being the same color
- User‑defined text (you can create your own banner)
- Display 19 top fonts in a grid layout, plus option to show all fonts
- "Surprise me!" option: randomly picks font and colors for your text
- Choose font manually from top 19, all fonts, or any installed font
- Optional text color (foreground) and background color with grid display
- Option to skip colors (plain banner)
- Live preview of the banner
- Generate ready‑to‑run Python code for your exact banner
- Save the generated banner to a text file
"""

import sys
import random
import pyfiglet
from termcolor import colored

# ----------------------------------------------------------------------
#  CONSTANTS & CONFIGURATION
# ----------------------------------------------------------------------

# Color lists supported by termcolor
FG_COLORS = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
BG_COLORS = ['on_grey', 'on_red', 'on_green', 'on_yellow', 'on_blue',
             'on_magenta', 'on_cyan', 'on_white']

# Number of top fonts to show in grid (use 19, so 20th option is "Show all fonts")
TOP_FONTS_COUNT = 19

# ----------------------------------------------------------------------
#  HELPER FUNCTIONS
# ----------------------------------------------------------------------

def get_top_fonts(n=TOP_FONTS_COUNT):
    """
    Return the first `n` font names from pyfiglet's font list.
    """
    all_fonts = pyfiglet.FigletFont.getFonts()
    return all_fonts[:n]


def display_grid(items, title, columns=4, numbered=True):
    """
    Print a list of items in a grid with `columns` columns.
    If `numbered` is True, each item is prefixed with a number.
    Returns the maximum number of items that can be displayed.
    """
    # Determine maximum item length for formatting
    max_len = max(len(item) for item in items) + 3  # +3 for spacing
    print("\n" + title)
    for i, item in enumerate(items, start=1):
        if numbered:
            print("{:<3} {:<{}}".format(str(i) + '.', item, max_len), end='')
        else:
            print("{:<{}}".format(item, max_len), end='')
        if i % columns == 0 or i == len(items):
            print()
    print()
    return len(items)


def display_all_fonts():
    """
    Show all available fonts in a grid (5 columns) and return to menu.
    """
    all_fonts = pyfiglet.FigletFont.getFonts()
    # Use 5 columns for all fonts, without numbers
    display_grid(all_fonts, "=== ALL AVAILABLE FONTS ===", columns=5, numbered=False)
    input("Press Enter to continue...")


def choose_font():
    """
    Interactively choose a font.
    Options:
        - 0: Surprise me! (random font & colors)
        - 1..TOP_FONTS_COUNT: pick from the grid
        - 20: Show all fonts
        - custom: enter font name manually
    Returns a tuple (font, fg_color, bg_color) where fg_color and bg_color
    are None if not chosen (meaning user will pick later) or actual colors
    if "Surprise me!" was selected.
    """
    while True:
        top_fonts = get_top_fonts()
        # Display top fonts in grid (numbered 1..TOP_FONTS_COUNT)
        display_grid(top_fonts, "=== Top {} Fonts (select by number) ===".format(TOP_FONTS_COUNT),
                     columns=4, numbered=True)

        print("Options:")
        print("  0. Surprise me! (random font & colors)")
        print("  [1-{}] Pick a font from the list above".format(TOP_FONTS_COUNT))
        print("  20. Show all fonts")
        print("  [custom] Enter a custom font name")

        choice = input("Your choice: ").strip()

        # Surprise me!
        if choice == '0':
            # Random font from all available
            all_fonts = pyfiglet.FigletFont.getFonts()
            font = random.choice(all_fonts)

            # Random colors ensuring they are different
            bg_base = [c.replace('on_', '') for c in BG_COLORS]
            fg = random.choice(FG_COLORS)
            # Filter background colors whose base != fg
            possible_bg_indices = [i for i, base in enumerate(bg_base) if base != fg]
            if possible_bg_indices:
                bg = BG_COLORS[random.choice(possible_bg_indices)]
            else:
                bg = random.choice(BG_COLORS)

            print("\n🎲 Surprise! Selected for you:")
            print(f"   Font: {font}")
            print(f"   Text color: {fg}")
            print(f"   Background: {bg}")
            return font, fg, bg

        # Show all fonts
        if choice == '20':
            display_all_fonts()
            continue  # back to font selection menu

        # Pick from numbered list
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= TOP_FONTS_COUNT:
                return top_fonts[num - 1], None, None

        # Custom font
        font_name = choice.strip()
        all_fonts = pyfiglet.FigletFont.getFonts()
        if font_name not in all_fonts:
            print("Font '{}' not found. Using default 'standard'.".format(font_name))
            font_name = "standard"
        return font_name, None, None


def choose_color(prompt, color_list, allow_none=True, forbid_equal=None):
    """
    Interactively choose a color from a list, displayed in a grid.
    If allow_none is True, option 0 means "no color" (returns None).
    If forbid_equal is provided (a color string), it will warn and ask again
    if user picks the same color (for background/foreground conflict).
    Returns a color string or None.
    """
    # Display colors in a grid (4 columns)
    display_grid(color_list, prompt, columns=4, numbered=True)

    if allow_none:
        print("0. No color")

    while True:
        try:
            num = int(input("Enter number (0-{}): ".format(len(color_list))))
            if num == 0 and allow_none:
                return None
            if 1 <= num <= len(color_list):
                chosen = color_list[num - 1]
                # Check if color conflicts with forbidden one (if any)
                if forbid_equal is not None:
                    # For background, we compare base color (strip 'on_')
                    if chosen.startswith('on_'):
                        base_chosen = chosen.replace('on_', '')
                    else:
                        base_chosen = chosen
                    if base_chosen == forbid_equal:
                        print("⚠️  This color is the same as the foreground! Please choose a different one.\n")
                        # Redisplay colors for clarity
                        display_grid(color_list, prompt, columns=4, numbered=True)
                        if allow_none:
                            print("0. No color")
                        continue
                return chosen
            print("Number must be between 0 and {}.".format(len(color_list)))
        except ValueError:
            print("Invalid input. Please enter a number.")


def generate_code(text, font, fg_color, bg_color):
    """
    Generate a self‑contained Python script that reproduces the banner.
    If fg_color or bg_color is None, they are omitted from the colored() call.
    """
    code_lines = [
        "import pyfiglet",
        "from termcolor import colored",
        "",
        '# Your banner configuration',
        'text = "{}"'.format(text),
        'font = "{}"'.format(font),
    ]

    # Add color lines only if they are used
    if fg_color is not None:
        code_lines.append('fg_color = "{}"'.format(fg_color))
    if bg_color is not None:
        code_lines.append('bg_color = "{}"'.format(bg_color))

    code_lines.extend([
        "",
        "# Generate banner",
        'banner = pyfiglet.figlet_format(text, font=font)',
        "",
    ])

    # Build the colored() call dynamically
    if fg_color is None and bg_color is None:
        code_lines.append("# Print plain banner")
        code_lines.append("print(banner)")
    else:
        colored_args = ["banner"]
        if fg_color is not None:
            colored_args.append('fg_color')
        if bg_color is not None:
            colored_args.append('bg_color')
        code_lines.extend([
            "# Apply colors and print",
            'colored_banner = colored({})'.format(", ".join(colored_args)),
            "print(colored_banner)"
        ])

    return "\n".join(code_lines)


def display_banner(text, font, fg_color, bg_color):
    """
    Generate and print the banner with optional colors.
    Returns the banner string (plain) for later use.
    """
    try:
        banner = pyfiglet.figlet_format(text, font=font)
    except Exception as e:
        print("Error generating banner: {}".format(e))
        sys.exit(1)

    if fg_color is None and bg_color is None:
        print(banner)
    else:
        colored_banner = colored(banner, fg_color, bg_color)
        print(colored_banner)

    return banner  # return plain banner (no ANSI codes)


def random_banner(text="Jack"):
    """
    Generate and display a random banner with the given text.
    Random font, random foreground, random background.
    Ensures foreground and background are different colors.
    Returns (font, fg_color, bg_color) for reference.
    """
    # Get all available fonts
    all_fonts = pyfiglet.FigletFont.getFonts()
    # Choose a random font
    font = random.choice(all_fonts)

    # Choose random colors, ensuring they are different
    bg_base = [c.replace('on_', '') for c in BG_COLORS]
    fg = random.choice(FG_COLORS)
    possible_bg_indices = [i for i, base in enumerate(bg_base) if base != fg]
    if not possible_bg_indices:
        bg = random.choice(BG_COLORS)
    else:
        bg = BG_COLORS[random.choice(possible_bg_indices)]

    try:
        banner = pyfiglet.figlet_format(text, font=font)
    except Exception as e:
        # Fallback if font fails
        banner = pyfiglet.figlet_format(text, font="standard")
        font = "standard"

    colored_banner = colored(banner, fg, bg)
    print(colored_banner)
    print("\n" + "=" * 50)
    print("      WELCOME TO BANNER MAKER")
    print("=" * 50)
    print("\n✨ Random banner info:")
    print(f"   Font: {font}")
    print(f"   Text color: {fg}")
    print(f"   Background: {bg}")

    return font, fg, bg


def save_banner_to_file(banner_text, filename):
    """
    Save the plain banner text to a file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(banner_text)
        print(f"\n✅ Banner saved to '{filename}'")
    except Exception as e:
        print(f"\n❌ Error saving banner: {e}")


# ----------------------------------------------------------------------
#  MAIN PROGRAM
# ----------------------------------------------------------------------

def main():
    # Display a random colorful banner for "Jack" as welcome header
    random_banner("Jack")

    # Get user text
    text = input("\nEnter text for the banner: ").strip()
    if not text:
        print("Text cannot be empty. Exiting.")
        sys.exit(1)

    # Choose font (and possibly colors if "Surprise me!")
    font, fg_color, bg_color = choose_font()

    # If not Surprise me! (i.e., colors still None), let user choose colors
    if fg_color is None:
        # Let user choose foreground first
        fg_color = choose_color("=== Foreground (Text) Color ===", FG_COLORS, allow_none=True)
        if fg_color is None:
            print("No text color will be applied.")
        else:
            print("Text color: {}".format(fg_color))
            # When choosing background, forbid same as foreground (if foreground exists)
            forbid = fg_color if fg_color is not None else None
            bg_color = choose_color("=== Background Color ===", BG_COLORS, allow_none=True, forbid_equal=forbid)
        if fg_color is None:
            # If no foreground, background can be any (including no color)
            bg_color = choose_color("=== Background Color ===", BG_COLORS, allow_none=True)

        if bg_color is None:
            print("No background color will be applied.")
        else:
            print("Background color: {}".format(bg_color))

    # Show the final banner and capture the plain text
    print("\n" + "=" * 50)
    print("              YOUR BANNER")
    print("=" * 50)
    banner_plain = display_banner(text, font, fg_color, bg_color)

    # Ask to save the banner to a file
    print("\n" + "=" * 50)
    save_choice = input("Would you like to save this banner to a file? (y/n): ").strip().lower()
    if save_choice in ('y', 'yes'):
        filename = input("Enter filename (default: banner.txt): ").strip()
        if not filename:
            filename = "banner.txt"
        save_banner_to_file(banner_plain, filename)

    # Ask if the user wants to see the reusable code
    print("\n" + "=" * 50)
    show_code = input("Would you like to see the Python code for this banner? (y/n): ").strip().lower()
    if show_code in ('y', 'yes'):
        print("\n" + "=" * 50)
        print("         REUSABLE PYTHON CODE")
        print("=" * 50)
        code = generate_code(text, font, fg_color, bg_color)
        print(code)


if __name__ == "__main__":
    main()