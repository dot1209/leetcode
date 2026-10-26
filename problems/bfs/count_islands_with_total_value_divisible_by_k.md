# [3619] Count Islands With Total Value Divisible by K
**Pattern:** [BFS → Graph Traversal](../../patterns/bfs/graph-traversal.md)
**Complexity:** Time O(mn), Space O(mn)
**Link:** https://leetcode.com/problems/count-islands-with-total-value-divisible-by-k/

## Trigger Signals
- 「skip 0 nodes → find connected component → BFS → add divisible check」。
- 正數格子代表陸地，上下左右相連形成一座島；每座島要先累加總值，再檢查是否能被 k 整除。
- 不求最短路，不需要分層；一次 BFS 完整處理一個 component。

## Core Insight
外層找未拜訪的非零格子，啟動 BFS 走完整座島；出 queue 時累加值，最後用 `sum % k == 0` 決定是否計入答案。

「要操作的節點是出 queue 的」這個習慣可以保留，但要區分標記與處理：入 queue 前標記 visited，避免重複加入；出 queue 時處理節點。queue 中的每個格子都必須是陸地，而且已經標記 visited，起點與鄰居都遵守這個條件。

## Why It's Correct
BFS 只走上下左右相連的非零格子，因此不會跨越水域，也會找到起點所屬島嶼的所有格子。入隊前標記讓每格只入隊一次，所以總和恰好包含這座島的每個值一次。

走完後，整座島都已標記，外層不會再次計算它。每座島恰好檢查一次，且只在總值可被 k 整除時增加答案。

## Complexity Analysis
外層掃描 mn 格；雖然雙迴圈裡呼叫 BFS，visit 會確保每個陸地格子最多入隊、出隊各一次，每次只檢查四個方向。所有 BFS 合計 O(mn)，加上外層掃描仍為 O(mn)，不是 O((mn)²)。讀取輸入最壞就需要 Ω(mn) 時間。

visit 陣列需要 O(mn)，queue 最壞也需要 O(mn)，因此額外空間為 O(mn)。

## Solution Code
使用者 AC 版本，原樣保留。

```cpp
class Solution {
public:
    int countIslands(vector<vector<int>>& grid, int k) {
        int m = grid.size();
        int n = grid[0].size();
        vector<vector<int>> visit(m, vector<int>(n, 0));
        int res = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 0) {
                    continue;
                }
                if (visit[i][j]) {
                    continue;
                }
                if (bfs(grid, i, j, k, visit)) {
                    res++;
                }
            }
        }
        return res;
    }
private:
    int dirs[5] = {-1, 0, 1, 0, -1};
    bool bfs(const vector<vector<int>>& grid, int i, int j, int k,
             vector<vector<int>>& visit) {
        long long sum = 0;
        int m = grid.size();
        int n = grid[0].size();
        visit[i][j] = 1;
        queue<pair<int, int>> q;
        q.push({i, j});
        while (q.size()) {
            auto [x, y] = q.front();
            q.pop();
            sum += grid[x][y];
            for (int d = 0; d < 4; d++) {
                int nx = x + dirs[d];
                int ny = y + dirs[d+1];
                if (nx < 0 || nx >= m || ny < 0 || ny >= n) {
                    continue;
                }
                if (grid[nx][ny] == 0) {
                    continue;
                }
                if (visit[nx][ny]) {
                    continue;
                }
                visit[nx][ny] = 1;
                q.push({nx, ny});
            }
        }
        return sum % k == 0;
    }
};

/*
    0. skip 0 nodes
    1. find conneceted component -> BFS
    2. add divisible check
*/
```

## Alternatives / Optimization
### 允許修改 grid：入 queue 時累加並清成 0
「如果可以改 grid 的話，那就是把它改成 0。」用 0 同時表示水域與已拜訪格子，就能省掉 visit。但清成 0 會抹掉原值，因此要採用「進 queue 的時候，累加值並且清成 0」，順序如下：

```cpp
sum += grid[nx][ny];
grid[nx][ny] = 0;
q.push({nx, ny});
```

起點也要先累加、清成 0 再入隊，並移除出 queue 時的累加。這省掉一份 O(mn) 陣列，但 queue 最壞仍為 O(mn)，整體空間階數不變。

使用 visit 的原解法保留輸入，也讓格子數值與拜訪狀態分開，適合維持「入隊標記、出隊處理」的習慣。面試可以先寫這版，再說明原地標記的取捨。

## Pitfalls
- 外層跳過 0，不代表 BFS 也會跳過 0。原本鄰居只檢查邊界與 visit，會走進水域，甚至把不同島嶼接在一起。
- 用 `grid = {{1, 0, 2}}`、`k = 3` 手動追蹤：應有兩座島，合格數為 0；若穿過 0，會錯誤合成總和為 3 的一座島。
- `bool bfs` 要回傳 `sum % k == 0`。原本的 `return sum % k;` 會讓餘數為 0 轉成 false，判斷恰好相反。
- visited 要在入隊前標記，包含起點；若出隊才標記，同一格可能先被不同鄰居重複加入。
- 總值可能達到 10¹¹，超過 int 範圍，使用 `long long`。題目保證矩陣非空且 k 為正，因此可讀取 `grid[0]` 並取餘數。
- 全為 0 時答案為 0；單一陸地檢查它本身的值；k 為 1 時每座島都合格。

## Side Notes
### 註解與實作不一致：檢查每個 queue 入口
「我真的很常實作跟自己的註解不一樣，又發現不到錯誤。」把「skip 0 nodes」改寫成可逐行核對的 invariant：queue 裡的每個格子都必須是陸地，而且已經標記 visited。

接著檢查每個 `q.push()`，包含起點，確認條件是否成立。用最小反例手動追 queue，例如兩塊陸地中間隔一個 0，比單純重讀註解更容易發現漏判斷。

### vector 初始化合法，真正錯在函式提早結束
`vector<vector<int>> visit(m, vector<int>(n, 0));` 本身合法。最初寫成 `int countIslands(vector<vector<int>>& grid, int k) {}`，已經把函式關閉，後續敘述落在 class scope 才導致編譯錯誤。將右大括號移到 `return res;` 後；另外 bfs 參數列的 `int k` 後也要有逗號。

## Related Problems
- [1254] [Number of Closed Islands](number_of_closed_islands.md) — 同樣走完整個 component，再判斷是否符合條件；該題的 0 代表陸地。
- [200] Number of Islands — 只數陸地 components，不需要額外計算島嶼總值。
- [695] Max Area of Island — 遍歷時累計面積，與本題累加格子數值使用相同結構。
