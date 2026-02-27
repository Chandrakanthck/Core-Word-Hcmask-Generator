import itertools

def generate_masks(length, max_c, max_v, output_file):
    # Define the custom character sets
    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou"
    placements = ['c', 'v']

    print(f"\n[*] Generating all C/V combinations for core word length {length}...")
    all_combinations = [''.join(p) for p in itertools.product(placements, repeat=length)]
    
    # Create the filter strings
    bad_c_pattern = 'c' * max_c
    bad_v_pattern = 'v' * max_v

    def is_valid_pattern(pattern):
        # Reject if too many consecutive consonants
        if bad_c_pattern in pattern:
            return False
        # Reject if too many consecutive vowels
        if bad_v_pattern in pattern:
            return False
        return True

    print(f"[*] Applying linguistic filters (Max consecutive C: {max_c-1}, Max consecutive V: {max_v-1})...")
    filtered_patterns = [p for p in all_combinations if is_valid_pattern(p)]

    # Write the valid patterns to the Hashcat mask file
    with open(output_file, "w") as f:
        for pattern in filtered_patterns:
            # Translate 'c' and 'v' to Hashcat custom charset placeholders (?1 and ?2)
            hc_pattern = pattern.replace('c', '?1').replace('v', '?2')
            
            # Format: custom_charset_1, custom_charset_2, mask
            line = f"{consonants},{vowels},{hc_pattern}\n"
            f.write(line)

    print(f"\n[+] Success! Reduced {len(all_combinations)} combinations down to {len(filtered_patterns)} optimal core word patterns.")
    print(f"[+] Saved ready-to-use Hashcat masks to: {output_file}\n")

if __name__ == "__main__":
    print("=== Core Word Hcmask Generator ===")
    
    # Get Length
    try:
        l_input = input("Enter core word length [Default: 8]: ").strip()
        length = int(l_input) if l_input else 8
    except ValueError:
        print("Invalid input. Defaulting to 8.")
        length = 8

    # Get Max Consonants
    try:
        c_input = input("Drop patterns with this many consecutive CONSONANTS [Default: 4]: ").strip()
        max_c = int(c_input) if c_input else 4
    except ValueError:
        print("Invalid input. Defaulting to 4.")
        max_c = 4

    # Get Max Vowels
    try:
        v_input = input("Drop patterns with this many consecutive VOWELS [Default: 3]: ").strip()
        max_v = int(v_input) if v_input else 3
    except ValueError:
        print("Invalid input. Defaulting to 3.")
        max_v = 3

    # Get Output Filename
    o_input = input(f"Enter output filename [Default: core_word_{length}char.hcmask]: ").strip()
    output_file = o_input if o_input else f"core_word_{length}char.hcmask"

    # Run the generator
    generate_masks(length, max_c, max_v, output_file)