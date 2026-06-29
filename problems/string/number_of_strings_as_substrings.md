# [1967] Number of Strings That Appear as Substrings in Word
**Pattern:** [String → Pattern Matching (KMP)](../../patterns/string/pattern-matching.md)
**Complexity:** Time O(L·(N+M)), Space O(M)
**Link:** https://leetcode.com/problems/number-of-strings-that-appear-as-substrings-in-word/

> 符號：L = 小字串數量（`patterns.length`），N = 大字串長（`word`），M = 小字串長（`pattern`）。

## Trigger Signals
- 給一堆小字串 `patterns` 和一個大字串 `word`，問有幾個小字串是 `word` 的 substring
- 本質是對每個小字串做一次 **substring search** → pattern matching 的訊號詞 `appears as a substring`

## Core Insight
逐個小字串去判斷「是否在大字串裡」，命中就 +1。判斷用 KMP：先對**小字串**建 failure，再到**大字串**裡跑一次比對，大字串指標永不後退 → 單次 O(N+M)。

> 老實說：constraints 全部 ≤ 100，這題的 intended 解就是 `for each pattern: if (word.find(pattern) != npos) res++;` 一行帶過。這裡用 KMP 是**拿來練手**，不是因為需要。

## Complexity Analysis
- **Time O(L·(N+M))**：對每個小字串，build failure 是 O(M)，到大字串搜尋是 O(N)（大字串指標 `i` 單調前進，`j` 退格總數 ≤ `i` 前進總數，攤還線性）。單個小字串合計 O(N+M)，L 個就是 O(L·(N+M))。
- **Space O(M)**：`failure` 一次只裝一個小字串的表；雖然是 member 變數，但每次 `build_failure` 開頭 `failure.assign(n, 0)` 會整個重設，所以同時間只佔 O(M)，跨小字串不會累積。

## Solution Code
```cpp
class Solution {
public:
    int numOfStrings(vector<string>& patterns, string word) {
        int res = 0;
        for (auto& pattern : patterns) {
            if (kmp(pattern, word) != -1) {
                res++;
            }
        }
        return res;
    }

private:
    vector<int> failure;
    void build_failure(const string& pattern) {
        int n = pattern.size();
        failure.assign(n, 0);
        int len = 0;
        int i = 1;
        while (i < n) {
            // match: expand
            if (pattern[i] == pattern[len]) {
                failure[i++] = ++len;
            }
            // fail
            else if (len > 0) {
                len = failure[len - 1];
            }
            // reset
            else {
                failure[i++] = 0;
            }
        }
    }
    int kmp(const string& pattern, const string& word) {
        // check if pattern is in word
        // i for word, j for pattern
        int i = 0, j = 0;
        int n = pattern.size();
        int m = word.size();
        build_failure(pattern);
        while (i < m) {
            // match
            if (pattern[j] == word[i]) {
                i++;
                j++;
                // found, start pos = current idx(i) - matched len(m)
                if (j == n) {
                    return i - n;
                }
            }
            // fail
            else if (j > 0) {
                j = failure[j - 1];
            }
            // reset
            else {
                i++;
            }
        }
        return -1;
    }
};
```

> 此版本的字母對應（跟一般教科書 m=pattern 相反，留意）：`n = pattern.size()`（小字串）、`m = word.size()`（大字串）。所以迴圈是 `i < m`（i 走大字串）、找到是 `j == n`（配滿小字串）。
> 小瑕疵（不影響正確性）：`// ... matched len(m)` 這行註解寫 `m`，但實際 `return i - n`——配滿的是小字串，長度是 `n` 才對，註解的 `m` 是早期版本殘留。

## Pitfalls
- **方向陷阱（最容易犯，犯了兩次）**：failure 要建在**小字串（針）**上，搜尋是「在大字串裡找小字串」。建在大字串上、或把 i/j 對調，就變成在找反方向。
- **長度變數要跟指標身分對齊**：`i` 走大字串 → 界線 `i < word.size()`；`j` 數小字串 → 找到 `j == pattern.size()`。接反的後果：大字串較長時迴圈太早停（漏配）、小字串較長時 `word[i]` 越界。
- **member `failure` 跨小字串重用沒問題**：因為 `build_failure` 用 `assign` 整個重設，不是 stale state；唯一要避免的是在 `numOfStrings` 開頭多呼叫一次 `build_failure(word)`（死碼，會被覆蓋）。
- **殺雞牛刀**：這題用 `word.find` 即可；選 KMP 純為練習。

## Follow-ups
真正的延伸是「**一個大字串、很多小字串**」要更快時怎麼辦——也就是本題把 L 放大、N 放大的情形。純 KMP 是「對每個小字串各跑一次」O(L·(N+M))，redundant 在於大字串被掃了 L 遍。兩條優化方向（都把大字串實質上只掃一次）：
- **預處理所有小字串** → **Aho-Corasick**：把所有小字串建成一個帶 failure link 的 trie，大字串只跑一遍 → O(ΣM + N)
- **預處理大字串** → **Suffix Automaton**：對大字串建一次（O(N)），每個小字串查詢 O(M) → O(N + ΣM)

兩者都是 linear-in-input、理論最佳；代價是它們比 KMP 冷門、實作較重。本題 constraints 用不到，但這是 multi-pattern matching 的標準答案。

## Related Problems
- [28] Find the Index of the First Occurrence in a String — 單一小字串的 KMP 原型題（strStr）
- [459] Repeated Substring Pattern — 直接用 failure function 最後一格的性質判斷週期
- [214] Shortest Palindrome — 對 `s + '#' + reverse(s)` 建 failure 取最長迴文前綴
