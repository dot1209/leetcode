# Prefix Sum

Prefix Sum 是把「任意連續區間」轉換成**兩個前綴狀態的差**，而不是反覆掃描整段區間。對半開區間 `[l,r)`，`sum(l,r) = prefix[r] - prefix[l]`。當問題要求差值為固定目標、相等、最長／最短長度時，通常可以把「尋找所有左端點」變成「查詢先前看過的 Prefix Sum」。

## When to Use
- 題目針對**連續** Subarray，且區間的加總或兩種元素數量差能轉換成 Prefix Sum 的差。
- **最長 Sum = target**：固定右端點 `r`，查詢 `prefix[r] - target` **最早**出現的位置，長度 `r-l` 最大。
- **符合 Sum = target 的區間個數**：需要記錄每種 Prefix Sum 的出現**次數**，而不是最早 Index。
- **負數使普通 Sliding Window 失效**、但仍要最短 Sum ≥ k：可考慮 Prefix Sum 搭配 Monotonic Deque，見 LC 862。
- 若值域固定且小，可以改用 Vector 作 Direct Address Table；Key 值域很大而實際 Key 數量少，優先考慮 Hash Map。

## Typical Complexity
**Time:** 建立／滾動 Prefix Sum 是 O(n)。搭配 `unordered_map` 查詢或插入，通常為 **expected O(n)**（每個 Key 操作平均 O(1)）；若用定長 Direct Address Table，則能達到 worst-case O(n)。

**Space:** 若只需要當前累積值，Prefix Sum 本身可用 O(1)；但為了儲存歷史 Index 或 Frequency，Hash Map／Vector 最壞仍需 O(n)。若保留完整 Prefix Array，另需 O(n)。

## Template Code
```cpp
// Longest subarray whose sum equals target (arbitrary integer values).
unordered_map<long long, int> firstIndex;
firstIndex.emplace(0LL, 0);
long long prefix = 0;
int best = 0;
for (int r = 1; r <= n; ++r) {
    prefix += nums[r - 1];
    auto it = firstIndex.find(prefix - target);
    if (it != firstIndex.end()) {
        best = max(best, r - it->second);
    }
    firstIndex.try_emplace(prefix, r);
}
```

## 如何選擇記錄的 Prefix 狀態

固定右界 `r` 後，要問的是「哪個過去的 `l` 最有用」：

- **最長長度：** 同一 Prefix Sum 只保留**最早 Index**。較晚、值相同的 Index 被支配，因為 `r-l` 一定更短。
- **數量：** 同一 Prefix Sum 需要累積**Frequency**，因為每次出現都可能對應不同合法起點。
- **最短長度且有不等式：** 需要考慮候選 Index 的順序與 Prefix Sum 的大小關係，可用 Monotonic Deque 淘汰被支配的候選（LC 862）。

## Pitfalls
- **半開區間 Off-by-one：** `prefix[r] - prefix[l]` 對應 `nums[l:r)`，長度是 `r-l`，不是 `r-l+1`。
- **初始化 `prefix[0]=0`／`firstIndex[0]=0`：** 否則漏掉從 `nums[0]` 開始的答案。
- **最早 Index 不可覆寫：** 用 `try_emplace` 或先檢查 `find`，不要用 `mp[prefix] = i` 一直覆寫。
- **避免 Overflow：** 任意整數的 Prefix Sum 用 `long long`；LC 525 只有 `±1` 且長度 ≤ 100000，`int` 足夠。
- **連續不等於 Sliding Window：** 若不能證明移動左端點安全，不能只憑「Subarray」就強行縮窗。

---

## Problems
