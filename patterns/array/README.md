# Array

## When to Use
題目操作 1D / 2D 陣列。陣列題的核心特性：**random access O(1)** 且**位置本身有意義**（index 可以承載資訊）。

許多陣列題的 follow-up 會要求 **O(1) extra space**，這時候要利用陣列自帶的「可寫位置」當輔助資料結構，把外部的 hashmap / 旗標陣列收進 input 本身。

## Typical Complexity
**Time:** 多數 O(n) 或 O(m·n)（單純掃過）；複合操作如 sort + scan 是 O(n log n)
**Space:** Brute force 多半是 O(n)（hashmap / extra array），follow-up 常要求 O(1)

## General Template
最常用的幾個原語：

### 1. 兩個 index 同時走（two pointers / sliding window）
```cpp
int left = 0, right = 0;
while (right < n) {
    // expand right
    while (/* invariant broken */) {
        // shrink left
        left++;
    }
    right++;
}
```

### 2. In-place 改寫（compact / partition）
```cpp
int write = 0;
for (int read = 0; read < n; read++) {
    if (/* keep this */) {
        nums[write++] = nums[read];
    }
}
```

### 3. 用 index 承載資訊（marker / sentinel）
```cpp
// 用負號表示「值 i 已出現過」
nums[abs(nums[i]) - 1] = -abs(nums[abs(nums[i]) - 1]);
```

## Common Variations
- [In-place Marker](in-place-marker.md) — 用 array 自身位置當 flag 達成 O(1) extra space
- [In-place Transform](in-place-transform.md) — 把複雜矩陣變換拆成 transpose / reverse 等 primitive 的組合，每步都能 in-place swap
