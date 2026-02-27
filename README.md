# Core Word Hcmask Generator

A Python utility designed to generate highly probable, purely alphabetical `.hcmask` files for Hashcat. 

When attacking WPA/WPA2 handshakes or fast hashes, humans rarely use truly random strings of letters. Instead, they build passwords around a pronounceable, constructive **core word** (before appending numbers or symbols). This tool uses Consonant-Vowel (CV) linguistic rules to generate the masks for those core words, skipping the mathematically impossible or highly improbable garbage strings.

## 🧠 Why "Core Word" Masks?
This tool strictly generates alphabetical patterns (a-z). It does **not** append numbers or special characters. 

For an 8-character string of strictly consonants (C) and vowels (V), there are 256 possible pattern combinations. However, the most human-readable "core words" rarely contain:
* 4 or more consecutive consonants.
* 3 or more consecutive vowels.

By mathematically filtering out these non-human patterns, this script reduces the keyspace to only the constructive, probable word shapes. 

## ⚙️ Features
* **Interactive CLI:** Step-by-step terminal wizard to set word length and filter rules.
* **Strictly Alphabetical:** Builds all possible permutations of `C` and `V` for a defined word length.
* **Human-Pattern Filtering:** Automatically drops masks that fail basic human-readability limits.
* **Ready for Hashcat:** Outputs directly to the `.hcmask` format, mapping consonants to `?1` and vowels to `?2`.

## 🚀 Usage & GPU Optimization

### 1. Generate the Core Word Masks
Run the script from your terminal. The interactive wizard will ask for your preferred length and filtering rules.

```bash
python generate_masks.py
```

### 2. Run in Hashcat with GPU Optimizations
Pass the generated `.hcmask` file directly into Hashcat. To get the absolute maximum performance out of your graphics card, utilize the device (`-d`) and workload (`-w`) flags.

* `-w 3` or `-w 4`: Increases the workload profile. `-w 3` is highly recommended for password cracking rigs to keep the GPU fully saturated. `-w 4` is "nightmare" mode and may make your desktop lag entirely while running.
* `-d 1` or `-d 2`: Specifies which OpenCL/CUDA device to use if you have multiple GPUs (e.g., integrated graphics + dedicated NVIDIA GPU).

```bash
# Example against a WPA2/PMKID hash using maximum GPU utilization
hashcat -m 22000 target_hash.hc22000 core_word_8char.hcmask -a 3 -w 3 -d 1
```

## 📊 Hardware Performance Benchmarks
Because this tool reduces the overall keyspace, it allows slower cards to punch above their weight. Below are estimated benchmark speeds for popular NVIDIA GPUs across WPA2 and other common fast hashes (MD5, NTLM, SHA1, SHA256) when running mask attacks.

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
**Coming Soon:** I am actively developing an extended version of this tool that automatically generates hybrid masks (appending numeric combinations like `?d?d` and special characters to these core words). 

Once that repository is live, I will update this section with the direct link. For now, you can append digit masks manually in Hashcat alongside this generated wordlist!

## 🛠️ Requirements
* Python 3.x
* No external libraries required.
