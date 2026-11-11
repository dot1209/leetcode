# Union-Find (Disjoint Set Union)

## When to Use
- 題目需要判斷節點是否位於同一個 Connected Component，或隨著邊的加入動態合併群組。
- 需要在合併後快速取得 Component Size，例如島嶼面積、最大連通塊、網路連線數量。
- 適合「加入連線」的情境；一般 DSU 不擅長直接刪除邊或拆開已合併的 Component。

## Typical Complexity
**Time:** 初始化 O(N)；Path Compression + Union by Size 下，每次 `find`／`join` 為 amortized O(α(N))，其中 α 為 Inverse Ackermann Function。只有 Union by Size 而沒有 Path Compression 時，單次 `find` worst-case O(log N)。
**Space:** O(N) — `parent` 與 `size` 各儲存 N 個元素。

## Template Code
```cpp
class UF {
public:
    UF(int n) : parent(n), size(n, 1) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void join(int x, int y) {
        int rx = find(x);
        int ry = find(y);
        if (rx == ry) return;

        if (size[rx] < size[ry]) swap(rx, ry);
        parent[ry] = rx;
        size[rx] += size[ry];
    }

    int get_size(int x) { return size[find(x)]; }

private:
    vector<int> parent;
    vector<int> size;
};
```

## Root Size 與 Stale Data 的 Invariant

每個 Component 都有且只有一個 Root；`find(x)` 會取得它。只有 Root 的 `size[root]` 保證是當前 Component 的正確大小。舊 Root 被接到其他 Root 後，其 `size` 不會同步清零或更新，成為 Stale Data。

- 任意節點 `x` 的 Component Size 必須透過 `size[find(x)]` 讀取，而不是 `size[x]`。
- 合併時先取 `rx = find(x)`、`ry = find(y)`，確認不同 Root，再把其中一個掛到另一個之下，並更新**新 Root** 的 Size。
- 即使不用 Union by Size、任意指定合併後的 Root，只要新 Root 的 Size 正確等於兩邊相加，Stale Size 就不可能大於該節點所屬 Component 的 Root Size。因此 `max_element(size)` 仍等於最大 Root Size；這個正確性**不依賴** Union by Size。
- 不過一般查詢單一 Component 的大小仍應找 Root；掃整個 `size` 取最大值需要額外 O(N)，並不會因為 DSU 有路徑壓縮而變成 O(1)。

## 為什麼 Union by Size 能限制 Tree Height

Union by Size 的目的不是維護 Binary Tree，也不是直接記錄 Height，而是限制 DSU Parent Tree 的高度。一個 Root 可以有任意數量的 Children。

追蹤固定節點 `x`，暫時不使用 Path Compression：

1. 只有當 `x` 所屬 Component 的 Root 被掛到另一個 Root 下方時，`x` 的 Depth 才增加 1；較大 Component 的節點 Depth 不變。
2. 此時 `x` 所屬 Component 的大小為 `k`，因為採 Union by Size，接收它的 Component 至少也有 `k` 個節點。
3. 合併後 `x` 所在 Component Size 至少成為 `2k`。因此 **Depth 每增加一次，Component Size 至少翻倍**，但 Component Size 增加不代表 Depth 必然增加。
4. 從 Size 1 起步，若 Depth 累積增加 `d` 次，所屬 Component 至少有 `2^d` 個節點；總節點數最多 N，所以 `2^d <= N`，得 `d <= floor(log2 N)`。

這個證明與樹是不是二元樹無關；有 Path Compression 時，`find` 還可能縮短路徑。

## Pitfalls
- 忘記先取 Root 就讀取／更新 `size`，會把 Stale Data 當成 Component Size。
- 已在同一個 Component 時仍執行 Size 相加，造成重複計數。
- 把 Union by Size 的平衡策略誤認為 Component Size 正確性的必要條件；正確性靠新 Root 累加兩個 Root Size。
- 誤以為「每次 Union 都讓每個節點 Depth +1」。只有被掛上去的那棵樹深度會增加。
- `join` 需要先完成 `find → 比較 Root → 連接 Parent → 更新 Size` 的完整轉移；缺少其中一環就可能破壞 Invariant。
- 把 amortized O(α(N)) 說成單次操作的嚴格 worst-case；只有 Union by Size 時，單次 `find` 的 worst-case 是 O(log N)。

---

## Problems

### [[827] Making A Large Island](../problems/union-find/making_a_large_island.md)
**Complexity:** Time O(mn α(mn)), Space O(mn)
- **Trigger:** Grid 中原本的島嶼是 Connected Components，可將一格水改成陸地並與最多四個鄰居 Component 合併。
- **Insight:** 先用 DSU 建立各島 Root／Size；枚舉每格水，將四個相鄰島嶼的 Root 去重後加總，加上翻轉的 1 格。
- **Pitfall:** 同一座島可能從多個方向接觸一格水，必須對 Root 去重，不能直接相加四個鄰居 Size。
