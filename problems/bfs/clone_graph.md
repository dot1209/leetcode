# [133] Clone Graph
**Pattern:** [BFS → Graph Traversal](../../patterns/bfs/graph-traversal.md)
**Complexity:** Time O(V + E), Space O(V)
**Link:** https://leetcode.com/problems/clone-graph/

## Trigger Signals
- Connected undirected graph，需要把整張圖 deep copy。
- 每個 original node 都必須有唯一的 clone，且原圖的每條 neighbor 關係都要在新圖保留。
- Graph 可能有 cycle，所以不能每次看到 neighbor 都重新建立 node；需要 visited / mapping。

## Core Insight
用 `unordered_map<Node*, Node*>` 保存 `original -> clone`。這個 mapping 同時扮演 visited：第一次看到 node 時建立 clone，之後再碰到同一個 original node，就直接重用既有 clone。

BFS 從 source 開始。第一次 discover neighbor 時做 `create + enqueue`；不論 neighbor 是否第一次出現，都把 `mp[cur]` 連到 `mp[neighbor]`。Graph 保證 connected，因此從 source 跑一次 traversal 就能覆蓋所有節點。

## Why It's Correct
BFS 過程中維持 invariant：每個已 discover 的 original node 在 `mp` 中恰好有一個對應 clone。因為 neighbor 只有在不在 `mp` 時才建立，所以同一個 original node 不會產生多個 clone。

每次掃到 original edge `cur -> neighbor`，都把 `mp[neighbor]` 加入 `mp[cur]->neighbors`，因此每條 adjacency relation 都會被複製。Graph connected 保證 BFS 最後會 discover 所有 original nodes，所以得到的 new graph 與原圖結構相同，且所有 nodes 都是新建立的物件。

## Complexity Analysis
BFS 中每個 node 最多 enqueue 一次，每個 adjacency entry 掃一次，因此時間複雜度是 O(V + E)。Undirected graph 的每條 edge 會從兩端各看到一次，但常數 2 不影響 Big-O。

`unordered_map` 的 lookup / insert 平均為 O(1)，所以 expected time 是 O(V + E)。若改用 `map`，每次操作是 O(log V)，整體會變成 O((V + E) log V)。

Auxiliary space 是 O(V)：`unordered_map` 最多存 V 個 mappings，queue 最壞也可存 O(V) 個 nodes。這裡不把 output cloned graph 算進 auxiliary space。

## Solution Code
### 寫法 1 — BFS（主解）
```cpp
class Solution {
public:
    Node* cloneGraph(Node* node) {
        if (node == nullptr) {
            return nullptr;
        }
        queue<Node*> q;
        unordered_map<Node*, Node*> mp;
        Node* copy = new Node(node->val);
        mp[node] = copy;
        q.push(node);
        while (q.size()) {
            auto front = q.front();
            q.pop();
            for (auto neighbor: front->neighbors) {
                if (mp.count(neighbor) == 0) {
                    Node* copy = new Node(neighbor->val);
                    mp[neighbor] = copy;
                    q.push(neighbor);
                }
                mp[front]->neighbors.push_back(mp[neighbor]);
            }
        }
        return mp[node];
    }
};
```

這版保留 BFS 的直觀流程：從 source 出發，discover 新 neighbor 時 create + enqueue；mapping 同時就是 visited。

### 寫法 2 — DFS（定版）
```cpp
class Solution {
public:
    Node* cloneGraph(Node* node) {
        unordered_map<Node*, Node*> mp;
        return dfs(node, mp);
    }
private:
    // return copied node
    Node* dfs(Node* node, unordered_map<Node*, Node*>& mp) {
        if (node == nullptr) {
            return nullptr;
        }

        auto it = mp.find(node);
        if (it != mp.end()) {
            return it->second;
        }
        
        auto copy = new Node(node->val);
        mp.emplace(node, copy);
        
        for (auto neighbor: node->neighbors) {
            copy->neighbors.push_back(dfs(neighbor, mp));
        }
        return copy;
    }
};
```

DFS 的重點是先 `mp.emplace(node, copy)`，再 recurse neighbors。這樣 cycle 回到已建立的 node 時，`find` 會直接拿到既有 clone，不會無限遞迴。Time 同樣是 O(V + E)，auxiliary space 是 O(V)，其中包含 worst-case O(V) recursion stack。

## Alternatives / Optimization
### `unordered_map` vs `map`
這題不需要 key ordering。用 `unordered_map` 時 lookup / insert 平均 O(1)，整體 expected O(V + E)；若使用 `map`，每次操作 O(log V)，整體多一個 `log V` 因子。

### `find`、`contains`、`count`
只想知道 key 是否存在時，C++20 可用 `contains`。若存在時馬上要拿 value，`find` 可以在一次 lookup 後直接用 iterator 的 `second`，避免 `contains(key)` 再接 `mp[key]` 的 double lookup。

`operator[]` 在 key 不存在時會插入 default value；`emplace` 則只在 key 不存在時插入。DFS 定版用 `find` + `emplace`，語意更貼合「第一次看到才建立 clone」。

## Pitfalls
- BFS 第一次 discover 新 neighbor 時只 create clone、忘記 `q.push(neighbor)`：這會讓 BFS 只處理 source，後續節點永遠不會被展開。
- 不能每次看到 neighbor 都 `new Node`。Graph 有 cycle 或多條路徑可到同一節點，必須先查 mapping，否則同一個 original node 會被 clone 多次。
- DFS 必須在 recurse neighbors 之前先把 `node -> copy` 放進 map，否則 cycle 會造成無限遞迴。
- `mp[nullptr] = nullptr` 並非必要；直接用 `if (node == nullptr) return nullptr;` 當 explicit base case 可讀性更清楚。
- 若 complexity 宣稱 O(V + E)，container 必須是 expected O(1) lookup 的 `unordered_map`；使用 `map` 時不能忽略 `log V`。

## Side Notes
這題 BFS 不需要分 level，因為目標是 traversal，不是 shortest distance。Graph 保證 connected，所以從題目給的 source 做一次 BFS / DFS 即可遍歷整張圖。

面試收尾可用最小 non-trivial case，例如 `1 - 2 - 3` dry run。這次 BFS 的實作 slip 就能在這個 case 立刻看出來：如果 `2` 沒有 enqueue，就永遠不會處理 `2 -> 3`。

## Related Problems
- [138] Copy List with Random Pointer — 同樣需要 old node → copied node mapping，避免同一個節點被複製多次。
- [200] Number of Islands — 同樣是 traversal + visited，但資料結構改成 grid。
- [323] Number of Connected Components in an Undirected Graph — graph 不保證 connected 時，要從每個尚未訪問的 node 啟動 traversal。
