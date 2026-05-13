# [286] Islands and Treasure (Walls and Gates)
**Pattern:** [BFS → Multi-source BFS](../../patterns/bfs/multi-source-bfs.md)
**Complexity:** Time O(m·n), Space O(m·n)
**Link:** https://neetcode.io/problems/islands-and-treasure/

## Trigger Signals
- 2D grid，每個 INF（room）都要問「離最近 0（treasure）多遠」
- 來源（treasure）稀疏、查詢點（room）密集 → 反向從來源擴散一次比每個 room 各跑一次 BFS 划算
- 邊權都是 1（上下左右一步），且答案具單調擴散性 → BFS 適用

## Core Insight
把**所有** treasure 一次塞進 queue 當 level 0，同步往四方擴散。每個 INF 第一次被碰到時的距離就是它離最近 treasure 的步數。直接把距離寫回 `grid[nx][ny]`，既是答案也是 visited 標記。

牆（-1）天然不滿足 `grid[nx][ny] == INF` 的擴散條件，會被同一個 prune 擋下，不用特判。

## Complexity Analysis
- **Time O(m·n)**：每個 cell 最多入隊一次（被「距離已寫入」的 check 擋下後續入隊），每次出隊檢查 4 個鄰居，總工作量正比於 cell 數。
- **Space O(m·n)**：queue 在最壞情況下（例如整張地圖都是 INF、treasure 在中心）某一層會同時容納 O(m·n) 個節點；不需要額外的 `visited` array 因為距離寫回 grid 兼當標記。

對比樸素做法：每個 room 各跑一次 BFS 是 O((m·n)²)，因為每次 BFS 自己就 O(m·n)、共 m·n 個 room。多源版把這些 BFS 合併成一次。

## Solution Code
```cpp
class Solution {
public:
    void islandsAndTreasure(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        constexpr int INF = 2147483647;
        constexpr int dirs[5] = {1, 0, -1, 0, 1};

        queue<pair<int, int>> q;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 0) q.push({i, j});
            }
        }

        while (!q.empty()) {
            auto [x, y] = q.front();
            q.pop();
            for (int k = 0; k < 4; k++) {
                int nx = x + dirs[k];
                int ny = y + dirs[k + 1];
                if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
                // blocks walls (-1) and filled cells
                if (grid[nx][ny] != INF) continue;
                grid[nx][ny] = grid[x][y] + 1;
                q.push({nx, ny});
            }
        }
    }
};
```

## Pitfalls
- **「為什麼不能從每個 room 各跑 BFS」**：可以、但複雜度差一個 m·n 倍。觀念上要建立「多查詢共享同一目標集合 → 反向廣播」的條件反射。
- **`grid[i][j] != -1 || grid[i][j] != 0` 永真**：兩個不等式用 `||` 接起來永遠為真。本題用反向 BFS 後根本不需要這個判斷，但若用樸素做法寫，要記得是 `&&`。
- **`std::queue` 的 front 不叫 top**：`top()` 是 `priority_queue`/`stack` 的方法，queue 用 `front()`。
- **`unordered_set<pair<int,int>>` 不能直接用**：`std::pair` 沒有預設 hash。本題用「距離寫回 grid」就完全不需要 set。
- **push 時就標距離**：寫成 pop 時才標的話，同一格可能被多個鄰居重複入隊，最壞退化為指數爆炸。
- **queue 裡不需要存距離**：早期版本用 `tuple<int,int,int>` 帶 `d`，但 `d == grid[x][y]` 是 redundant，改 `pair<int,int>` 從 grid 讀就好。

## 為什麼反向 BFS 是對的
正向（每個 room → 最近 treasure）和反向（所有 treasure → 每個 room）在無向 grid 上等價：A 到 B 的最短步數 = B 到 A 的最短步數。差別只在「**誰是主動方**」——反向把 m·n 個獨立查詢合併成一次廣播，是計算上的優化，不是語意上的改變。

辨認時機口訣：**「每個格子都問同一件事，先想答案來源能不能主動廣播」**。腐爛橘子、火災蔓延、Pacific Atlantic 全是同一個套路。

## Related Problems
- **[994] Rotting Oranges** — 同模板；要回傳「最後一層的時間」所以需分層計數
- **[1162] As Far from Land as Possible** — 同模板 + 取最大距離（最後一個被填到的就是離陸地最遠的水）
- **[417] Pacific Atlantic Water Flow** — 同反向思路，但擴散規則是「逆流」而非 +1 距離
- **[1293] Shortest Path in a Grid with Obstacles Elimination** — BFS 升級版：座標不足以代表狀態，要加 `(x, y, k_remaining)` 三維狀態

## Follow-up: 打 K 次牆會怎樣（LC 1293）
若把題目改成「最多可消除 K 個障礙，求 `(0,0)` 到 `(m-1,n-1)` 最短路徑」，普通 2D `visited` 會錯——因為「站在 (3,4) 剩 5 次額度」跟「站在 (3,4) 剩 0 次額度」是不同處境，前者未來能走的選項更多。

解法：把狀態從 `(x, y)` 擴成 `(x, y, used)`，`visited[x][y][used]` 三維標記。複雜度從 O(m·n) 變 O(m·n·K)。

更廣義的觀念：**當座標不足以描述「目前的我」，就把區別不同處境的東西塞進狀態**。同模板的兄弟題包括 LC 864（持有鑰匙 bitmask）、LC 847（已訪問節點 bitmask）。
