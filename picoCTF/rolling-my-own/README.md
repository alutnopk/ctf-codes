# Rolling My Own
The binary hosted at `nc mercury.picoctf.net 23773` (as of today) gets a SIGILL upon execution for most input passwords. Static analysis shows that the binary actually uses the password to generate machine instructions; if they are valid, the program outputs the flag.
Some more details:

- Maximum password length is 16 characters, logically split into 4*4 words.
- Each word is appended with 8 characters from a hardcoded salt.
- Each of these 12-byte chunks is MD5 hashed, and a subarray of 4 bytes is extracted from the digest.
- These subarrays (4*4 = 16 bytes) are concatenated and written to memory.
- This memory block is then `call`ed, with `$rdi` holding the address to a special routine, which prints the flag if the first argument its called with equals 0x7B3DC26F1.

A hint shows that the password begins with `D1v1`, which upon processing produces the instruction `mov $rsi, $rdi` (Intel syntax) with a trailing `0x48` byte. Guessing the following instructions to be simply `mov $rdi, 0x7B3DC26F1` and `call $rsi` (which is actually correct in this scenario), one can assemble these instructions using `radare2`, `nasm` or any suitable tool to obtain the probable contents of the memory block.

The next obvious step is to search each word from the input such that its corresponding salted hashed subarray equals our guess. Brute force ftw.

These ideas are implemented in [solve.py](./solve.py).