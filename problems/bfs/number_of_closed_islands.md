# [1254] Number of Closed Islands
**Pattern:** [BFS → Graph Traversal](../../patterns/bfs/graph-traversal.md)
**Complexity:** Time O(mn), Space O(mn)（以下複雜度以補上起點標記後為準）
**Link:** https://leetcode.com/problems/number-of-closed-islands/

## Trigger Signals
- 先以「找 island」這個條件來想，其實就是在找上下左右相連的 `0` 所形成的 connected components。
- 加上「要被 `1` 包圍」的限制後，要判斷整個 component 有沒有碰到網格邊界。
- 不求最短路，也不需要分層；用 BFS 完整走訪一個 component，順便收集它是否封閉的資訊。

## Core Insight
「先找 connected components，再檢查是否被包圍。」這張圖只有 `0`、`1`，所以只要整個 `0` component 沒有碰到網格邊界，它就一定是 closed island。

外層找「未看過的 `0`」，一次 BFS 走完一個 component；在找連通的過程中，用 `bool` 記錄這次 BFS 的 `0` 有沒有碰到邊邊。即使碰到了，也必須走完整個 component，最後才決定是否計入答案。

讓 BFS 只處理「未看過的 `0`」：`1` 通通跳過，已拜訪的也跳過。原地把 `0` 改成 `1` 就能合併這兩個篩選條件；在入隊時標記，保證每格只入隊一次。queue 裡保存的是「原本為陸地、已 discover、等待處理的格子」；其目前的 grid 值已經是 `1`，不必在出隊時再檢查值。

## Why It's Correct
BFS 只沿上下左右相連的 `0` 擴展，所以從一個未拜訪的 `0` 出發，會走完它所屬的整個 component，不會走進其他島嶼。入隊時就標記，使每格只被 discover 一次；外層因此也只會啟動一次 BFS 來處理這個 component。

如果 component 有任何一格位於網格邊界，就有一側直接接到網格外，不可能完全被 `1` 包圍。如果整個 component 都沒碰到邊界，那麼緊鄰它、卻不屬於它的格子一定是 `1`：假如是 `0`，它就應該被 BFS 納入同一個 component。因此「不碰邊界」恰好等價於「被 `1` 包圍」。遠處仍可能有其他 `0`，不是所有沒走到的格子都一定是 `1`。

## Complexity Analysis
補上起點標記後，外層掃描 mn 格；每格最多入隊、出隊各一次，每次只檢查四個方向，總時間是 O(mn)。最差情況必須檢查整張圖，因為沒檢查的格子可能改變島嶼的數量或封閉性，所以時間下界也是 `Ω(mn)`。

原地修改 grid 省掉了額外的 O(mn) visit 陣列，但 queue 最差仍可能需要 O(mn) 空間。因此整體輔助空間仍為 O(mn)，減少的是實際配置，不是整體空間的 Big-O。

下方原始版本僅漏標起點：起點有鄰居時可能再次入隊一次；孤立起點則不會被改成 `1`。外層每個位置只掃一次，因此孤立起點不會在本次呼叫被重算，這個疏漏也不會改變答案或 O(mn) 的時間上界，但不符合「每格只入隊一次、整個 component 都已標記」的 invariant。

## Solution Code
### 寫法 1 — 使用者最後貼的版本（原樣保留，起點標記待補）

這版已在鄰居入隊時標記；起點漏標的修正另外列於 Pitfalls，沒有直接修改原始程式。

```cpp
class Solution {
public:
    int closedIsland(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();

        int res = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    continue;
                }
                if(bfs(grid, i, j)) {
                    res++;
                }
            }
        }
        return res;
    }
private:
    int dirs[5] = {-1, 0, 1, 0, -1};
    bool bfs(vector<vector<int>>& grid, int i, int j) {
        queue<pair<int, int>> q;
        q.push({i, j});
        int m = grid.size();
        int n = grid[0].size();
        bool res = true;
        while (q.size()) {
            auto [x, y] = q.front();
            if (x == 0 || x == m-1 || y == 0 || y == n-1) {
                res = false;
            }
            q.pop();
            for (int k = 0; k < 4; k++) {
                int nx = x + dirs[k];
                int ny = y + dirs[k+1];
                if (nx < 0 || nx >= m || ny < 0 || ny >= n) {
                    continue;
                }
                if (grid[nx][ny] == 1) {
                    continue;
                }
                grid[nx][ny] = 1;
                q.push({nx, ny});
            }
        }
        return res;
    }
};
```

### 寫法 2 — 補充替代：先排除與邊界相連的 component

這是補充的反向思考：從邊界的 `0` 做 flood fill，先淹掉所有不封閉的島；剩下的每個 `0` component 都必定封閉。時間與最差輔助空間同樣是 O(mn)，重點在「先排除無效集合，再計數」。

```cpp
class Solution {
public:
    int closedIsland(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        for (int i = 0; i < m; ++i) {
            flood(grid, i, 0);
            flood(grid, i, n - 1);
        }
        for (int j = 0; j < n; ++j) {
            flood(grid, 0, j);
            flood(grid, m - 1, j);
        }

        int count = 0;
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                if (grid[i][j] == 0) {
                    ++count;
                    flood(grid, i, j);
                }
            }
        }
        return count;
    }

private:
    void flood(vector<vector<int>>& grid, int i, int j) {
        if (grid[i][j] == 1) return;
        int m = grid.size();
        int n = grid[0].size();
        int dirs[5] = {-1, 0, 1, 0, -1};
        queue<pair<int, int>> q;
        grid[i][j] = 1;
        q.push({i, j});
        while (!q.empty()) {
            auto [x, y] = q.front();
            q.pop();
            for (int k = 0; k < 4; ++k) {
                int nx = x + dirs[k];
                int ny = y + dirs[k + 1];
                if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
                if (grid[nx][ny] == 1) continue;
                grid[nx][ny] = 1;
                q.push({nx, ny});
            }
        }
    }
};
```

## Alternatives / Optimization
### 從 visit 陣列改成原地標記
原本同時有 visit 和修改 grid，資訊重複。允許修改輸入時，可以直接把走過的 `0` 改成 `1`；如果必須保留輸入，才另外保留 visit。這裡的用語是 in-place，與 STL 的 `emplace` 不同。

### 從出隊標記改成入隊標記
先前出隊才標記的版本，會讓不同鄰居把同一個尚未出隊的 `0` 重複放入 queue，而且重複項目仍會繼續展開。這不只是多了一點固定開銷；重複項目可能沿路累積，不能直接套用「每格只處理一次，所以 O(mn)」的分析。入隊時立即標記，才能阻止後續路徑重複 discover。

## Pitfalls
- 最初只數 `0` 的 components，卻無條件 res++，會把不封閉的島也算進去。應讓 BFS 回傳整個 component 是否封閉。
- 最初鄰居沒有檢查是否為 `0`，會連水域也放進 queue。先檢查範圍，再跳過 `1` 和已拜訪的格子。
- 合法邊界是 `0`、`m - 1`、`n - 1`，不是 `m`、`n`。越界檢查已擋住 `x == m` 和 `y == n`，用它們判斷下邊界與右邊界永遠不會成功。
- 發現碰到邊界，只設 res = false，不能提前 return；必須把同一個 component 全部標記，避免外層再次啟動 BFS。
- 最後貼的版本仍漏了起點標記：在起點 `q.push({i, j});` 後補上 `grid[i][j] = 1;`。標記規則必須同時適用於起點和所有鄰居。
- 「queue 裡都是 `0`」指原本的陸地身分；原地標記後，其 grid 值已是 `1`，因此出隊時不能再用 grid[x][y] == 0 決定要不要處理。
- 若矩陣只有一排或一列，所有陸地都在邊界，答案必為 0；全為 `1` 時也應回傳 0。題目保證矩陣非空，因此可讀取 grid[0]。

## Side Notes
### 這次的測資與邊界錯誤
```text
[[1,1,1,1,1,1,1,0],
 [1,0,0,0,0,1,1,0],
 [1,0,1,0,1,1,1,0],
 [1,0,0,0,0,1,0,1],
 [1,1,1,1,1,1,1,0]]
```
正確答案是 2。右上角那三格會因碰到最上排而被排除；使用錯誤的 m、n 邊界時，被誤算的是右下角的（4，7），因為下邊界與右邊界都沒被辨識。

### 效能截圖不能代替複雜度分析
這次兩張 Accepted 截圖都顯示 13 ms；記憶體由 19.20 MB 降到 18.61 MB。這能記錄單次提交的結果，但不能由此斷定修改沒有作用。先確認每格只入隊一次，再看配置與常數開銷；最優時間仍是 O(mn)。

## Follow-ups
### 如果還有 2，但只能算被 1 包圍的島嶼呢？
「其實就是玩 closed 的條件。」找 island 的方式不變：BFS 仍然只走上下左右相連的 `0`。改變的是這個 component 要符合哪些條件，才能被算進答案。

若 `1`、`2` 都能當圍牆，其實就跟原題一樣，只要整個 component 不碰網格邊界即可。真正新增的限制是「只能被 `1` 包圍」：此時不能只看是否碰到邊界，還必須排除鄰接 `2` 的 component。

從每個陸地格探索四個方向時，依序處理：

- 鄰居超出網格：設 `closed = false`，跳過這個方向。
- 鄰居是 `2`：設 `closed = false`，但不走進 `2`。
- 鄰居是 `1`：它是合法圍牆，直接跳過。
- 鄰居是 `0`：若未拜訪，就標記後入隊；已拜訪則跳過。

`closed` 一旦變成 false 就不會恢復，但仍然要走完整個 component。所有 `0` 都處理完後，若既沒有越界、也沒有鄰接 `2`，外圍便只能是 `1`，所以這座島符合條件。時間仍是 O(mn)。

### 解法二也能用：修改先淹掉的島嶼條件
先排除不合格島嶼的解法同樣適用。原題先淹掉碰到邊界的 `0` component；只能被 `1` 包圍時，再加上所有鄰接 `2` 的 `0` component。

先從邊界的 `0` 啟動 flood fill，再掃描所有 `2`，從它上下左右仍為 `0` 的格子啟動 flood fill。每次只沿 `0` 擴展，把整個不合格的 component 改成 `1`；保留所有 `2`，讓後續仍能辨識不合法的鄰接物。最後數剩下的 `0` components 即可。

解法一是走完每座島再判斷是否符合條件；解法二是先移除所有不符合條件的島，再數剩下的。解法二適用的關鍵是能從局部的不合格訊號找到起點，並確定整座島都該排除；碰到邊界與鄰接 `2` 都符合。每格最多被淹掉一次，掃描 `2` 時每格只檢查四個方向，所以總時間仍為 O(mn)，最差輔助空間為 O(mn)。

### 用 visit 把格子種類與拜訪狀態分開
這個延伸題偏向使用獨立的 visit，因為可讀性更好：grid 只描述格子是什麼，`0` 是陸地、`1` 是合法圍牆、`2` 是不合法的鄰接物；visit 只描述搜尋進度。兩種資訊各自獨立，判斷 closed 或擴充條件時，不必再解讀被改寫的格子。

不過，獨立 visit 是可讀性的選擇，不是正確性的必要條件。先前討論中「不能把拜訪過的 `0` 改成 `1`」的說法過強，已修正：只要透過「有沒有越界、是否鄰接 `2`」判定 closed，原地標記不會改掉這兩種資訊，因此仍然可行。代價是 `1` 同時代表原本的圍牆與拜訪過的陸地，需要額外理解這層約定。

使用 visit 需多配置 O(mn) 空間；原地標記省掉這份陣列，但兩者算入 queue 後，最差輔助空間都仍是 O(mn)。

## Related Problems
- [200] Number of Islands — 只計算陸地的 connected components，不需要封閉性檢查。
- [1020] Number of Enclaves — 同樣排除與邊界相連的陸地，但最後計算格子數而非 component 數。
- [130] Surrounded Regions — 從邊界保留可達區域，再翻轉其餘區域，對應先排除不封閉集合的反向思考。
