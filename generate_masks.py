import itertools

def generate_masks(length, max_c, max_v, c_chars, v_chars, case_mode, output_file):
    print(f"\n[*] Generating all C/V combinations for core word length {length}...")
    placements = ['c', 'v']
    all_combinations = [''.join(p) for p in itertools.product(placements, repeat=length)]
    
    # Create the filter strings
    bad_c_pattern = 'c' * max_c
    bad_v_pattern = 'v' * max_v

    def is_valid_pattern(pattern):
        if bad_c_pattern in pattern: return False
        if bad_v_pattern in pattern: return False
        return True

    print(f"[*] Applying linguistic filters (Max consecutive C: {max_c-1}, Max consecutive V: {max_v-1})...")
    filtered_patterns = [p for p in all_combinations if is_valid_pattern(p)]

    # Setup Character Sets based on user casing choice
    c_lower, v_lower = c_chars.lower(), v_chars.lower()
    c_upper, v_upper = c_chars.upper(), v_chars.upper()
    c_mixed, v_mixed = c_lower + c_upper, v_lower + v_upper

    with open(output_file, "w") as f:
        for pattern in filtered_patterns:
            hc_pattern = ""
            charset_line = ""

            # Mode 1: All Lowercase (Uses ?1, ?2)
            if case_mode == '1':
                hc_pattern = pattern.replace('c', '?1').replace('v', '?2')
                charset_line = f"{c_lower},{v_lower},{hc_pattern}\n"

            # Mode 2: All Uppercase (Uses ?1, ?2)
            elif case_mode == '2':
                hc_pattern = pattern.replace('c', '?1').replace('v', '?2')
                charset_line = f"{c_upper},{v_upper},{hc_pattern}\n"

            # Mode 3: Title Case (First Cap, Rest Lower) (Uses ?1, ?2 for Upper, ?3, ?4 for Lower)
            elif case_mode == '3':
                for i, char in enumerate(pattern):
                    if i == 0: # First Letter
                        hc_pattern += '?1' if char == 'c' else '?2'
                    else:      # Rest of Letters
                        hc_pattern += '?3' if char == 'c' else '?4'
                charset_line = f"{c_upper},{v_upper},{c_lower},{v_lower},{hc_pattern}\n"

            # Mode 4: Mixed Case (Uses ?1, ?2)
            elif case_mode == '4':
                hc_pattern = pattern.replace('c', '?1').replace('v', '?2')
                charset_line = f"{c_mixed},{v_mixed},{hc_pattern}\n"

            # Mode 5: Inverted Title Case (First Lower, Rest Upper)
            elif case_mode == '5':
                for i, char in enumerate(pattern):
                    if i == 0: # First Letter
                        hc_pattern += '?1' if char == 'c' else '?2'
                    else:      # Rest of Letters
                        hc_pattern += '?3' if char == 'c' else '?4'
                charset_line = f"{c_lower},{v_lower},{c_upper},{v_upper},{hc_pattern}\n"

            f.write(charset_line)

    print(f"\n[+] Success! Reduced {len(all_combinations)} combinations down to {len(filtered_patterns)} optimal core word patterns.")
    print(f"[+] Saved ready-to-use Hashcat masks to: {output_file}\n")

if __name__ == "__main__":
    print("=== Core Word Hcmask Generator (v2.0 Advanced) ===")
    
    # 1. Get Length
    l_input = input("Enter core word length [Default: 8]: ").strip()
    length = int(l_input) if l_input else 8

    # 2. Get Filters
    c_input = input("Drop patterns with this many consecutive CONSONANTS [Default: 4]: ").strip()
    max_c = int(c_input) if c_input else 4

    v_input = input("Drop patterns with this many consecutive VOWELS [Default: 3]: ").strip()
    max_v = int(v_input) if v_input else 3

    # 3. Custom Alphabets
    print("\n--- Alphabet Customization ---")
    print("Tip: Remove rare letters (q, x, z, j) to drastically speed up cracking time.")
    def_c = "bcdfghjklmnpqrstvwxyz"
    cust_c = input(f"Enter CONSONANTS to use [Default: {def_c}]: ").strip()
    c_chars = cust_c if cust_c else def_c

    def_v = "aeiou"
    cust_v = input(f"Enter VOWELS to use [Default: {def_v}]: ").strip()
    v_chars = cust_v if cust_v else def_v

    # 4. Casing Modes
    print("\n--- Capitalization Modes ---")
    print("1) All Lowercase (default)")
    print("2) All Uppercase (DEFAULT)")
    print("3) Title Case (First letter Capital, rest lowercase)")
    print("4) Mixed Case (Upper + Lower combined)")
    print("5) Inverted Title (First letter lowercase, rest Capital)")
    
    case_input = input("Select casing mode (1-5) [Default: 1]: ").strip()
    case_mode = case_input if case_input in ['1', '2', '3', '4', '5'] else '1'

    # 5. Output
    o_input = input(f"\nEnter output filename [Default: core_word_{length}char_mode{case_mode}.hcmask]: ").strip()
    output_file = o_input if o_input else f"core_word_{length}char_mode{case_mode}.hcmask"

    # Run the generator
    generate_masks(length, max_c, max_v, c_chars, v_chars, case_mode, output_file)
