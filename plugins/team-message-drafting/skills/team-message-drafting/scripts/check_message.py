#!/usr/bin/env python3
"""Flag formatting and phrasing in a chat-message draft that reads as AI-written.

Reads the draft from stdin (or a file path argument) and prints one line per finding.
Exits 1 if anything was found, 0 if the draft is clean.
"""
import re
import sys

PATTERNS = [
    (r"[—–]", "em or en dash; use a comma, full stop or brackets"),
    (r"\s--\s", "double hyphen used as a dash"),
    (r"\*\*[^*]+\*\*|__[^_]+__", "bold markdown"),
    (r"(?m)^[ \t]*#{1,6}\s", "markdown heading"),
    (r"(?m)^[ \t]*>", "blockquote"),
    (r"(?m)^[ \t]*[-*•]\s", "bullet list"),
    (r"(?m)^[ \t]*\d+[.)]\s", "numbered list"),
    (r"`", "backtick code formatting"),
    (r"!.*!", "more than one exclamation mark"),
]

PHRASES = [
    "hope this message finds you", "hope this finds you", "hope you're well", "hope you are well",
    "just wanted to reach out", "wanted to reach out", "reaching out", "quick question", "quick ones",
    "touch base", "circle back", "great question", "happy to help", "thanks in advance",
    "let me know if you have any questions", "don't hesitate", "do not hesitate",
    "a few things to flag", "to summarise", "to summarize", "in summary",
    "ensure", "leverage", "streamline", "robust", "seamless", "delve", "furthermore",
    "additionally", "moreover", "i wanted to", "as per", "kindly",
]


def check(text):
    findings = []
    for pattern, message in PATTERNS:
        for match in re.finditer(pattern, text):
            line = text.count("\n", 0, match.start()) + 1
            findings.append(f"line {line}: {message}: {match.group(0).strip()[:40]!r}")
    lowered = text.lower()
    for phrase in PHRASES:
        if re.search(r"\b" + re.escape(phrase) + r"\b", lowered):
            findings.append(f"stock phrase: {phrase!r}")
    words = len(text.split())
    if words > 120:
        findings.append(f"{words} words; most chat messages should be under about 80")
    if text.count("?") > 2:
        findings.append(f"{text.count('?')} questions; research the ones you can answer yourself")
    return findings


def main():
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    findings = check(text)
    for finding in findings:
        print(finding)
    if not findings:
        print("clean")
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
