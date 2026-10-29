# DP — Grid State Reachability（網格有限狀態可達性）

## When to Use
路徑只能向右或向下，且累積值的範圍有限；同一格可能需要保留多個累積值，不能只存一個最佳值。XOR 尤其如此：`a < b` 不保證 `a ^ z < b ^ z`。

## Core Technique: Preserve Every Relevant Value
`dp[i][j][x]` 記錄是否能以值 `x` 到達格子 `(i-1, j-1)`。從上方或左方的可達值 `x` 轉移至 `x ^ grid[i-1][j-1]`。相同格子、相同 XOR 的前綴路徑可以合併，因為後續轉移結果完全相同。

數值範圍決定額外 state 維度的成本。若每格都是 10-bit 值，所有路徑 XOR 仍在 `0..1023`，故 `X = 1024`。

## Rolling Dependencies
若依列從上往下、每列從左往右處理，目前格子只讀上方 `dp[i-1][j]` 和左方 `dp[i][j-1]`。兩列版的 `pre[j]` 是上方、`cur[j-1]` 是左方；一列版的 `dp[j]` 在覆寫前是上方，`dp[j-1]` 在覆寫後是左方。壓縮的是列 `i`，保留的索引是欄 `j`。

XOR 轉移須讀完來源集合，才能覆寫目前欄。直接在同一份 `dp[j]` 掃描並設新 XOR，可能把剛寫入的值再次當成來源。因此一列版仍要有單格的暫存集合，空間為 `O(n·X + X) = O(n·X)`；兩列版也是 `O(n·X)`，只是常數用量較大。

## Template Code
```cpp
// dp[i][j][x] means value x is reachable at grid[i - 1][j - 1].
vector<vector<vector<bool>>> dp(
    m + 1, vector<vector<bool>>(n + 1, vector<bool>(X, false)));
dp[1][1][grid[0][0]] = true;
for (int i = 1; i <= m; ++i) {
    for (int j = 1; j <= n; ++j) {
        if (i == 1 && j == 1) continue;
        for (int x = 0; x < X; ++x) {
            if (dp[i - 1][j][x] || dp[i][j - 1][x]) {
                dp[i][j][x ^ grid[i - 1][j - 1]] = true;
            }
        }
    }
}
```

## Pitfalls
- XOR 不保序，不能用到每格的一個最小 `d[v]` 取代全部可達值；例如 `1 < 2`，但 `1 ^ 3 = 2 > 1 = 2 ^ 3`。
- 1-indexed DP 的第 0 列與第 0 欄是全 `false` 的虛擬邊界，起點在 `dp[1][1]`。
- Rolling row 時要區分尚未覆寫的上方與已更新的左方狀態。
- 起點必須與虛擬邊界分清楚；若邊界全為 `false`，要另外設定起點，避免漏掉或重複 XOR 起點。
- 一列版不能直接原地改寫同一格的 XOR 可達集合；例如舊集合 `{0}` 遇到格子值 `1`，原地掃描會先設出 `1`、再從新設的 `1` 設回 `0`，須先產生新集合再覆蓋。

---

## Problems

### [[3882] Minimum XOR Path in a Grid](../../problems/dp/minimum_xor_path_in_a_grid.md)
**Complexity:** Time O(m·n·X), Space O(m·n·X) → rolling O(n·X)，`X = 1024`
- **Trigger:** 右下網格路徑，且 XOR 值域只有 1024 種。
- **Insight:** 每格保留所有可達 XOR，從上、左的可達值 XOR 當前格子。
- **Pitfall:** XOR 不保序；rolling 時上方與左方的讀取時機不同，原地改寫 XOR 集合會污染來源。
