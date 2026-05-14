# DP — Unbounded Knapsack

## When to Use
每個物品**可以重複選任意次**（包含 0 次），對某個總量做 feasibility / counting / optimization。

典型問題形態：
- **Coin Change**：用無限量硬幣湊出 amount，最少幾枚 / 幾種方式
- **Rod Cutting**：把長度 L 的鋼條切成片段，每種長度有對應價值，求最大值
- **Word Break**：用字典裡的詞（每個可重複用）拼出某 string

關鍵特徵：「**選或不選**」變成「**選 0 / 1 / 2 / … 次**」，但不需要列舉次數 —— 巧妙的 transition 設計可以把它壓回 O(n × W)。

## Why 0/1 vs Unbounded 差在「內層方向」

兩者 2D 寫法的 transition 看似很像，差別在於「pick 物品 i 後，剩下要從哪些物品湊？」：

| 變體 | 選後剩餘可選 | 2D Transition |
|------|------------|--------------|
| 0/1 | 物品 `0..i-1`（不能再用 i） | `dp[i][w] = dp[i-1][w] \|\| dp[i-1][w-nums[i-1]]` |
| Unbounded | 物品 `0..i`（i 可重複） | `dp[i][w] = dp[i-1][w] \|\| dp[i][w-nums[i-1]]` |

注意右下角的下標：0/1 是 `dp[i-1][w-...]`（pick 完跳到上一行），unbounded 是 `dp[i][w-...]`（pick 完留在同一行 → i 可再選）。

**1D rolling 時這個差別變成「內層方向」**：

| 變體 | 1D 內層方向 | 原因 |
|------|-----------|------|
| 0/1 | `for w = W; w >= num; w--`（**倒著**） | 讀 `dp[w-num]` 要是「上一行的值」→ 還沒被當前 num 動過 |
| Unbounded | `for w = num; w <= W; w++`（**正向**） | 讀 `dp[w-num]` 要是「當前行已更新的值」→ 包含 num 重複使用的結果 |

這是兩者最常被搞混的點。**寫 1D 時方向錯就直接 WA**，2D 寫得對也別漏這條。

## Template Code

### 1D rolling — counting ways (LC 518 Coin Change II 風格)
```cpp
// 從 coins 中（可重複）湊出 amount 的方案數
vector<int> dp(amount + 1, 0);
dp[0] = 1;
for (int coin : coins) {
    for (int w = coin; w <= amount; w++) {   // 正向掃！
        dp[w] += dp[w - coin];
    }
}
return dp[amount];
```

### 1D rolling — min count (LC 322 Coin Change 風格)
```cpp
// 用 coins 湊 amount 的最少枚數，湊不出則 -1
vector<int> dp(amount + 1, amount + 1);      // sentinel: amount+1 = 不可達
dp[0] = 0;
for (int coin : coins) {
    for (int w = coin; w <= amount; w++) {
        dp[w] = min(dp[w], dp[w - coin] + 1);
    }
}
return dp[amount] > amount ? -1 : dp[amount];
```

### 1D rolling — feasibility
```cpp
vector<bool> dp(W + 1, false);
dp[0] = true;
for (int num : nums) {
    for (int w = num; w <= W; w++) {
        dp[w] = dp[w] || dp[w - num];
    }
}
return dp[W];
```

## Counting：外層內層順序很關鍵

Coin Change II 的 1D counting 中，外層**必須是 coins**、內層才是 `w`：

```cpp
for (int coin : coins)         // ← 外層
    for (int w = coin; ...)    // ← 內層
```

如果反過來（外層 `w`、內層 `coin`），會把「組合（combinations）」算成「排列（permutations）」，方案數會多算很多倍。

**直觀理解**：
- **外層 coin、內層 w**：對每個 coin 「加進考慮範圍」一次，dp 一直在「以這些 coins 為素材」的狀態下累加。每種組合**只在固定順序**下被算到一次。
- **外層 w、內層 coin**：每個 w 內都把所有 coin 試一遍，等於允許 `(1, 2)` 和 `(2, 1)` 是不同方式。算的是 permutations 不是 combinations。

題目問「**有幾種組合**」用前者；問「**有幾種排列**」（LC 377 Combination Sum IV 那種）用後者。

## Pitfalls
- **方向錯誤直接 WA**：1D unbounded 必須正向掃 w，0/1 必須倒著掃
- **Counting 的外層內層順序**：combinations vs permutations 差很大
- **`min` DP 的 sentinel 值**：用 `amount + 1`（一定不可達）當「未達」標記比 `INT_MAX` 安全 —— 後者做 `dp[w-coin] + 1` 會 overflow
- **包不包含「選 0 次」**：題目允許不選某物品時，base case `dp[0] = 1`（counting）或 `dp[0] = 0`（min count）就涵蓋了。不要再額外處理
- **`Word Break` 那種「順序敏感」題用 permutation 風格**：它要的是「拼接序列」，不是「用了哪些詞」

## Common Problems（尚未進筆記）
- [322] Coin Change — min count
- [518] Coin Change II — counting combinations
- [377] Combination Sum IV — counting permutations（外層內層要反過來）
- [139] Word Break — feasibility，可以看成 unbounded 的字串版

---

## Problems

_尚無已解題目。解到第一題 unbounded knapsack 後會新增。_
