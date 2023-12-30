def kmp_search(text, pattern):
    lps = get_pi(pattern)
    i, j = 0, 0
    result = []
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            result.append(i-len(pattern))
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return result


def get_pi(pattern):
    length = 0
    pi = [0] * len(pattern)
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            pi[i] = length
            i += 1
        else:
            if length != 0:
                length = pi[length - 1]
            else:
                pi[i] = 0
                i += 1

    return pi


def _dfa_setting(pattern):
    alphabet = set(pattern)
    dfa = [{ch: 0 for ch in alphabet} for _ in range(len(pattern) + 1)]
    dfa[0][pattern[0]] = 1

    x = 0
    for j in range(1, len(pattern)):
        for ch in alphabet:
            dfa[j][ch] = dfa[x][ch]
        dfa[j][pattern[j]] = j + 1
        x = dfa[x][pattern[j]]

    return dfa


def dfa_search(text, pattern):
    dfa = _dfa_setting(pattern)
    n, m = len(text), len(pattern)
    state = 0
    result = []
    for i in range(n):
        if text[i] in dfa[state]:
            state = dfa[state][text[i]]
        else:
            state = 0
        if state == m:
            result.append(i-len(pattern))
    return result
