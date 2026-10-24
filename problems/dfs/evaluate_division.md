# [399] Evaluate Division
**Pattern:** [DFS](../../patterns/dfs.md)
**Complexity:** Time O(E + Q(V + E)), Space O(V + E)
**Link:** https://leetcode.com/problems/evaluate-division/

## Trigger Signals
- 等式提供兩個變數之間的比值，查詢可能需要串接多個等式才能推導。
- 所謂可推導結果的 query，就是以 equations 建圖後，能從 query[0] 走到 query[1]。
- 等式有效、比值皆為正數且互不矛盾，因此找到任一條有效路徑即可。

## Core Insight
每個 a / b = w 都建立 a 到 b 的權重 w，以及 b 到 a 的權重 1 / w。查詢從起點出發做 DFS，初始值為 1，每走過一條邊就乘上邊的權重；走到終點回傳累積值，所有方向都走不到才回傳 -1.0。

visited 記錄這筆 query 已經拜訪的節點，避免反向邊與其他迴圈造成重複探索。下一層找到的 res 已是起點到終點的完整結果，上一層只需把它往上傳。

## Why It's Correct
搜尋的 invariant 是 cur_val = start / cur_node。起點的初始值為 1，符合 start / start = 1。若沿 cur_node / next = val 前進，新的累積值為：

```text
(start / cur_node) * (cur_node / next) = start / next
```

因此抵達 end_node 時，累積值就是 start / end_node。等式保證一致，所以任一有效路徑都能推導相同的比值。

DFS 只跳過已拜訪的節點，並在一個子搜尋失敗後繼續探索其他鄰居。若存在通往終點的路徑，就能找到；所有可達節點都探索完仍未找到，才回傳 -1.0。開始前先檢查兩端是否出現在圖中，因此未知變數的同點查詢也會正確回傳 -1.0。

## Complexity Analysis
令 V 為不同變數數量、E 為 equations 數量、Q 為 queries 數量。values 與 equations 一一對應，不需要再定義另一個變數表示 values 數量。假設字串長度視為常數，hash 操作為 expected O(1)。

| 階段 | 時間 | 額外空間 |
|---|---|---|
| 建立 adjacency list | O(E) | O(V + E) |
| 單筆 DFS 查詢 | O(V + E) | O(V) |
| 全部查詢 | O(Q(V + E)) | O(V) |
| 整體，不含輸出 | O(E + Q(V + E)) | O(V + E) |

- 每個等式產生兩條反向邊，2E 在 Big-O 中仍為 O(E)。
- 單次 DFS 中，每個節點最多展開一次，每條 adjacency entry 最多掃描一次。
- 查詢空間包含 visited 與遞迴 stack，兩者各為 O(V)；查詢逐次執行，不必乘上 Q。
- 輸出 res 另占 O(Q)，若包含輸出，總空間為 O(V + E + Q)。
- 每個變數至少出現在一個等式中，因此 V <= 2E；本題總時間也可以簡化為 O(QE)，但保留 V + E 更容易看出圖搜尋成本。

## Solution Code
### User's solution — verbatim
```cpp
class Solution {
public:
    vector<double> calcEquation(vector<vector<string>>& equations, vector<double>& values, vector<vector<string>>& queries) {
        // build graph
        int n = equations.size();
        Graph graph;
        for (int i = 0; i < n; i++) {
            string start_node = equations[i][0];
            string end_node = equations[i][1];
            graph[start_node][end_node] = values[i];
            graph[end_node][start_node] = 1 / values[i];
        }

        // cal val
        int q = queries.size();
        vector<double> res(q);
        for (int i = 0; i < q; i++) {
            string start_node = queries[i][0];
            string end_node = queries[i][1];
            unordered_set<string> visit;
            if (graph.count(start_node) == 0 || graph.count(end_node) == 0) {
                res[i] = -1;
            }
            else {
                res[i] = dfs(start_node, end_node, graph, 1.0, visit);
            }
        }
        return res;
    }
private:
    using Graph = unordered_map<string, unordered_map<string, double>>;
     double dfs(string cur_node, string end_node, Graph& graph, double cur_val, unordered_set<string>& visit) {
        if (cur_node == end_node) {
            return cur_val;
        }

        visit.insert(cur_node);

        for (auto& [next, val]: graph[cur_node]) {
            if (visit.count(next)) {
                continue;
            }
            double res = dfs(next, end_node, graph, cur_val*val, visit);
            if (res != -1.0) {
                return res;
            }
        }
        return -1.0;
    }
};
```

### Supplementary optimization — preprocess connected components
下方為補充的優化實作，上方使用者的 AC 程式碼維持原樣。preprocess 的工作是走完整個 component，把 component ID 與 root / node 寫入 info；它不負責回傳某筆 query 的答案，因此使用 void。info 同時作為全圖共用的 visited，查詢階段不再呼叫 DFS。

```cpp
class Solution {
private:
    using Graph = unordered_map<string, unordered_map<string, double>>;

    struct NodeInfo {
        int component;
        double ratio; // component root / this node
    };

    using InfoMap = unordered_map<string, NodeInfo>;

    void preprocess(const string& cur_node, int component, double cur_val,
                    const Graph& graph, InfoMap& info) {
        info.emplace(cur_node, NodeInfo{component, cur_val});

        for (const auto& [next, val] : graph.at(cur_node)) {
            if (info.count(next)) {
                continue;
            }
            preprocess(next, component, cur_val * val, graph, info);
        }
    }

public:
    vector<double> calcEquation(vector<vector<string>>& equations,
                                vector<double>& values,
                                vector<vector<string>>& queries) {
        Graph graph;
        for (size_t i = 0; i < equations.size(); ++i) {
            const string& start_node = equations[i][0];
            const string& end_node = equations[i][1];
            graph[start_node][end_node] = values[i];
            graph[end_node][start_node] = 1.0 / values[i];
        }

        // Preprocess every connected component once.
        InfoMap info;
        int component = 0;
        for (const auto& entry : graph) {
            const string& root = entry.first;
            if (info.count(root)) {
                continue;
            }
            preprocess(root, component, 1.0, graph, info);
            ++component;
        }

        vector<double> res;
        res.reserve(queries.size());

        for (const auto& query : queries) {
            auto start = info.find(query[0]);
            auto end = info.find(query[1]);

            if (start == info.end() || end == info.end() ||
                start->second.component != end->second.component) {
                res.push_back(-1.0);
                continue;
            }

            // (root / end) / (root / start) = start / end
            res.push_back(end->second.ratio / start->second.ratio);
        }
        return res;
    }
};
```

## Alternatives / Optimization
### 靜態圖先預處理比值
若同一份等式會被大量查詢，可以先對每個 connected component 做一次 DFS，為節點保存 component ID 與 ratio[u] = root / u。沿 u / v = w 前進時，設定 ratio[v] = ratio[u] * w。

之後查詢 a / b，只需檢查變數是否存在且屬於同一個 component；若成立，答案為 ratio[b] / ratio[a]：

```text
ratio[a] = root / a
ratio[b] = root / b

a / b = (root / b) / (root / a)
      = ratio[b] / ratio[a]
```

例如 a / b = 2、b / c = 3，若選 a 為 root，預處理結果為：

| 節點 | component | ratio，也就是 a / node |
|---|---|---|
| a | 0 | 1 |
| b | 0 | 2 |
| c | 0 | 6 |

因此 a / c = 6 / 1 = 6、b / a = 1 / 2 = 0.5。unordered_map 的遍歷順序不保證選 a 為 root，但同一個 component 內的 root 會在除法中消去，答案不受 root 選擇影響。不同 component 的 root 沒有可推導的共同尺度，因此必須先比較 component ID。

每筆查詢 expected O(1)，建圖與預處理 O(V + E)，總時間降為 O(V + E + Q)。保留 adjacency list 時，額外空間仍為 O(V + E)，不含輸出；若包含輸出則為 O(V + E + Q)。預處理完成後也可釋放圖，保留 O(V) 的 info 回答後續查詢，但整體 peak space 仍包含建圖時的 O(V + E)。

| 做法 | 前置處理 | 每筆查詢 | Q 筆查詢的總時間 |
|---|---|---|---|
| 使用者原始版本 | O(E) | O(V + E) | O(E + Q(V + E)) |
| 全圖預處理版本 | O(V + E) | O(1) | O(V + E + Q) |

一次預處理可以共用的前提是等式維持不變，且等式保證一致。若新增或修改等式，原本保存的 component 與 ratio 可能失效，需要重新預處理。

### 唯讀參數與字串複製
dfs 的 cur_node 與 end_node 可改成 const string&，避免每層複製字串。Graph& 可改成 const Graph&，搭配 graph.at(cur_node) 與 const auto&，明確表示搜尋不修改圖。這些是可讀性與常數成本的改善，不是原始程式的 correctness bug。

## Pitfalls
### 成功時回傳 res，而非 cur_val * val
最初版本收到下一層成功的 res 後，卻回傳 cur_val * val。後者只包含起點到 next 的比值，會遺失下一層繼續走到終點的結果。

例如 a / b = 2、b / c = 3，查詢 a / c：

| 目前這一層 | cur_val | next | val | 下一層回傳的 res | cur_val * val |
|---|---|---|---|---|---|
| a | 1 | b | 2 | 6 | 2 |
| b | 2 | c | 3 | 6 | 6 |

在 b 那層，下一個節點剛好就是終點，兩者碰巧相同；回到 a 時若重新回傳 1 * 2，就把完整答案 6 換成部分結果 2。累積值往下傳的設計，成功後應直接 return res。

### 一個鄰居失敗，不代表全部失敗
第一版在 for 迴圈內、一次子搜尋失敗後就 return -1.0。這會使目前節點提早停止，後面的鄰居完全不會被搜尋。

正確流程是：子搜尋成功才回傳 res；失敗則繼續下一個鄰居。迴圈外的 return -1.0 代表所有方向都找過。若目前不是終點且沒有可探索的鄰居，也會自然走到這個失敗回傳。

### 遇到迴圈，跳過該鄰居
一致的等式讓繞圈乘積為 1，但這只表示繞圈沒有增加資訊，不代表抵達查詢終點。不能因此回傳 1 或 cur_val。

例如已知 a / b = 2、x / y = 3，查詢 a / x。雖然能走 a 到 b 再回 a，仍然到不了 x，答案必須是 -1.0。同樣地，b、c、d 可以是不同節點，仍存在 b 到 c 到 d 再回 b 的一致迴圈。

同一筆 query 內，visited 可保留已拜訪節點，不必在遞迴回傳後移除；每筆新 query 則必須重新建立 visited。

### 未知變數要先檢查
如果先處理 cur_node == end_node，未知的 x / x 也會誤回傳 1。必須在呼叫 DFS 前確認兩端存在，才能區分已知的 a / a = 1 與未知的 x / x = -1。

## Side Notes
### 遞迴回傳後，上一層從原位置繼續執行
每一層有自己的 cur_node、cur_val、區域變數與迴圈進度；visit 則以 reference 共用。呼叫下一層時，目前這一層暫停，下一層回傳後才繼續。

某次 for 迴圈分支沒有 return，不會自動結束 DFS，而是往下執行或進入下一個鄰居。若非 void 函式整條路徑走到函式結尾卻沒有回傳值，才會造成 undefined behavior。

### -1.0 是可以直接比較的失敗標記
-1.0 可以被 double 精確表示，而且是程式直接指定的 sentinel；合法比值皆為正數，不會與它混淆。因此 res != -1.0 不需要 epsilon。失敗標記必須先檢查，不能當成有效比值參與後續累乘。

浮點數不是每個值都有誤差：1、-1、0.5 都能精確表示；十進位 0.1 轉成二進位會無限循環，有限位數的 double 才需要存近似值。比較一般浮點計算結果時，則應依誤差需求選擇比較方式。

### Hash-based adjacency list
Graph 使用 unordered_map<string, unordered_map<string, double>>，只儲存存在的邊，屬於 adjacency list；adjacency matrix 才會配置 O(V²) 空間。變數名稱應保留為 string，存在性可直接用 graph.count(name) 檢查。

1 / values[i] 也沒有整數除法問題，因為 values[i] 是 double，整數 1 會先轉成 double；寫成 1.0 / values[i] 只是更明確地表達型別。

## Related Problems
- [1971] Find if Path Exists in Graph — 相同的可達性搜尋，移除比值與權重後只需回傳是否連通。
- [133] Clone Graph — 以 visited 或 original-to-copy mapping 保證每個節點只展開一次。
- [721] Accounts Merge — 從共同關係建立 connected components，也可用 DFS 或 Union-Find 分組。
