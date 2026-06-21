# [139] Word Break
**Pattern:** [DP → String Partition](../../patterns/dp/string-partition.md)
**Complexity:** Time O(n · m · L), Space O(n) — n = |s|, m = |wordDict|, L = avg word length
**Link:** https://leetcode.com/problems/word-break/

## Trigger Signals
- 輸入一個字串 `s` 和一個 word 集合 `wordDict`，問能不能把 `s` 完全切成 dict 裡的 word 序列
- 「能不能切成段落，每段滿足某條件」→ 前綴 feasibility DP
- 暴力解（從每個位置試所有 word 並遞迴）會 TLE，因為**同一個後綴 `s[i:]` 會在不同遞迴路徑被重複計算** → memo 化 / DP

## Core Insight
**可變步長的爬樓梯**：爬樓梯題目直接告訴你步長是 1 或 2；這題的「步長」由 wordDict 決定，每個 word 都是一種可用的步長。
- 定義 `dp[i]` = 「前 `i` 個字元 `s[0..i)` 能否完全被 dict 切完」
- 轉移：枚舉每個 word，若 `dp[i - len(word)] == true` 且 `s[i - len(word)..i) == word`，則 `dp[i] = true`
- Base：`dp[0] = true`（空字串永遠能切）

## Complexity Analysis
- **Time O(n · m · L)**：
  - 外層 `i` 跑 n 次
  - 內層對每個 `i` 遍歷整個 wordDict（m 個 word）
  - 每次比對 `s.compare(start, len, word)` 是 O(L)
- **Space O(n)**：只需要一個長度 n+1 的 bool array

跟暴力遞迴的對比：純 recursion 對同一個後綴 `s[i:]` 會在不同切法路徑下被重複問「能不能切」，最壞指數爆炸；DP 把每個位置的答案存下來，每個 state 只算一次。

## Solution Code
```cpp
class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        // similar to climbing stairs but with variable step sizes
        // step sizes are determined by wordDict
        int n = s.size();
        // dp[i] is true iff
        // exists a j, dp[j] = true and s[j:i] in wordDict
        vector<bool> dp(n + 1, false);
        dp[0] = true;
        for (int i = 1; i <= n; i++) {
            for (auto& word : wordDict) {
                if (i >= word.size() && dp[i - word.size()] &&
                    // start, len, target — avoid substr allocation
                    s.compare(i - word.size(), word.size(), word) == 0) {
                    dp[i] = true;
                    break;  // feasibility: first hit is enough
                }
            }
        }
        return dp[n];
    }
};
```

## Pitfalls

### `substr` 的起點是 `i - len(word)`，不是 `i - 1`
`dp[i]` 對應的前綴是 `s[0..i)`，所以結尾那段 word 佔據 `s[i - len(word) .. i)`，起點當然是 `i - len(word)`。寫成 `s.substr(i - 1, ...)` 是常見的 off-by-one 錯誤（拿了從位置 `i-1` 開始的子字串，整個位移亂掉）。

### `substr` vs `compare`
`s.substr(start, len)` 每次都會 allocate 一個新的 string，DP tight loop 跑 n × m 次配置很浪費。改用 `s.compare(start, len, target)` 直接在原字串上比，不配記憶體。

### Feasibility 記得 `break`
一旦 `dp[i] = true`，後面繼續查其他 word 也沒意義（不能更 true）。`break` 出內層 loop 在 dict 大時是顯著加速。

### 不要硬套 knapsack
看起來像「每個 word 是物品、長度是 weight、s 的長度是 capacity」，但 knapsack 不關心物品出現在哪個位置；這題的 `s[j..i)` 必須在 `s` 的特定位置上對得起來。硬套會丟掉位置約束，思路被帶歪。

### `dp[i] = true` vs `dp[i] = dp[i - len]`
在「先用 if 確認 `dp[i - len] == true` 才進入 assign」的寫法下，兩者等價。建議用 `dp[i] = true` 因為意圖比較直接（reader 不用追前一個 state 是什麼）。

## Optimization

### Early break
已寫進上面 Solution Code 裡（內層 `break`）。

### 換成 j-loop + unordered_set（dict 大時更快）
```cpp
unordered_set<string> dict(wordDict.begin(), wordDict.end());
vector<bool> dp(n + 1, false);
dp[0] = true;
for (int i = 1; i <= n; i++) {
    for (int j = 0; j < i; j++) {
        if (dp[j] && dict.count(s.substr(j, i - j))) {
            dp[i] = true;
            break;
        }
    }
}
```
Time O(n² · L)。哪種快取決於 `m` 與 `n` 的比例：
- `m` 小、`n` 大 → 原版（outer i × inner wordDict）
- `m` 大、`n` 小 → 這版（outer i × inner j + hashset）

### Trie（進階）
把 wordDict 建成 Trie，從位置 `j` 沿 Trie 往下走 `s[j], s[j+1], ...`，遇到 word end 就標記 `dp[i] = true`。一次走訪能同時試所有以 `s[j]` 開頭的字，少很多重複比對。Code 複雜很多，面試一般 early break + hashset 就夠。

## Related Problems
- [140] Word Break II — 同樣狀態定義，但要列舉所有切法（feasibility → enumeration，DP + backtracking 結合）
- [70] Climbing Stairs — 固定步長 {1, 2} 版本的同類問題
- [91] Decode Ways — 也是 `dp[i]` = 前 i 個字元的切法數，固定步長 {1, 2}（但每步要檢查合法性）
- [132] Palindrome Partitioning II — string partition min-cut 變體
