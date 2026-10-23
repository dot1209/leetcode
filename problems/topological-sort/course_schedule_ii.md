# [210] Course Schedule II
**Pattern:** [Topological Sort](../../patterns/topological-sort.md)
**Complexity:** Time O(V + E), Space O(V + E)
**Link:** https://leetcode.com/problems/course-schedule-ii/

## Trigger Signals
- 課程之間有先修 dependency，必須輸出一個符合所有先後約束的順序。
- 如果有 directed cycle，就無法完成所有課程。
- `[a, b]` 表示先完成 `b` 才能修 `a`。

## Core Insight
把 `[a, b]` 建成 `b -> a`，再執行 Kahn's Algorithm。先找 indegree = 0 的課程，完成後把它指向的課程 indegree 減一；新歸零的課程可以加入 Queue。

原本直覺先建 `a -> b`，手推後發現會得到相反的修課順序，因此改成 `b -> a`。

## Why It's Correct
Queue 中每個節點都沒有尚未完成的先修課程，因此取出時加入結果是安全的。處理完節點 `u`，解除所有 `u -> v` 的 dependency，只有 `v` 的 indegree 歸零後才允許加入 Queue。若最後輸出數量等於 V，所有 dependency 都被滿足；否則仍有節點無法解除 dependency，表示存在 directed cycle。

## Complexity Analysis
- **Time O(V + E)：** 建圖掃描 E 條邊，初始化 Queue 掃描 V 個節點。每個節點最多入隊／出隊一次，每條邊只會在其來源節點出隊時掃描一次。
- **Space O(V + E)：** adjacency list 儲存 V 個容器及 E 條邊；indegree、Queue、結果各為 O(V)。Hash-based adjacency list 的操作為 expected O(1)。

## Solution Code
### User's solution — verbatim
```cpp
class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        int n = numCourses;
        vector<unordered_set<int>> graph(n);
        vector<int> deg(n);
        for (const auto& pre: prerequisites) {
            // [a, b] -> (b -> a)
            graph[pre[1]].insert(pre[0]);
            deg[pre[0]]++;
        }
        queue<int> q;
        for (int i = 0; i < n; i++) {
            if (deg[i] == 0) {
                q.push(i);
            }
        }

        vector<int> res;
        while (q.size()) {
            int level = q.size();
            for (int i = 0; i < level; i++) {
                auto front = q.front();
                q.pop();
                res.push_back(front);
                for (auto neighbor: graph[front]) {
                    if (deg[neighbor] == 0) {
                        continue;
                    }
                    deg[neighbor] -= 1;
                    if (deg[neighbor] == 0) {
                        q.push(neighbor);
                    }
                }
            }
        }
        if (res.size() != n) {
            return {};
        }
        return res;
    }
};
```

## Alternatives / Optimization
### 移除不必要的 BFS level
這題只要求合法的 topological order，不需要計算學期數；可直接使用 `while (!q.empty())`。原始程式的分層不影響正確性，但增加巢狀迴圈。

### 簡化 indegree 更新
正常的 Kahn's Algorithm 可以直接使用 `if (--deg[neighbor] == 0) q.push(neighbor);`，不必額外檢查 `deg[neighbor] == 0`。前提是 adjacency list 與 indegree 的邊數一致。

### 使用 vector adjacency list
題目保證沒有重複 prerequisite，因此 `vector<vector<int>>` 就足夠；`unordered_set` 雖然也屬於 adjacency list，但有額外 hashing 成本。

### DFS Postorder
另一個獨立解法是 DFS 三色標記。對 `u -> v` 先完成 `v` 再將 `u` 加入 postorder，最後 reverse。遇到 visiting 節點即為 directed cycle；finished 節點可以直接跳過。Time／Space 同樣是 O(V + E)。

## Pitfalls
- 第一版曾使用 `deg[i] = graph[i].size()`，但這算的是 outdegree；修正為建圖時 `deg[pre[0]]++`。
- 最初漏掉 `res.size() != numCourses` 的檢查；即使 Queue 曾處理一些節點，獨立的 cycle 仍可能讓結果不完整。
- 曾把 `vector<vector<int>>` 誤認成 O(V²) adjacency matrix；它實際上是 O(V + E) adjacency list。
- 目前程式使用 `unordered_set`，若放寬題目限制而允許重複 prerequisite，應只在 insert 成功時增加 indegree，避免計數不一致。

## Side Notes
- BFS level 不是拓樸排序正確性的必要條件；它適合用來計算最少學期數。
- Directed cycle detection 使用 DFS 三色標記；Undirected Graph 可以使用 visited + parent，忽略走回父節點的邊。
- 對 `0 -> 2 <- 1`，`DFS(1)` 再遇到已完成的 `2`（state = 2）不代表 cycle。

## Follow-ups
### Minimum Semesters
如果每學期能同時修任意數量課程，Kahn's Algorithm 每一層 BFS 代表一個學期；每處理完一層就增加學期數。若最後完成節點數不足 V，回傳 -1。

## Related Problems
- [207] Course Schedule — 只需要判斷是否存在可行的修課安排。
- [1136] Parallel Courses — 求所有課程完成所需的最少學期數。
- [802] Find Eventual Safe States — 可用 DFS 狀態或反向圖拓樸排序處理。
