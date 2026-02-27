# Core Word Hcmask Generator

A Python utility designed to generate highly probable, purely alphabetical `.hcmask` files for Hashcat. 

When attacking WPA/WPA2 handshakes or fast hashes, humans rarely use truly random strings of letters. Instead, they build passwords around a pronounceable, constructive **core word** (before appending numbers or symbols). This tool uses Consonant-Vowel (CV) linguistic rules to generate the masks for those core words, skipping the mathematically impossible or highly improbable garbage strings.

## 📉 The Math: Brute Force vs. CV Masking
Why not just use a standard Hashcat brute force attack for 8 lowercase letters (`?l?l?l?l?l?l?l?l`)? 

Because of **keyspace bloat**. The English alphabet has 26 letters (21 consonants, 5 vowels).
* **Standard Brute Force:** $26^8$ = **208,827,064,576** (208.8 Billion combinations).

A massive portion of those 208.8 billion combinations are mathematically impossible for a human to type as a password. For example, the pattern `cccccccc` (8 consonants in a row, like `xwqkpzrt`) accounts for $21^8$ combinations. That is **37.8 Billion** combinations alone—all completely useless!

By automatically filtering out non-human patterns (e.g., dropping masks with 4+ consonants or 3+ vowels in a row), this script reduces the 256 possible CV patterns down to just ~89 highly probable patterns. 

### ⏱️ Time-to-Crack Comparison (RTX 5090)
Here is how that keyspace reduction translates to real-world cracking time against a heavy algorithm like WPA2/PMKID (Assuming an RTX 5090 running at ~4.8 MH/s):

| Attack Type | Total Combinations (Keyspace) | WPA2 Crack Time (RTX 5090) |
| :--- | :--- | :--- |
| **Standard Brute Force (`?l*8`)** | ~208.8 Billion | **~12.1 Hours** |
| **Optimized CV Masks** | ~50.0 Billion | **~2.9 Hours** |

**Result:** You achieve realistic, human-probable password coverage while skipping over 9 hours of wasted GPU compute time.

## ⚙️ Features
* **Interactive CLI:** Step-by-step terminal wizard to set word length and filter rules.
* **Strictly Alphabetical:** Builds all possible permutations of `C` and `V` for a defined word length.
* **Human-Pattern Filtering:** Automatically drops masks that fail basic human-readability limits.
* **Ready for Hashcat:** Outputs directly to the `.hcmask` format, mapping consonants to `?1` and vowels to `?2`.

## 🥊 Masking vs. The Competition
Why use `.hcmask` files instead of traditional tools?
* **Vs. Crunch:** Crunch generates dictionary lists that are saved to your hard drive. A 10-character Crunch list can consume terabytes of storage. Mask attacks generate the password candidates **in-memory** on the fly, requiring zero disk space.
* **Vs. Aircrack-ng:** Aircrack-ng primarily relies on the CPU for dictionary attacks against WPA/WPA2 handshakes, which is painfully slow. Hashcat utilizes the GPU, making it hundreds of times faster.
* **Vs. John the Ripper (JtR):** While JtR is incredible for CPU-based cracking and exotic hash types, Hashcat is the undisputed industry standard for heavily optimized, raw GPU brute-forcing.

## ⚙️ Hardware Acceleration: GPUs & CUDA
Password cracking—especially against heavy algorithms like WPA2's PBKDF2—requires massive parallel processing.
* **Why GPU over CPU?** A high-end CPU might have 16 to 32 complex cores. A modern graphics card contains **thousands** of smaller, specialized arithmetic cores (CUDA cores) capable of calculating thousands of hashes simultaneously. Even an entry-level laptop GPU will drastically outperform a flagship desktop CPU in Hashcat.
* **The Role of VRAM:** While core count dictates your *speed*, GPU VRAM (Video RAM) is critical for capacity. Hashcat loads its compute kernels, the target hashes, and the password candidates into VRAM. Higher VRAM prevents bottlenecks when attacking large lists of captured handshakes simultaneously.
* **NVIDIA CUDA Toolkit:** To allow Hashcat to communicate with your GPU's raw hardware, you **must** install the NVIDIA CUDA Toolkit. It acts as the essential bridge between the cracking software and the silicon.

## 🚀 Usage & GPU Optimization

### 1. Generate the Core Word Masks
Run the script from your terminal. The interactive wizard will ask for your preferred length and filtering rules.

```bash
python generate_masks.py
```

### 2. Use Hashcat with GPU Optimizations
To execute the attack, pass the generated `.hcmask` file directly into Hashcat. To get the right balance of performance and stability out of your graphics card, utilize the workload (`-w`) and device (`-d`) flags.

* **`-w 2` (Stable/Default):** The best profile if you are using your computer for other tasks while cracking in the background. It balances GPU load and system stability.
* **`-w 3` (High):** Highly recommended for dedicated password cracking rigs to keep the GPU fully saturated.
* **`-w 4` (Nightmare):** Maximum utilization. This will likely lag or freeze your desktop display entirely while running.
* **`-d 1` or `-d 2`:** Specifies which OpenCL/CUDA device to use if you have multiple GPUs (e.g., integrated graphics + dedicated NVIDIA GPU).

```bash
# Example against a WPA2/PMKID hash using the stable workload profile
hashcat -m 22000 target_hash.hc22000 core_word_8char.hcmask -a 3 -w 2 -d 1
```

### 3. Advanced Tuning: The Pipeline Hack (Rules + Masks)
Hashcat mask attacks (`-a 3`) do not natively support rule files like `best64.rule`. If you want to take the generated core words and apply rules (like capitalizing the first letter or adding '123' to the end), you can pipe the output directly into a standard wordlist attack (`-a 0`):

```bash
# Generate the words in memory, pipe them, and apply best64.rule
hashcat -a 3 --stdout core_word_8char.hcmask | hashcat -m 22000 target_hash.hc22000 -a 0 -r rules/best64.rule -w 3
```

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

*(Note: Speeds vary based on cooling, overclocks, and specific Hashcat release versions. MH/s = Megahashes per second, GH/s = Gigahashes per second).*

## 🛣️ Roadmap & Future Updates
**Coming Soon:** I am actively developing an extended version of this tool that automatically generates hybrid masks (appending numeric combinations like `?d?d` and special characters directly into the mask patterns). 

Once that repository is live, I will update this section with the direct link. 

## 🛠️ Requirements
* **NVIDIA CUDA Toolkit** (Crucial for NVIDIA GPU acceleration).
* **Hashcat** (Installed and accessible in your system PATH).
* **Python 3.x**
* No external Python libraries required.
