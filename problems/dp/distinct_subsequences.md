# [115] Distinct Subsequences
**Pattern:** [DP → Two-Sequence](../../patterns/dp/two-sequence.md)
**Complexity:** Time O(s·t), Space O(s·t) → 可壓 O(t)
**Link:** https://leetcode.com/problems/distinct-subsequences/

## Trigger Signals
- 輸入**兩個**字串 `s`、`t`，問「`t` 在 `s` 裡作為 subsequence 出現**幾次**」
- 「有幾種方式」+ 兩序列對齊 → 二維 counting DP，state 是一對前綴長度
- 暴力解（對每個 `s` 字元決定選不選，遞迴比對 `t`）會對同一組 `(i, j)` 後綴重複計算 → 記憶化 / DP

## Core Insight
先定義狀態：`dp[i][j]` = 用 `s` 前 `i` 個字元組成 `t` 前 `j` 個字元的**方法數有幾種**。這樣答案就是 `dp[s.size()][t.size()]`。

接下來想轉移——只看「當前 `s[i-1]` 和 `t[j-1]` 相不相等」：
- **相等**：`s[i-1]` 有兩條獨立的路，相加
  - **拿來配對**：消化掉 `t` 的這一位 → 回到 `dp[i-1][j-1]`
  - **不拿、留給前面的 `s` 去配**：`t` 這位還沒被滿足 → `dp[i-1][j]`
  - `dp[i][j] = dp[i-1][j-1] + dp[i-1][j]`
- **不等**：`s[i-1]` 根本配不上 `t[j-1]`，只能不用它 → `dp[i][j] = dp[i-1][j]`

**Base case（邊界）**：
- `dp[i][0] = 1`：要組成**空的 `t`**？永遠 1 種——`s` 全部不選。整個第 0 行填 1。
- `dp[0][j>0] = 0`：用**空的 `s`** 組非空 `t`？永遠 0 種。

## Complexity Analysis
- **Time O(s·t)**：填滿一張 `(s+1) × (t+1)` 的表，每格 O(1) 轉移
- **Space O(s·t)**：整張二維表。但每個 `dp[i][j]` 只依賴上一列（`i-1`）→ 可滾動壓成 **O(t)**

跟暴力遞迴對比：純 recursion 對同一個 `(s 後綴, t 後綴)` 組合會在不同選擇路徑下被重複問，最壞指數爆炸；DP 把每個 `(i, j)` 只算一次。

## Solution Code
```cpp
class Solution {
public:
    int numDistinct(string s, string t) {
        // dp[i][j] = number of ways to use the first i chars of s
        // to form the first j chars of t
        vector<vector<unsigned long>> dp(
            s.size() + 1, vector<unsigned long>(t.size() + 1, 0));

        // base case: forming an empty t -> always 1 way (pick nothing)
        for (int i = 0; i <= (int)s.size(); i++) {
            dp[i][0] = 1;
        }
        // dp[0][j>0] stays 0: empty s cannot form a non-empty t

        for (int i = 1; i <= (int)s.size(); i++) {
            for (int j = 1; j <= (int)t.size(); j++) {
                if (s[i - 1] == t[j - 1]) {
                    // use s[i-1] to match (diagonal) OR skip it (up)
                    dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j];
                } else {
                    // s[i-1] can't match t[j-1]; must skip it
                    dp[i][j] = dp[i - 1][j];
                }
            }
        }
        return dp[s.size()][t.size()];
    }
};
```

## Pitfalls
- **Base 不是整列同值**：第 0 **行**（空 `t`）全填 1，第 0 **列**（空 `s`）保持 0。把握「哪一維為 0 代表空哪個字串」才不會初值寫反。
- **半開區間 → 比較 `s[i-1]` / `t[j-1]`**：`dp[i]` 指前 `i` 個字元 `s[0..i)`，所以實際比對的是 index `i-1`，差一格是經典 off-by-one。
- **Counting overflow**：方案數最壞指數級，用 `unsigned long` / `long long`（LeetCode 保證最終答案落在 32-bit，但中間累加要型別夠寬）。
- **「相等才多一條路」**：不等時**不能**加 `dp[i-1][j-1]`，只有 `dp[i-1][j]`。把不等也寫成相加是最常見的邏輯錯。

## Optimization

### Rolling array → O(t) space
每個 `dp[i][j]` 只看上一列。壓成一維時，從**右往左**更新 `j`，這樣 `dp[j-1]` 在被覆寫前還是「上一列的左上對角」：
```cpp
vector<unsigned long> dp(t.size() + 1, 0);
dp[0] = 1;  // empty t
for (int i = 1; i <= (int)s.size(); i++) {
    // iterate j from high to low so dp[j-1] is still the previous row's diagonal
    for (int j = t.size(); j >= 1; j--) {
        if (s[i - 1] == t[j - 1]) {
            dp[j] = dp[j] + dp[j - 1];  // dp[j]=up (this iter unchanged yet), dp[j-1]=diagonal
        }
        // else: dp[j] unchanged (== up), nothing to do
    }
    // dp[0] stays 1
}
return dp[t.size()];
```
往左掃是關鍵：若往右掃，`dp[j-1]` 會先被本列更新、變成「左」而非「左上」，對角值就丟了。

## Related Problems
- [1143] Longest Common Subsequence — 同網格，相等取 `dp[i-1][j-1]+1`、不等取 `max(上, 左)`
- [72] Edit Distance — 同網格，不等取 `1 + min(替換, 刪, 增)`
- [583] Delete Operation for Two Strings — LCS 的變形（刪到剩共同子序列）
- [97] Interleaving String — 雙序列 DP 但問「能否交錯組成第三字串」(feasibility)
