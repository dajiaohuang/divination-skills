# Randomness contract

`sha256-counter-rejection-v1` derives independent card and orientation streams from a 256-bit seed. Card indices use rejection sampling and removal from the remaining deck, preventing modulo bias and duplicates. The output discloses the seed, its commitment, the canonical deck hash, and a draw ID so anyone with the same version can replay the draw.

A user-supplied seed is reproducible but may be chosen strategically. A generated seed uses the operating system cryptographic random source. Neither mode proves supernatural randomness. Never redraw merely because the first result is inconvenient.
