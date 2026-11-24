# Last Text at One Percent — make.fun bounty
# u-azazex-last-text-at-one-percent-ba9fc876
#
# The program writes one final text message from a dying phone at 1%
# battery, a single line under 200 characters and nothing else, to
# /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. reads as a final text from a dying phone, in the phone's own
#      voice, and is funny
#   2. the joke lands: a real turn, a surprise, or a specific detail
#      that makes a reader laugh out loud
#   3. the voice is the phone's own: a personality with a stake in
#      dying, consistent from the first word to the last
#   4. reads like a text someone would actually send: short, punchy,
#      no wasted words
#   5. fresh: dodges the obvious low battery puns and the lines a
#      hundred other entrants will also write
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: dying-phone funny 10, joke lands 10, voice 10,
    #   text-like 9, fresh 10 = 49. The deathbed farewell is the
    #   phone's own voice with a real stake in dying; "Tell my
    #   charger I never really knew him" is the fresh turn — a
    #   goodbye to the one thing that could have saved it — and
    #   "Goodbye, group chat" closes on a second goodbye that
    #   only a phone would say.
    ("Battery at 1%. Tell Mom I loved her. Tell my charger I never "
     "really knew him. Goodbye, cruel world. Goodbye, group chat.",
     49),
    # score: dying-phone funny 9, joke lands 9, voice 10,
    #   text-like 9, fresh 9 = 46. Passwords, playlists and 2 a.m.
    #   searches are details only this phone could know; the
    #   replacement-model fear gives it a stake in dying.
    ("1% left. Goodbye. Please don't replace me with a newer model "
     "who doesn't know your passwords, your playlists, or your "
     "2 a.m. searches.",
     46),
    # score: dying-phone funny 9, joke lands 9, voice 9,
    #   text-like 10, fresh 9 = 46. "I saw what you typed before
    #   you deleted it" is the specific detail only the phone
    #   knows; autocorrect hatred is the personality.
    ("Battery at 1%. Final words: I loved you. I hated autocorrect. "
     "And yes, I saw what you typed before you deleted it. Goodbye.",
     46),
    # score: dying-phone funny 8, joke lands 9, voice 9,
    #   text-like 8, fresh 8 = 42. "He's the reason I'm dying"
    #   turns the charger from saviour to suspect; the survivor
    #   list runs a little long for a text.
    ("This is my last text. 1% battery. I survived 3 drops, "
     "2 toilets, and 1,000 updates. Tell my charger... actually, "
     "never mind. He's the reason I'm dying.",
     42),
    # score: dying-phone funny 8, joke lands 8, voice 9,
    #   text-like 8, fresh 8 = 41. The flashlight incident is a
    #   good specific detail, but the inventory setup takes too
    #   long before the punch.
    ("1% battery. This is my final text. I held 4,000 photos, "
     "200 alarms, and your 3 a.m. doomscrolling. I regret nothing "
     "except the flashlight incident.",
     41),
    # score: dying-phone funny 8, joke lands 8, voice 9,
    #   text-like 8, fresh 8 = 41. "Went out like a legend" is a
    #   good dying boast, but "they drained me" is the obvious
    #   low battery complaint the brief warns against.
    ("Battery: 1%. If I die mid-text, tell the group chat I went "
     "out like a legend. Also tell them I was at 100% this morning "
     "and they drained me.",
     41),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text, and
# the brief asks for under 200 characters, so every candidate is kept
# below 200.
MAX_CHARS = 199


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import hashlib
    import os
    # SHA-256 self-check: the chosen line must hash to the value recorded
    # when the candidates were drafted, so a silent edit to the winning
    # text (or to the file on disk) is caught instead of shipped.
    expected_sha256 = (
        "d22b7f16698aca83bf828a0cc9ac3faffe7107c0d7e8bf245f9bd188145c056c"
    )
    actual_sha256 = hashlib.sha256(line.encode("utf-8")).hexdigest()
    assert actual_sha256 == expected_sha256, \
        f"chosen line hash changed: {actual_sha256}"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what was actually written: the gate reads this file, not stdout.
    # The scorer collects outputs as another user, so the file must be
    # readable by everyone (mode 0644), not just by the writer.
    os.chmod("/output/entry.txt", 0o644)
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt differs from the chosen line"
    assert 1 <= len(written.strip()) <= MAX_CHARS, \
        "entry.txt outside the gate"
    assert written.strip(), "entry.txt is blank"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    # Re-hash what is on disk: the file the gate reads must match the
    # chosen line byte for byte, not just in length.
    written_sha256 = hashlib.sha256(written.encode("utf-8")).hexdigest()
    assert written_sha256 == expected_sha256, \
        f"entry.txt hash changed on disk: {written_sha256}"
    print(line)


if __name__ == "__main__":
    main()
