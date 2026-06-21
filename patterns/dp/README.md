# Dynamic Programming

## When to Use
- 問題能拆成「**重疊**的子問題」並具有「**最佳子結構**」
- 對暴力遞迴會重複算同個子問題（典型訊號：純 recursion 會 TLE）
- 題目問「能不能 / 有幾種 / 最小 / 最大 / 最佳路徑」這類**值**而非具體列舉
- 與 backtracking 的分界：backtracking 列舉具體解、DP 算解的數量或最佳值

## Typical Complexity
**Time:** O(state × transition) — state 數乘上每個 state 的決策數
**Space:** O(state)；若 state 只依賴前一兩層，可 rolling 壓到 O(1 row) 甚至 O(1)

特殊類型：**pseudo-polynomial**（如 knapsack）對「值的大小 V」是 polynomial，對「input 編碼長度 log V」是 exponential。

## General Template

### 狀態定義（最重要）
先確定 `dp[i][j][...]` 的意義，越精確越好。常見的提問格式：
- 「考慮前 i 個元素，當前 state 是 j，**xxx 的值是什麼**」
- 「以 i 結尾的 substring，**xxx 的值是什麼**」

### 轉移
從子問題推上來：`dp[state] = f(dp[smaller_state_1], dp[smaller_state_2], ...)`

### Base case 與答案位置
- Base：state 為 0 / 空 / 邊界時的初始值
- 答案：最後從哪個 state 取出

### Bottom-up vs Top-down
- **Bottom-up**：double loop 直接填表。常數小、空間可壓縮、容易做 rolling
- **Top-down**：recursion + memo。直觀好寫，但 stack 深度與 cache miss 較吃

## Common Variations
- [0/1 Knapsack](knapsack-01.md) — 每個物品**選或不選**，求 feasibility / counting / max value 等
- [Unbounded Knapsack](knapsack-unbounded.md) — 每個物品**可重複選任意次**（Coin Change 系列）
- [String Partition](string-partition.md) — 把字串切成段，`dp[i]` 是前綴 `s[0..i)` 能否 / 有幾種 / 最少幾段達成條件
