# [827] Making A Large Island
**Pattern:** [Union-Find](../../patterns/union-find.md)
**Complexity:** Time O(mn α(mn)), Space O(mn)
**Link:** https://leetcode.com/problems/making-a-large-island/

## Trigger Signals

- `grid` 的上下左右相連的 1 構成一座島，也就是一個 Connected Component。
- 可以把**最多一個** 0 改成 1，求可能形成的最大島嶼面積。
- 一格 0 最多接觸四個方向，但這四個方向可能指向**同一座島**。

## Core Insight

先把所有相鄰的 1 以 Union-Find 合併，每個 Component 的 Root 維護正確 `size`。再逐一考慮把某格 0 變成 1：先蒐集四個相鄰陸地的**不同 Root**，將它們的 Component Size 相加，最後加上翻轉的這一格。

重點不是直接加四個相鄰格子的 Size，而是先用 `unordered_set<int> roots` 消除重複 Component。這樣可以避免同一座島從兩個方向圍住水格時，被重複計算。

## Why It's Correct

1. 第一輪將所有相鄰陸地 Union，因此原始每座島的所有格子恰好屬於同一個 Component；沒有跨越 0 的連接。
2. 對任意待翻轉的 0，新島只會由這格本身和它四個方向相鄰的原始島組成。透過 Root 去重後，每座相鄰島恰好加入一次，`1 + sum(size[root])` 正好是翻轉該格得到的島嶼面積。
3. 第二輪枚舉每一格 0，因此所有合法的單格翻轉都被考慮。初始 `get_max_size()` 同時保留原本最大的島，包含完全沒有 0 的情況。
4. 取所有候選的最大值，得到題目要求的答案。

邊界例子：全部是 1 時，初始最大 Component Size 就是 `m*n`；全部是 0 時，所有 DSU 單點 `size` 預設為 1，任何翻轉最多得到面積 1；`1x1` Grid 也成立。

## Complexity Analysis

令 `N = m*n`。

- **Time：O(N α(N))**。初始化 DSU 為 O(N)；第一輪最多對每格檢查四個鄰居並進行 Union；第二輪每格水最多查四次 Root，且 Set 最多有四個元素；`get_max_size()` 額外掃描 O(N)。在 Path Compression + Union by Size 下，整體為 O(N α(N)) amortized。
- **Space：O(N)**。DSU 的 `parent`／`size` 各為 O(N)；每個水格的 `unordered_set` 最多四個 Root，為 O(1) 額外空間；不含輸入 Grid。

## Solution Code

### Union-Find（本人 AC Code，完整保留）

```cpp
class UF {
public:
    UF(int n) : size(n, 1), parent(n) { iota(parent.begin(), parent.end(), 0); }
    int find(int x) {
        if (x != parent[x]) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    void join(int x, int y) {
        int rx = find(x);
        int ry = find(y);
        if (rx == ry) {
            return;
        }
        if (size[rx] < size[ry]) {
            parent[rx] = ry;
            size[ry] += size[rx];
        } else {
            parent[ry] = rx;
            size[rx] += size[ry];
        }
    }
    int get_size(int x) { return size[find(x)]; }
    int get_max_size() { return *max_element(size.begin(), size.end()); }

private:
    vector<int> parent;
    vector<int> size;
};
class Solution {
public:
    int largestIsland(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        UF uf(m * n);
        int dirs[5] = {-1, 0, 1, 0, -1};
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    for (int k = 0; k < 4; k++) {
                        int nx = i + dirs[k];
                        int ny = j + dirs[k + 1];
                        if (nx < 0 || nx >= m || ny < 0 || ny >= n) {
                            continue;
                        }
                        if (grid[nx][ny] == 0) {
                            continue;
                        }
                        uf.join(i * n + j, nx * n + ny);
                    }
                }
            }
        }
        int res = uf.get_max_size();
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 0) {
                    unordered_set<int> roots;
                    for (int k = 0; k < 4; k++) {
                        int nx = i + dirs[k];
                        int ny = j + dirs[k + 1];
                        if (nx < 0 || nx >= m || ny < 0 || ny >= n) {
                            continue;
                        }
                        // check neighbors are different groups;
                        if (grid[nx][ny] == 1) {
                            roots.insert(uf.find(nx * n + ny));
                        }
                    }
                    int size = 0;
                    for (auto node : roots) {
                        size += uf.get_size(node);
                    }
                    res = max(res, size + 1);
                }
            }
        }
        return res;
    }
};
```

## Alternatives / Optimization

### 減少重複 Union

第一輪目前向四個方向檢查，會讓每對相鄰陸地最多觸發兩次 `join`。若只看「右、下」，仍能涵蓋全部相鄰邊，節省部分常數時間；**不改變**整體時間複雜度，也不必為此修改已 AC 的 Code。

### DFS／BFS Connected Component Labeling

另一種值得會的思路是先用 DFS 或 BFS 把每座島標成不同 ID，並記錄 `area[id]`；再枚舉每格 0，把四個不同的相鄰島 ID 對應面積相加。每格原始陸地只探索一次，Time O(mn)、Space O(mn)；是不用 DSU 的替代方法，且避免 O(α(N)) 因子。若原地改寫 Grid 儲存島 ID，還能節省額外標籤陣列，但會改動輸入。

### Interface 與 Code Length

目前 `get_size(int x) { return size[find(x)]; }` 對任意節點都安全。DSU 獨立封裝，加上兩次 Grid 掃描，雖然行數較多但職責清楚，不必為縮短程式碼而犧牲可讀性。

## Pitfalls

- **同一座島重複加總：** 四個方向可能有不同陸地格子，卻屬於同一個 Root；必須先對 Root 去重。
- **拿非 Root 的 Size：** `size[x]` 在 `x` 不是 Root 時可能是 Stale Data。應使用 `get_size(x)` 或 `size[find(x)]`。
- **翻轉的格子漏加：** 相鄰島面積加總後還要 `+1`；即使四周沒有島也應得到 1。
- **全陸地或全水：** 沒有 0 時仍需得到原島面積；沒有 1 時結果是 1。
- **座標映射：** `(i, j)` 對應 `i*n + j`，必須使用欄數 `n`，不是列數 `m`。

## Side Notes

### Stale Size 與 max_element

先前疑問是：`get_max_size()` 對整個 `size` Array 做 `max_element()`，但非 Root 的值可能已過期，為何答案仍正確？

因為每個 Component 的 Root 持有正確 Size，且被合併掉的舊 Root Size 一定不大於合併後的新 Root Size。即使沒有 Union by Size、任意選 Root，只要新 Root Size 是兩邊的總和，這個關係仍成立。因此全陣列的最大 Stale Value 不會超過某個真實 Root 的 Size，`max_element(size)` 正確。

### Union by Size 的真正作用

最初把「小的接到大的」當成 `max_element(size)` 正確的原因；修正後要區分：

- **Correctness：** Root Size 正確累加，不依賴哪一個 Root 當 Parent。
- **Performance：** Union by Size 控制樹深度。追蹤固定節點，只有它所在 Component 被掛到另一棵樹時 Depth 才增加；每發生一次，所屬 Component Size 至少翻倍。因此沒有 Path Compression 時也有 `Depth <= floor(log2 N)`，進而保證單次 `find` worst-case O(log N)。
- **With Path Compression：** 加上 Path Compression 後，操作的 amortized 複雜度降至 O(α(N))。

## Related Problems
- [200] Number of Islands — 同樣需要找 Grid 的 Connected Components，但只要計數，不需維護翻轉後的 Component Size。
- [684] Redundant Connection — 用 DSU 判斷一條邊是否連到已經同屬一個 Component 的兩個節點。
- [1319] Number of Operations to Make Network Connected — 同樣以 DSU 維護 Component 並判斷需要多少次合併。
