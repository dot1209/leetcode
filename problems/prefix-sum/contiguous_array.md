# [525] Contiguous Array
**Pattern:** [Prefix Sum](../../patterns/prefix-sum.md)
**Complexity:** Time O(n) expected, Space O(n)
**Link:** https://leetcode.com/problems/contiguous-array/

## Trigger Signals
- 要找最長的**連續** Subarray，且其中 `0`、`1` 數量相同。長度必為偶數，但只靠這個條件還不能直接決定最佳區間。
- 一開始會想 Sliding Window，但無法保證目前不合法時「縮掉左端」是安全的。例如 `[0,0,1]` 不合法，繼續加入 `1` 後 `[0,0,1,1]` 卻合法。
- 關鍵是將 `0` 改成 `-1`、`1` 維持 `+1`，把「兩種元素數量相等」轉成「Subarray Sum = 0」。

## Core Insight
把每個 `0` 看成 `-1`，每個 `1` 看成 `+1`，則 `count(1) - count(0) = 0` 等價於轉換後區間總和為 0。

採用半開區間 Prefix Sum：`sum[i:j) = prefix[j] - prefix[i]`。要讓 Sum = 0，就是尋找 `prefix[j] == prefix[i]`。

**對相同的右端點 `j`，最早的左端點 `i` 一定最好。** 如果另一個同樣 Prefix Sum 的 `i'` 較晚（`i' > i`），則 `j-i > j-i'`。因此只要從左往右掃，使用 `unordered_map<prefix, earliestIndex>` 保留每種 Prefix Sum **第一次**出現的位置；每個右端點都用 Hash Map 查到最長可能長度。

自己的最新版解法直接使用 Rolling Prefix Sum，不再需要 `vector<int> prefix`。使用 C++17 的 `try_emplace(prefix, i)`，在 Key 已存在時不覆寫最早 Index，且回傳 Iterator，省掉再次查表。

## Why It's Correct
對任意合法區間 `[l,r)`，轉換後的 Sum = 0，所以必有 `prefix[l] == prefix[r]`。掃描到右端點 `r` 時，Hash Map 已記錄該 Prefix Sum 的最早位置 `first[prefix[r]]`，因此一定找得到一個**不短於** `[l,r)` 的合法區間。

反過來，每次更新答案時，左右 Prefix Sum 相同，所對應的區間必有相同數量的 `0` 和 `1`，因此不會把不合法的長度算進答案。

同一個 Prefix Sum 只保留最早位置，不會漏掉最佳解，因為對固定 `r`，較晚的 `l'` 永遠有 `r-l' < r-l`，不可能形成更長的答案。

## Complexity Analysis
- **Time：expected O(n)**。單次掃描 n 個元素，Rolling Prefix Sum 每步 O(1)；`unordered_map::try_emplace` 平均 O(1)，因此期望時間 O(n)，不是 Hash Collision 最壞情況的保證。
- **Space：O(n)**。目前 Prefix Sum 是 O(1) 空間，Hash Map 最壞儲存 O(n) 個不同的 Prefix Sum。沒有必要保留整個 Prefix Array。
- 已達到漸近最佳時間量級：至少必須讀過全部輸入，Lower Bound 為 Ω(n)。

## Solution Code
### 寫法 1 — 自己最後更新的 AC Code（Rolling Prefix + Hash Map）

```cpp
class Solution {
public:
    int findMaxLength(vector<int>& nums) {
        int n = nums.size();
        int prefix = 0;
        int res = 0;
        // prefix, index
        unordered_map<int, int> mp;
        mp.insert({0, 0});
        for (int i = 1; i <= n; i++) {
            prefix += nums[i - 1] == 0 ? -1 : 1;
            auto [it, inserted] = mp.try_emplace(prefix, i);
            res = max(res, i - it->second);
        }
        return res;
    }
};
// [   0,1,1,1,1,1,0,0,0]
// [0,-1,0,1,2,3,4,3,2,1]
```

### 寫法 2 — 補充：Direct Address Table（不是自己的提交版本）

此題 Prefix Sum 只會落在 `[-n,n]`，可以用 `prefix+n` 映射到 Vector Index，省下 Hash Map 的雜湊與配置成本；時間仍為 O(n)，但改為 worst-case O(n)，空間 O(n)。

```cpp
class Solution {
public:
    int findMaxLength(vector<int>& nums) {
        int n = nums.size();
        vector<int> first(2 * n + 1, -1);
        first[n] = 0; // Prefix sum 0 occurs at prefix index 0.

        int prefix = 0, res = 0;
        for (int i = 1; i <= n; i++) {
            prefix += (nums[i - 1] == 0 ? -1 : 1);
            int pos = prefix + n;

            if (first[pos] == -1) {
                first[pos] = i;
            } else {
                res = max(res, i - first[pos]);
            }
        }
        return res;
    }
};
```

## Alternatives / Optimization
- **早期版本：** 先建完整 `prefix[n+1]`，再用 `mp.insert({prefix[i], i})` 和 `mp.at(prefix[i])` 計算。答案正確，但多用一個 O(n) Prefix Array，且同一輪有兩次 Hash Map 查詢。
- **最終版本：** Rolling Prefix + `try_emplace`，只保留目前 Prefix Sum，同一次查詢取得最早 Index。
- **Direct Address Table：** 適合 LC 525 的 `±1` 小值域情境；若改成任意整數的最長 Sum = 0 Subarray，Prefix Sum 值域可能非常大，改用 Hash Map 才能把空間限制在實際出現的 Key 數量 O(n)。一般整數加總應使用 `long long`，避免 Overflow。

## Pitfalls
- **「Contiguous」不代表可以直接套 Sliding Window。** 典型雙指標縮窗需要證明移動 `l` 後不會錯過未來最佳答案；本題 `[0,0,1]` 不合法，右擴成 `[0,0,1,1]` 又合法，直接縮 `l` 可能漏掉長度 4 的答案。
- **保留最早 Index，不能一直覆寫：** `try_emplace` 在 Key 已存在時保持原 Index；若用 `mp[prefix] = i` 就會丟掉較長答案的起點。
- **別漏初始 Prefix：** `mp.insert({0,0})` 代表空前綴，否則從陣列開頭就符合條件的案例（如 `[0,1]`）會漏掉。
- **Prefix Index 和 Array Index 不同：** `prefix[0]=0`，掃到 `nums[i-1]` 對應右界 `i`；半開區間長度為 `i-l`，不用再加 1。
- **區分最佳長度與一般平衡：** 長度必為偶數是必要非充分條件；仍需確認區間內 `0`、`1` 數量相同。

## Side Notes
- `unordered_map::try_emplace(key, value)` 回傳 `pair<iterator,bool>`。Key 已存在時不覆寫 Value，`it->second` 可直接取得最早 Index，而 `inserted` 可用來分辨是否為第一次出現。
- 面試時最值得問的是「**我丟掉的左端點，為什麼以後永遠不可能更好？**」只有能證明這一點，才能放心使用單向移動的 Variable Sliding Window。

## Follow-ups
- **若 `nums[i]` 改成任意整數，但仍尋找最長 Sum = 0 Subarray：** 前綴相等、保留最早 Index 的證明不變；資料結構應保留 Hash Map，並視數值範圍使用 `long long`。

## Related Problems
- [[862] Shortest Subarray with Sum at Least K](../sliding-window/shortest_subarray_with_sum_at_least_k.md) — 同樣由區間 Sum 轉為 Prefix Sum 差，但要找最短且含負數，使用 Monotonic Deque 管理候選。
- [[437] Path Sum III](../dfs/path_sum_iii.md) — 把樹上的 Downward Path Sum 化成 Prefix 差，Hash Map 記的是頻率，並須 Backtracking。
- [560] Subarray Sum Equals K — 同樣是 Prefix Sum，但要求區間**個數**，所以 Map Value 是 Frequency 而非最早 Index。
