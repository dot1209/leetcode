# DP — String Partition

## When to Use
要把一個字串 `s` **切成若干段**，每段需滿足某種條件，問「能不能切 / 有幾種切法 / 最少幾段」。

關鍵特徵：
- 子問題能用「**前綴長度**」唯一描述 → `dp[i]` = 「前 `i` 個字元 `s[0..i)` 是否能達成目標 / 達成目標的某個值」
- 切點 `j` 是決策變數：枚舉 `0 ≤ j < i`，要求 `dp[j]` 成立且 `s[j..i)` 滿足條件
- 不關心切完後段落的順序（因為段落本來就由位置決定），只關心**位置**與**條件**

跟其他 DP 變種的分界：
- 跟 **knapsack** 的差別：knapsack 只在意「總量」是否湊得到，不在意元素在哪個位置；string partition **位置很重要**，`s[j..i)` 必須在那個 specific range 上對得起來
- 跟 **LIS / 一般 1D linear DP** 的差別：linear DP 通常只看 `dp[i-1]` 或固定幾個前一個 state；string partition 要枚舉**所有切點 `j`**，所以多一層 O(n)

## Template Code

### Feasibility（能不能切）
```cpp
// dp[i] = can s[0..i) be partitioned to satisfy the condition
int n = s.size();
vector<bool> dp(n + 1, false);
dp[0] = true;                                // empty prefix always valid
for (int i = 1; i <= n; i++) {
    for (int j = 0; j < i; j++) {
        if (dp[j] && isValid(s, j, i)) {     // s[j..i) is a valid segment
            dp[i] = true;
            break;                           // feasibility: first hit is enough
        }
    }
}
return dp[n];
```

### Counting（幾種切法）
```cpp
vector<int> dp(n + 1, 0);
dp[0] = 1;
for (int i = 1; i <= n; i++) {
    for (int j = 0; j < i; j++) {
        if (isValid(s, j, i)) dp[i] += dp[j];
    }
}
return dp[n];
```

### Optimization（最少切幾刀 / 最少分幾段）
```cpp
vector<int> dp(n + 1, INT_MAX);
dp[0] = 0;
for (int i = 1; i <= n; i++) {
    for (int j = 0; j < i; j++) {
        if (dp[j] != INT_MAX && isValid(s, j, i)) {
            dp[i] = min(dp[i], dp[j] + 1);
        }
    }
}
return dp[n];
```

### 兩種枚舉方向
上面是「對每個 `i`，枚舉切點 `j`」。當「合法段落」由外部集合定義（例如 wordDict）時，可以改成「對每個 `i`，枚舉 dict 裡每個 word，看 `s[i - word.size()..i)` 是否 = word」：

```cpp
for (int i = 1; i <= n; i++) {
    for (auto& word : wordDict) {
        int len = word.size();
        if (i >= len && dp[i - len] &&
            s.compare(i - len, len, word) == 0) {
            dp[i] = true;
            break;
        }
    }
}
```

哪個快取決於 `|dict|` 與 `n` 的比例：dict 小用上面；n 小、dict 大用 hashset 版（內層 j-loop + `unordered_set.count(s.substr(j, i-j))`）。

## Pitfalls
- **狀態的「半開區間」要寫清楚**：`dp[i]` 講的是 `s[0..i)`（不含 i）還是 `s[0..i]`（含 i）？前者比較自然（dp[0] = 空字串），後者轉移時 off-by-one 容易出錯
- **Base `dp[0] = true`（feasibility）/ `dp[0] = 1`（counting）/ `dp[0] = 0`（min）**：空字串永遠是 valid base，但每種版本初始值不同
- **`s.substr` 是 O(L) allocation**：tight loop 裡換成 `s.compare(start, len, target)` 比較不會多配記憶體
- **不要把這題硬套 knapsack**：兩者狀態定義差很多。如果你想成「word 是物品、長度是 weight、capacity = n」，會丟掉「word 必須出現在 `s` 的特定位置」這個關鍵約束，思路會被帶歪
- **內層 break**：feasibility 版本一旦 `dp[i] = true` 就可以 break，counting / min 版本不能 break（要累加 / 取 min）

---

## Problems

### [[139] Word Break](../../problems/dp/word_break.md)
**Complexity:** Time O(n · m · L), Space O(n) — n = |s|, m = |wordDict|, L = avg word length
- **Trigger:** 給字串 `s` 與 word 集合，問能否完全切成 dict 裡的 word 序列 → 前綴 feasibility DP
- **Insight:** 可變步長的爬樓梯 —— 步長由 wordDict 決定，dp[i] 看是否存在一個 word 能落在尾端把問題接回 dp[i - len(word)]
- **Pitfall:** `s.compare(i - len, len, word)` 的起點是 `i - len`，不是 `i - 1`；feasibility 記得 early break
