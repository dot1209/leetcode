# [583] Delete Operation for Two Strings
**Pattern:** [DP → Two-Sequence](../../patterns/dp/two-sequence.md)
**Complexity:** Time O(m·n), Space O(m·n) → 可壓 O(min(m,n))
**Link:** https://leetcode.com/problems/delete-operation-for-two-strings/

## Trigger Signals
- 輸入**兩個**字串 `word1`、`word2`，每次只能刪一個字元，問「最少刪幾次讓兩字串相等」
- 兩序列對齊 + 求「最少操作數」→ 二維 DP，state 是一對前綴長度
- 本質是 **Edit Distance 的縮減版**：只有刪除，沒有替換 / 插入

## Core Insight
定義狀態：`dp[i][j]` = 讓 `word1` 前 `i` 個字元與 `word2` 前 `j` 個字元相等，最少要刪幾次。答案是 `dp[m][n]`。

轉移就看當前兩字元相不相等：
- **不相等**：當前這兩個字元至少有一個留不住，只能刪。兩條路取小：
  - 刪 `word1[i-1]` → `dp[i-1][j] + 1`
  - 刪 `word2[j-1]` → `dp[i][j-1] + 1`
  - `dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + 1`
- **相等**：當前字元可以直接配對留下，**不用花任何一次刪除** → `dp[i][j] = dp[i-1][j-1]`

**Base case**：
- `dp[0][j] = j`：`word1` 為空，要跟 `word2` 前 `j` 個相等，只能把那 `j` 個全刪 → `j` 次
- `dp[i][0] = i`：對稱，`word2` 為空 → 刪 `word1` 那 `i` 個

檢查直覺的小技巧:**哪一維減 1,就代表刪了那一邊的字元**——減 `i` 是刪 `word1`、減 `j` 是刪 `word2`。

## Complexity Analysis
- **Time O(m·n)**：填滿 `(m+1)×(n+1)` 的表，每格 O(1)
- **Space O(m·n) → O(min(m,n))**：每格只依賴上一列 `dp[i-1][*]` 與本列左邊 `dp[i][j-1]`，留一列即可（O(n)）；再把較短字串擺內層 → O(min(m,n))

旁註:答案也等於 `m + n - 2 · LCS(word1, word2)`——留得越多共同子序列、要刪的越少。所以這題跟 LCS 是同一題的兩種問法。

## Solution Code
```cpp
class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size(), n = word2.size();
        // dp[i][j] = min deletions to make word1[0..i) and word2[0..j) equal
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

        // base case: one side empty -> delete every char of the other side
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        for (int i = 0; i <= m; i++) dp[i][0] = i;

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1[i - 1] != word2[j - 1]) {
                    // delete word1[i-1] or delete word2[j-1], take the cheaper
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + 1;
                } else {
                    // chars match: pair them up for free, no deletion
                    dp[i][j] = dp[i - 1][j - 1];
                }
            }
        }
        return dp[m][n];
    }
};
```

## Pitfalls
- **相等分支不可漏**：若只寫 `if (!=)` 而沒有 `else`，相等時 `dp[i][j]` 會停在初始值 0，整張表錯掉(這是第一版踩到的 bug)。
- **「都刪」是多餘且容易寫錯成本**:直覺會想加第三條「同時刪兩個」`dp[i-1][j-1]`。但同時刪兩字元是**兩次**操作(`+2`),而 `dp[i-1][j] ≤ dp[i-1][j-1] + 1` 保證「刪左再刪右」永遠不比它差 → 這條 transition 多餘。若誤寫成 `dp[i-1][j-1] + 1` 會把答案算少(WA)。
- **半開區間 → 比較 `word1[i-1]` / `word2[j-1]`**：`dp[i]` 指前 `i` 個字元,實際比對 index `i-1`。

## Optimization

### Rolling array → O(min(m,n)) space
把較短字串擺內層(column),只留一列;對角值 `dp[i-1][j-1]` 在覆寫前用 `prev` 接住:
```cpp
int minDistance(string word1, string word2) {
    if (word1.size() < word2.size()) swap(word1, word2);  // keep shorter on inner dim
    int m = word1.size(), n = word2.size();               // n <= m
    vector<int> dp(n + 1);
    for (int j = 0; j <= n; j++) dp[j] = j;               // row 0
    for (int i = 1; i <= m; i++) {
        int prev = dp[0];   // dp[i-1][0], the diagonal for j=1
        dp[0] = i;          // dp[i][0]
        for (int j = 1; j <= n; j++) {
            int tmp = dp[j];                              // save dp[i-1][j] before overwrite
            if (word1[i - 1] == word2[j - 1]) dp[j] = prev;            // diagonal
            else dp[j] = min(dp[j], dp[j - 1]) + 1;       // up = dp[j], left = dp[j-1]
            prev = tmp;
        }
    }
    return dp[n];
}
```

## Related Problems
- [72] Edit Distance — 完整版（加上替換、插入），相等時同樣 `dp[i-1][j-1]`、不等時 `1 + min(三條)`
- [1143] Longest Common Subsequence — 這題等價於 `m + n - 2·LCS`
- [115] Distinct Subsequences — 同網格的 counting 版
- [712] Minimum ASCII Delete Sum — 把「刪除次數」換成「刪除字元的 ASCII 總和」
