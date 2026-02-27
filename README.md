# Core Word Hcmask Generator (v2.0)

A highly customizable Python utility designed to generate highly probable, purely alphabetical `.hcmask` files for Hashcat. 

When attacking WPA/WPA2 handshakes or fast hashes, humans rarely use truly random strings of letters. Instead, they build passwords around a pronounceable, constructive **core word**. This tool uses Consonant-Vowel (CV) linguistic rules to generate the masks for those core words, skipping the mathematically impossible garbage strings and allowing the cracker complete control over the alphabet and capitalization.

## 🧠 Why "Core Word" Masks?
This tool strictly generates alphabetical patterns (a-z). It does **not** append numbers or special characters. 

For an 8-character string of strictly consonants (C) and vowels (V), there are 256 possible pattern combinations. However, the most human-readable "core words" rarely contain 4+ consecutive consonants or 3+ consecutive vowels. By mathematically filtering out these non-human patterns, this script reduces the keyspace to only the constructive, probable word shapes. 

## 🎯 Advanced Cracker Tactics (v2.0 Features)

### 1. Custom Alphabet Filtering (The "Rare Letter" Drop)
In v2.0, you are no longer forced to use all 26 letters of the English alphabet. Pentesters know that letters like **Q, X, Z, and J** are rarely used in standard naming conventions or base words. 
* By removing just those 4 consonants from your custom alphabet, you drastically reduce the mathematical keyspace, shaving hours or even days off your total cracking time while maintaining high probability coverage.

### 2. Native Capitalization Routing
Standard mask attacks usually require piping output to apply rules (like capitalizing the first letter). This tool is smarter. It natively formats the `.hcmask` file utilizing Hashcat's four custom charset slots (`?1`, `?2`, `?3`, `?4`) to enforce casing rules directly in the mask.
* **Mode 3 (Title Case):** Automatically assigns Capital letters to the first position (`?1` or `?2`) and lowercase to the rest (`?3` or `?4`), perfectly mimicking the most common human password habit.
* **Available Modes:** All Lowercase, All Uppercase, Title Case, Mixed Case, and Inverted Title.

## 📉 The Math: Brute Force vs. CV Masking
Why not just use a standard Hashcat brute force attack for 8 lowercase letters (`?l?l?l?l?l?l?l?l`)? 

Because of **keyspace bloat**. The English alphabet has 26 letters.
* **Standard Brute Force:** $26^8$ = **208.8 Billion** combinations.

A massive portion of those combinations are mathematically impossible for a human to type. The pattern `cccccccc` (8 consonants in a row, like `xwqkpzrt`) accounts for **37.8 Billion** combinations alone—all completely useless!

By filtering out non-human patterns and dropping rare letters, this script reduces your keyspace by over **80%**, allowing you to crack highly probable words in a fraction of the time.

## 🚀 Usage & GPU Optimization

### 1. Generate the Core Word Masks
Run the script from your terminal. The interactive wizard will guide you through length, filtering, custom alphabets, and casing modes.

```bash
python generate_masks.py
```

### 2. Use Hashcat with GPU Optimizations
Pass the generated `.hcmask` file directly into Hashcat. To get the absolute maximum performance out of your graphics card, utilize the device (`-d`) and workload (`-w`) flags.

* **`-w 2` (Stable/Default):** The best profile if you are using your computer for other tasks while cracking.
* **`-w 3` (High):** Highly recommended for dedicated password cracking rigs to keep the GPU fully saturated.
* **`-w 4` (Nightmare):** Maximum utilization. This will likely freeze your desktop display while running.

```bash
# Example against a WPA2/PMKID hash using the stable workload profile
hashcat -m 22000 target_hash.hc22000 masks -a 3 -w 2 -d 1
```

## ⚡ Quick Start Guide & Real-World Example

To see the power of v2.0, follow this example to create a surgical strike on an 8-character core word:

1. **Launch the script:** `python generate_masks.py`
2. **Set strict limits:** Choose **3** for consonants and **2** for vowels. This tells the script to only include patterns with 1-2 consonants or 1 vowel in a row.
3. **Filter the Alphabet:** Remove rare letters by entering `bcdghklmnprstvy` as your consonants.
4. **Choose Casing:** Select **Mode 1** for All Lowercase.
5. **Output:** Name the file `masks`.

**The result:** You just reduced **256** possible patterns down to **16** highly optimal core word patterns.

### Expected Output Example
Your `masks` file will contain optimized lines that look like this:
```text
bcdghklmnprstvy,aeiou,?1?1?2?1?1?2?1?1
bcdghklmnprstvy,aeiou,?1?1?2?1?1?2?1?2
... (14 more optimized patterns)
```
Each line tells Hashcat exactly which characters to use for `?1` and `?2`, ensuring your **GTX 1650 Ti** (or higher) is only checking high-probability human words.

## 📊 Hardware Performance Benchmarks
Below are estimated benchmark speeds for popular NVIDIA GPUs across WPA2 and other common fast hashes (MD5, NTLM, SHA1, SHA256) when running mask attacks.

| GPU Architecture | WPA2 (22000) | MD5 (0) | NTLM (1000) | SHA1 (100) | SHA256 (1400) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RTX 5090** *(Est.)* | ~4.8 MH/s | ~220 GH/s | ~350 GH/s | ~75 GH/s | ~32 GH/s |
| **RTX 4090** | 3.5 MH/s | 164 GH/s | 265 GH/s | 53 GH/s | 23 GH/s |
| **RTX 3090** | 2.1 MH/s | 99 GH/s | 145 GH/s | 31 GH/s | 13 GH/s |
| **GTX 1080 Ti** | 650 kH/s | 39 GH/s | 55 GH/s | 12 GH/s | 5.2 GH/s |
| **GTX 1660 Ti** | 350 kH/s | 20 GH/s | 28 GH/s | 6.5 GH/s | 2.6 GH/s |
| **GTX 1650 Ti** | 180 kH/s | 11 GH/s | 15 GH/s | 3.2 GH/s | 1.3 GH/s |
| **GTX 1650** | 150 kH/s | 9 GH/s | 12 GH/s | 2.8 GH/s | 1.1 GH/s |

*(Note: Speeds vary based on cooling, overclocks, and specific Hashcat release versions).*

## 🛣️ Roadmap & Future Updates
**Coming Soon:** I am actively developing an extended version of this tool that automatically generates hybrid masks (appending numeric combinations like `?d?d` and special characters directly into the mask patterns). 

Once that repository is live, I will update this section with the direct link. 

## 🛠️ Requirements
* **NVIDIA CUDA Toolkit** (Crucial for NVIDIA GPU acceleration).
* **Hashcat** (Installed and accessible in your system PATH).
* **Python 3.x**
* No external Python libraries required.
