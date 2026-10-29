# [3882] Minimum XOR Path in a Grid
**Pattern:** [DP → Grid State Reachability](../../patterns/dp/grid-state-reachability.md)
**Complexity:** Time O(m·n·X)；原版 Space O(m·n·X)，rolling 版 Space O(n·X)，`X = 1024`
**Link:** https://leetcode.com/problems/minimum-xor-path-in-a-grid/

## Trigger Signals
- 只能向右或向下，格子有固定的填表順序。
- `a < b` 不保證 `a ^ z < b ^ z`，所以到同一格時不能只保留最小 XOR。
- `grid[i][j] <= 1023`，每條路徑的 XOR 也在 `0..1023`。

## Core Insight
你先想到 Dijkstra 的 relax，接著發現 XOR 不保留大小順序；於是改用 `dp[i][j][x]` 記錄到每格時 cost `x` 是否可能出現，讓後面的格子判斷。例如 `1 < 2`，但 `1 ^ 3 = 2 > 1 = 2 ^ 3`。只走完所有格子也無法補救單一 `d[v]`：到同格時較大的前綴值若先被丟掉，後面的 relax 就再也看不到那條路徑。

三維 AC code 用 1-indexed DP：`dp[i][j]` 對應 `grid[i-1][j-1]`，第 0 列及第 0 欄是全 `false` 的虛擬邊界。起點在 `dp[1][1][grid[0][0]]`，不是 `dp[0][0]`。從上或左的可達 `x` 轉移到 `x ^ grid[i-1][j-1]`，最後從 `dp[m][n][0]` 往上掃第一個 `true`。只有一格時，cost 就是該格的值。

Rolling 的核心依賴是 `dp[i-1][j]`（上）和 `dp[i][j-1]`（左）。按列由上往下、每列由左往右更新時，兩列版用 `pre[j]` 存上方、`cur[j-1]` 存左方；一列版則在覆寫 `dp[j]` 前，它還是上方，而已更新的 `dp[j-1]` 是左方。

## Why It's Correct
起點只有一個可能的 XOR，即 `grid[0][0]`。其餘每格的合法路徑最後一步必來自上方或左方。若這兩格已記錄全部可達 XOR，轉移便恰好產生目前格子的全部可達 XOR。依填表順序歸納，終點表包含所有完整路徑的 XOR，從小到大掃描得到最小值。

## Complexity Analysis
- **Time O(m·n·X)：** 三版都對每個格子的 `X = 1024` 種 XOR 值檢查上、左兩個前驅。清空或複製一整列也在這個時間界限內。

| 版本 | 儲存內容 | Space |
|---|---|---|
| 三維原版 | 每格一份 XOR 可達表 | O(m·n·X) |
| 兩列 rolling | `pre`、`cur` 各 `n+1` 份 | O(n·X) |
| 一列 rolling | `dp` 的 `n+1` 份，另加單格的 `next` | O(n·X + X) = O(n·X) |

因此是三種**程式寫法**、兩種漸近空間複雜度；一列版比兩列版節省常數倍空間。

## Solution Code
### 版本一：三維 DP，你的 AC 版本
使用 1-indexed DP；依你確認修正了 `x` 的 typo。

```cpp
class Solution {
public:
    int minCost(vector<vector<int>>& grid) {
        // define dp[i][j][x] = possible cost from (0, 0) to (i, j) (bool)
        int m = grid.size();
        int n = grid[0].size();
        int x = 1023;
        vector<vector<vector<bool>>> dp(
            m+1, vector<vector<bool>>(n+1, vector<bool>(x+1, false)));

        dp[1][1][grid[0][0]] = true;
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                for (int x = 0; x <= 1023; x++) {
                    int val = x^grid[i-1][j-1];
                    if (dp[i-1][j][x] || dp[i][j-1][x]) {
                        dp[i][j][val] = true;
                    }
                }
            }
        }
        for (int x = 0; x <= 1023; x++) {
            if (dp[m][n][x]) {
                return x;
            }
        }
        // unreachable
        return -1;
    }
};
```

### 版本二：兩列 rolling，你的程式
`pre[j]` 是上一列同欄，`cur[j-1]` 是目前列左邊。每列先清空 `cur`，整列完成後複製到 `pre`。

```cpp
class Solution {
public:
    int minCost(vector<vector<int>>& grid) {
        // define dp[i][x] = possible cost from (0, 0) to (i, j) (bool)
        int m = grid.size();
        int n = grid[0].size();
        int x = 1023;

        vector<vector<bool>> pre(n + 1, vector<bool>(x + 1, false));
        vector<vector<bool>> cur(n + 1, vector<bool>(x + 1, false));
        for (int i = 1; i <= m; i++) {
            for (auto& state: cur) {
                fill(state.begin(), state.end(), false);
            }
            // Roll the row dimension: pre[j] is above, cur[j - 1] is left.
            for (int j = 1; j <= n; j++) {
                if (i == 1 && j == 1) {
                    cur[1][grid[0][0]] = true;
                    continue;
                }
                for (int x = 0; x <= 1023; x++) {
                    int val = x ^ grid[i - 1][j - 1];
                    if (pre[j][x] || cur[j - 1][x]) {
                        cur[j][val] = true;
                    }
                }
            }
            pre = cur;
        }
        for (int x = 0; x <= 1023; x++) {
            if (cur[n][x]) {
                return x;
            }
        }
        // unreachable
        return -1;
    }
};
```

### 版本三：一列 rolling，補充寫法
`dp[j]` 更新前是上方，`dp[j-1]` 已更新成左方；用單格的 `next` 接住新結果，避免同一輪讀到剛寫入的 XOR。

```cpp
class Solution {
public:
    int minCost(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        constexpr int X = 1024;

        vector<vector<bool>> dp(n + 1, vector<bool>(X, false));
        dp[1][grid[0][0]] = true;

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (i == 1 && j == 1) continue;

                vector<bool> next(X, false);
                for (int x = 0; x < X; x++) {
                    if (dp[j][x] || dp[j - 1][x]) {
                        next[x ^ grid[i - 1][j - 1]] = true;
                    }
                }
                dp[j].swap(next);
            }
        }

        for (int x = 0; x < X; x++) {
            if (dp[n][x]) return x;
        }
        return -1;
    }
};
```

## Alternatives / Optimization
### Rolling 的更新成本
兩列版的 `pre = cur` 會複製整列，但不改變 `O(m·n·X)` 時間界限。若改成交換兩列，下一輪仍須清空新的 `cur`。一列版每格要建立 `next`，整體時間界限也相同。

## Pitfalls
- 不能只做單一最小值的 relax。例：兩條前綴到同一格時分別是 `1`、`2`，雖然 `1 < 2`，後綴再 XOR `3` 卻得到 `1 ^ 3 = 2`、`2 ^ 3 = 1`；先丟掉 `2` 就會漏掉較小答案。即使走完所有格子，也無法重新產生已丟掉的前綴。
- 1-indexed DP 的座標要一致。例：`grid = [[1,2]]` 時，起點是 `dp[1][1][1]`，終點是 `dp[1][2][3]`；`dp[0][1]` 是虛擬邊界。原碼註解的 `(i,j)` 實際對應 `grid[i-1][j-1]`。
- 起點要有獨立 base case。例：`grid = [[7]]` 只有一格，答案就是 `7`。三維原碼先設 `dp[1][1][7]`，一般轉移讀到兩個全 `false` 的虛擬前驅，不會覆蓋它。
- 兩列版不能把起點設在 `pre` 再做一般轉移。例：`grid = [[1,2]]`，若先設 `pre[1][1] = true`，處理起點又算 `1 ^ 1 = 0`，錯誤產生 cost `0`；應在 `cur[1]` 設起點並跳過該格的一般轉移。
- 兩列版的陣列索引必須是欄 `j`：`pre[j]` 是上方、`cur[j-1]` 是左方，長度是 `n+1`。例：`grid = [[1,2]]` 處理第二格時，左方要讀 `cur[1]`，不是固定讀 `cur[i-1] = cur[0]`；每列開始也要清空 `cur`，否則 `grid = [[1],[2]]` 的第二列可能殘留上一列 cost `1`，與正確的 cost `3` 混在一起。
- 辨認壓縮維度時，看哪個座標不再存於陣列索引。例：`2×3` grid 的兩列版保留 `j=1..3` 的三份狀態，卻沒有為每個 `i` 保存一份表，因此壓掉的是列 `i`，不是欄 `j`。
- 一列版不能一邊掃描 `dp[j][x]` 一邊原地設 `dp[j][x ^ value]`。例：舊狀態只有 `x=0`、目前格子的值為 `1`，設出 `x=1` 後同一輪又讀到它，錯誤留下 `x=0`；正確的新集合只有 `{1}`，須先寫入 `next` 再覆蓋。

## Related Problems
- [3393] Count Paths With the Given XOR Value — 同樣追蹤格子與 XOR，但 state 存路徑數量。
- [[1293] Shortest Path in a Grid with Obstacles Elimination](../bfs/shortest_path_in_a_grid_with_obstacles_elimination.md) — 同格保留額外狀態；1293 用 BFS 求等權步數，本題用 DAG DP。
