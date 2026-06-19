import argparse
import hashlib
import random
import sys
import os

try:
    from rich.prompt import Prompt, Confirm
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.theme import Theme
    from rich.table import Table
    # Setup UiPro Pro Max aesthetic theme (OLED Dark Mode)
    uipro_theme = Theme({
        "primary": "#F8FAFC",         # Pure text
        "secondary": "#1E293B",       # Borders, structural elements
        "accent": "bold #22C55E",     # Success / CTA Green
        "bg": "on #020617",           # Deep OLED Black
        "dim": "#475569",             # Muted text
        "danger": "bold #EF4444"      # Errors
    })
    console = Console(theme=uipro_theme)
except ImportError:
    print("Please install 'rich' to use the interactive menu: pip install rich")
    sys.exit(1)

ZW_SPACE = '\u200B'       # Represents '0'
ZW_NON_JOINER = '\u200C'  # Represents '1'
ZW_JOINER = '\u200D'      # Delimiter between bytes

COVER_EMOJIS = [
    "😈", "👁️", "💀", "👻", "🔥", "⚡", "🦇", "🕷️", 
    "🔮", "🌙", "💎", "🤖", "👽", "🦊", "🐺", "🦅", 
    "🦄", "💣", "🔑", "🔒", "💌", "🛸", "⚔️", "☠️"
]

def get_prng(password):
    """Generates a seeded random number generator based on the password."""
    seed = int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16)
    return random.Random(seed)

def encode(text, password, cover_emoji):
    """Encodes UTF-8 text into Zero-Width Characters bound to a Cover Emoji."""
    r = get_prng(password)
    text_bytes = text.encode('utf-8')
    zw_chars = []
    
    for b in text_bytes:
        offset = r.randint(0, 255)
        encrypted_byte = (b + offset) % 256
        
        # Convert byte to 8-bit binary string
        binary_str = format(encrypted_byte, '08b')
        
        # Map 0 to ZW_SPACE and 1 to ZW_NON_JOINER
        zw_byte = binary_str.replace('0', ZW_SPACE).replace('1', ZW_NON_JOINER)
        zw_chars.append(zw_byte)
        
    # Join bytes with ZW_JOINER and prepend cover emoji
    payload = ZW_JOINER.join(zw_chars)
    return cover_emoji + payload

def decode(stego_text, password):
    """Decodes Zero-Width Steganography back into UTF-8 text."""
    r = get_prng(password)
    
    # Extract only the Zero-Width characters
    zw_only = ''.join(c for c in stego_text if c in (ZW_SPACE, ZW_NON_JOINER, ZW_JOINER))
    
    if not zw_only:
        print("[ERR] No hidden data detected in file.")
        sys.exit(1)
        
    zw_bytes = zw_only.split(ZW_JOINER)
    decoded_bytes = bytearray()
    
    for zw_byte in zw_bytes:
        if not zw_byte:
            continue
            
        binary_str = zw_byte.replace(ZW_SPACE, '0').replace(ZW_NON_JOINER, '1')
        
        if len(binary_str) != 8:
            print("[ERR] File is corrupted. Malformed zero-width data.")
            sys.exit(1)
            
        encrypted_byte = int(binary_str, 2)
        offset = r.randint(0, 255)
        b = (encrypted_byte - offset) % 256
        decoded_bytes.append(b)
        
    try:
        return decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        print("[ERR] Decryption failed. Invalid key provided.")
        sys.exit(1)

def display_emoji_grid():
    """Displays a grid of cover emojis to select from."""
    table = Table(show_header=False, show_edge=False, box=None)
    
    cols = 8
    rows = [COVER_EMOJIS[i:i + cols] for i in range(0, len(COVER_EMOJIS), cols)]
    
    for row in rows:
        formatted_row = []
        for emoji in row:
            idx = COVER_EMOJIS.index(emoji) + 1
            formatted_row.append(f"[dim][{idx:02d}][/] {emoji}")
        table.add_row(*formatted_row)
        
    console.print(Panel(table, title="[primary bg] COVER EMOJI SELECTOR [/]", border_style="secondary", style="bg"))

def run_interactive():
    header = Text("BESTY ZERO-WIDTH ENGINE", justify="center", style="primary")
    panel = Panel(header, border_style="secondary", style="bg", padding=(1, 4), title="[primary bg] Steganography Module [/]", subtitle="[primary bg] v2.0.4 [/]")
    console.print(panel)
    console.print()
    
    action = Prompt.ask("[primary]Select Protocol[/] [dim](encode/decode/text-encode/text-decode)[/]", choices=["encode", "decode", "text-encode", "text-decode"], console=console)
    
    is_text = action.startswith("text-")
    base_action = action.replace("text-", "")
    
    if not is_text:
        target_input = Prompt.ask("[primary]Target File Path[/]", console=console)
        if not os.path.exists(target_input):
            console.print(f"\n[danger][ERR] File '{target_input}' not found in filesystem.[/danger]")
            console.print("[dim]Tip: If you want to encode plain text instead of a file, choose 'text-encode' as the protocol.[/dim]")
            sys.exit(1)
    else:
        if base_action == "encode":
            target_input = Prompt.ask("[primary]Secret Text to Encode[/]", console=console)
        else:
            target_input = Prompt.ask("[primary]Stego-Emoji to Decode[/]", console=console)
            
    password = Prompt.ask("[primary]Encryption Key[/] [dim](Press Enter to skip)[/]", password=True, default="", console=console)
    
    cover_emoji = "😈"
    if base_action == "encode":
        console.print()
        display_emoji_grid()
        choice = Prompt.ask("[primary]Select Cover Emoji ID[/] [dim](1-24)[/]", default="1", console=console)
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(COVER_EMOJIS):
                cover_emoji = COVER_EMOJIS[idx]
        except ValueError:
            pass
    
    if not is_text:
        console.print(f"\n[secondary]>[/] [primary]Initializing {base_action.upper()} protocol on file...[/]")
        process_file(base_action, target_input, password, cover_emoji)
    else:
        console.print(f"\n[secondary]>[/] [primary]Initializing TEXT-{base_action.upper()} protocol...[/]")
        process_text(base_action, target_input, password, cover_emoji)

def process_text(action, text_input, password, cover_emoji="😈"):
    if action == "encode":
        result = encode(text_input, password, cover_emoji)
        console.print(Panel(result, title="[accent bg] STEGO-EMOJI RESULT (COPY THIS) [/]", border_style="accent", style="bg"))
        console.print("[dim]The text above looks like a normal emoji, but your encrypted data is hidden inside it using zero-width characters![/dim]")
    elif action == "decode":
        result = decode(text_input, password)
        console.print(Panel(result, title="[accent bg] DECODED SECRET MESSAGE [/]", border_style="accent", style="bg"))

def process_file(action, file_path, password, cover_emoji="😈"):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if action == "encode":
        result = encode(content, password, cover_emoji)
        base_name = os.path.splitext(file_path)[0]
        out_file = base_name + ".besty"
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        success_msg = Text(f"BOUND TO: {cover_emoji} -> {out_file}", style="accent bg")
        console.print(Panel(success_msg, border_style="secondary", style="bg", title="[secondary bg] STATUS: SUCCESS [/]"))
        
    elif action == "decode":
        result = decode(content, password)
        base_name = os.path.splitext(file_path)[0]
        if file_path.endswith(".besty"):
            out_file = base_name + ".decoded.txt"
        else:
            out_file = file_path + ".decoded.txt"
            
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(result)
            
        success_msg = Text(f"EXTRACTED: {out_file}", style="accent bg")
        preview = result[:200] + ("..." if len(result) > 200 else "")
        
        console.print(Panel(success_msg, border_style="secondary", style="bg", title="[secondary bg] STATUS: SUCCESS [/]"))
        console.print(f"\n[secondary]--- DECODED PREVIEW ---[/]\n[primary]{preview}[/]")

def main():
    if len(sys.argv) == 1:
        run_interactive()
        return

    if len(sys.argv) == 2 and sys.argv[1] == "update":
        console.print("\n[accent]>[/] [primary]Fetching latest Zero-Width Steganography updates from PyPI...[/]")
        os.system(f"{sys.executable} -m pip install --upgrade irl-besty")
        console.print("[accent]Update complete. You are now running the latest engine.[/]\n")
        return

    parser = argparse.ArgumentParser(description="Besty Zero-Width Engine")
    parser.add_argument("action", choices=["encode", "decode"], help="Action to perform")
    parser.add_argument("file", help="Target file path")
    parser.add_argument("--password", "-p", default="", help="Encryption key (optional)")
    parser.add_argument("--emoji", "-e", default="😈", help="Cover emoji (for encoding)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"[ERR] File '{args.file}' doesn't exist.")
        sys.exit(1)
        
    process_file(args.action, args.file, args.password, args.emoji)

if __name__ == "__main__":
    main()

