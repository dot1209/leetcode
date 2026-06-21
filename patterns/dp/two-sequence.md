# DP — Two-Sequence (雙序列對齊)

## When to Use
兩個序列 `s`、`t`（字串或陣列）放在二維表上對齊，`dp[i][j]` 描述「`s` 前 `i` 個 vs `t` 前 `j` 個」的某個值——這是 LCS / Edit Distance / Distinct Subsequences 的共同骨架。

會走這條路，是因為兩序列的「對齊方式」是指數量級（每個位置都能 match 或 skip），暴力遞迴會對同一組 `(i, j)` 後綴一再重算；把 `(i, j)` 當 state 存表，就把指數壓成 O(s·t)。跟爬樓梯、LIS 那種只看單一序列的 1D DP 不同，這裡 state 是**兩個前綴長度的二維座標**，轉移恆定地在左上 `dp[i-1][j-1]`、上 `dp[i-1][j]`、左 `dp[i][j-1]` 這幾格之間取——認得這個「網格」就認得整個家族。

關鍵訊號：
- 輸入是**兩個**序列，問「最長共同 / 最少編輯 / 有幾種對應」
- 子問題能用一對前綴長度 `(i, j)` 唯一描述
- 決策永遠是「當前兩字元相等嗎」分兩岔：相等時帶 `dp[i-1][j-1]`，不等時退化成上 / 左

與其他 DP 變種的分界：
- 跟 **string-partition** 的差別：partition 是**單**字串切段（1D `dp[i]`）；two-sequence 是**兩**序列對齊（2D `dp[i][j]`）
- 跟 **knapsack** 的差別：knapsack 第二維是「湊到的總量 W」、值無位置；two-sequence 第二維是「另一個序列的前綴長度」、位置即一切

## 三個代表題的轉移對照
同一張網格，差別只在「相等 / 不等時各往哪幾格取、取 max/min/sum」：

| 題目 | `s[i-1]==t[j-1]` 時 | 不等時 | 答案語意 |
|---|---|---|---|
| **LCS** (1143) | `dp[i-1][j-1] + 1` | `max(dp[i-1][j], dp[i][j-1])` | 最長共同子序列長度 |
| **Edit Distance** (72) | `dp[i-1][j-1]` | `1 + min(替換 dp[i-1][j-1], 刪 dp[i-1][j], 增 dp[i][j-1])` | 最少編輯次數 |
| **Distinct Subseq** (115) | `dp[i-1][j-1] + dp[i-1][j]` | `dp[i-1][j]` | `t` 在 `s` 中出現幾次 |

## Template Code
```cpp
// dp[i][j]: relation between s[0..i) and t[0..j)
vector<vector<long>> dp(s.size() + 1, vector<long>(t.size() + 1, 0));

// base case: depends on the problem (see each entry)
// for distinct subsequences: dp[i][0] = 1 (empty t), dp[0][j>0] = 0

for (int i = 1; i <= (int)s.size(); i++) {
    for (int j = 1; j <= (int)t.size(); j++) {
        if (s[i - 1] == t[j - 1]) {
            dp[i][j] = /* diagonal-based transition */;
        } else {
            dp[i][j] = /* up / left transition */;
        }
    }
}
return dp[s.size()][t.size()];
```

### Rolling 壓縮空間
每個 `dp[i][j]` 只依賴第 `i` 與 `i-1` 兩列 → 可降到 **O(t)**（一列 + 一個暫存對角值）。對角值 `dp[i-1][j-1]` 在覆寫前先存起來，否則會被同列前一格蓋掉。

## Pitfalls
- **半開區間講清楚**：`dp[i]` 對應 `s[0..i)`（不含 i），所以比較的字元是 `s[i-1]` / `t[j-1]`，差一格是最常見錯誤
- **Base case 不是整列同值**：要分清「哪一維為 0」代表什麼。空 `t` 與空 `s` 的初值往往不同（見 115：`dp[i][0]=1` 但 `dp[0][j>0]=0`）
- **Counting 會 overflow**：方案數可達指數，用 `long long`（115 LeetCode 測資保證落在範圍內，但型別仍要給夠）
- **Rolling 時對角值要先暫存**：壓成一維後，`dp[j-1]` 在你寫 `dp[j]` 前還是「上一列的左上」，但寫完就被汙染，需用 `prev` 變數接住

---

## Problems

### [[115] Distinct Subsequences](../../problems/dp/distinct_subsequences.md)
**Complexity:** Time O(s·t), Space O(s·t) → 可壓 O(t)
- **Trigger:** 兩字串，問 `t` 作為 `s` 的 subsequence 出現幾次 → 雙序列 counting DP
- **Insight:** 相等時「用這個 `s[i-1]` 配對」(`dp[i-1][j-1]`) 與「不用、留給後面」(`dp[i-1][j]`) 兩條路相加；不等時只能不用
- **Pitfall:** Base 是 `dp[i][0]=1`（空 `t` 一種：全不選）、`dp[0][j>0]=0`（空 `s` 湊不出非空 `t`）；計數要開 `long`

### [[583] Delete Operation for Two Strings](../../problems/dp/delete_operation_two_strings.md)
**Complexity:** Time O(m·n), Space O(m·n) → 可壓 O(min(m,n))
- **Trigger:** 兩字串每次刪一字元、求最少刪幾次相等 → Edit Distance 的縮減版（只有刪除）
- **Insight:** 相等時直接配對不用刪 (`dp[i-1][j-1]`)；不等時刪左 / 刪右取小 (`min(dp[i-1][j], dp[i][j-1]) + 1`)。等價於 `m + n - 2·LCS`
- **Pitfall:** 相等分支不可漏（漏了停在 0）；別加「都刪」那條——成本是 +2、且被刪左/刪右支配，多餘
