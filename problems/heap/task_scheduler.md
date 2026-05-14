# [621] Task Scheduler
**Pattern:** [Heap / Priority Queue](../../patterns/heap.md)
**Complexity:** Time O(n log k), Space O(k)
**Link:** https://leetcode.com/problems/task-scheduler/

## Trigger Signals
- 「同一個任務之間要間隔至少 `n` 個 slot」→ scheduling with cooldown
- 「求最少需要多少時間完成」→ greedy 排程，且每輪都要挑當下「最該優先排」的任務
- 「最該優先排」= 當下頻率最高者，因為它最容易撞到冷卻限制 → 需要動態取極值 → priority queue

## Core Insight
把 timeline 切成一段段長度 `n+1` 的視窗。同一個任務在同一個視窗內最多出現一次（因為冷卻時間是 `n`），所以每一輪：

1. 從 heap pop 出最多 `n+1` 個**不同**任務各執行一次
2. 執行完後頻率 `-1`，**暫存**起來（snapshot）；不要立刻 push 回 heap，否則同輪可能再次取到同一個任務
3. 整輪結束後，把 snapshot 裡頻率仍 > 0 的 push 回 heap

「先 pop 整輪，最後再 push 回去」這個延遲機制是這題的核心技巧。

## Complexity Analysis
設 `n` 為 tasks 總長度，`k` 為 unique 任務數（題目限制 ≤ 26）。

- **Time O(n log k)**：每個任務最多被 push / pop O(log k) 一次，總 push / pop 次數為 O(n)。因為 k ≤ 26，實務上近似 O(n)
- **Space O(k)**：heap 與 hash map 各 O(k)；snapshot 每輪 O(k)

## Solution Code
```cpp
class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        // need to allocate n+1 slots
        // [a, b, c] [ ] [ ] ...

        // we count the frequency and pull highest tasks first
        // so that we can use the slots more efficiently

        // pop a task and check its frequency
        // if > 0, -1 and push back to the pq
        unordered_map<char, int> mp;
        for (const auto& t : tasks) {
            mp[t]++;
        }
        priority_queue<int> pq;
        for (auto [_, v] : mp) {
            pq.push(v);
        }

        int res = 0;
        while (pq.size()) {
            int slots = n + 1;
            vector<int> snapshot;
            for (int i = 0; i < slots; i++) {
                if (pq.size()) {
                    auto top = pq.top();
                    pq.pop();
                    snapshot.push_back(top - 1);
                }
            }
            for (auto f : snapshot) {
                if (f > 0) {
                    pq.push(f);
                }
            }
            // if the queue still has tasks, this batch must occupy a full (n+1)
            // window (idle slots count toward the cooldown); otherwise it's the
            // last batch and we only count the tasks actually executed — no
            // trailing idle needed
            res += pq.size() ? slots : snapshot.size();
        }
        return res;
    }
};
```

## Pitfalls
### 最後一輪不要硬補 idle
若 pop 完 pq 已空（沒人需要再排了），這輪就是收尾，只算 `snapshot.size()`。若無條件 `res += n+1` 會把不必要的 idle 也算進去，答案會偏大。

### snapshot 暫存是必須的
若 pop 出來 `-1` 後立刻 push 回 heap，下一個迴圈跌代可能又取到同一個任務 → 違反「同任務間隔 ≥ n」的限制。必須整輪結束再統一回填。

### `auto [_, v]` 的 `_` 不是 wildcard
C++17 structured binding 裡的 `_` 只是普通變數名，跟 Python 的 `_` 概念不同。連續寫兩次 `_` 會編譯錯，因為變數重複宣告。

### 數學公式解（O(n) 替代方案）
這題有經典 closed-form：
```
ans = max(tasks.size(), (maxFreq - 1) * (n + 1) + maxCount)
```
- `maxFreq`：出現最多次的任務的次數
- `maxCount`：有幾個任務同時擁有 `maxFreq`
頻率最高的任務決定骨架。
畫成 (maxFreq - 1) 個長度為 n+1 的區塊 + 最後一排放所有 maxCount 個並列最高頻的任務。
其他任務塞進空格，塞不下時 tasks.size() 才會超過骨架值
模擬法直觀適合理解，數學解適合面試／競賽追求 O(n)。

## Related Problems
- [253] Meeting Rooms II — min-heap 維護當前進行中會議的結束時間
- [1834] Single-Threaded CPU — heap 模擬 CPU 排程，類似「動態取下一個該處理的任務」
- [358] Rearrange String k Distance Apart — 結構幾乎一樣，把字母當任務、`k-1` 當冷卻時間
- [347] Top K Frequent Elements — 用 heap 維護 top-k，限制 heap 大小到 k 把 time 壓到 O(n log k)
