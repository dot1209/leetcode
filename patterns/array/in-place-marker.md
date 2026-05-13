# Array — In-place Marker

## When to Use
- 題目（或 follow-up）要求 **O(1) extra space**
- 需要記住「哪些 index / row / col / 值已經出現過或要處理」這種**布林狀態**
- 輸入陣列允許被修改（或最後會輸出，原始值不再需要）

把外部的 hashmap / visited array 收進 input 自身，代價是要找到一個「不會跟原始值衝突」的方式把旗標寫進去。

## Core Technique: Snapshot Before Mutation
In-place marker 的本質是「**input 的某些位置同時當原始資料與旗標**」。當這兩個身份衝突時（某位置既要當旗標又要保留原值），就需要 O(1) 個額外變數先**快照**原始值，後面再回填。

### 標準四步骨架
1. **Snapshot**：用 O(1) 變數記下即將被「身份重疊」的位置原本是什麼
2. **Mutate**：讓那些位置開始扮演旗標
3. **Use**：依旗標處理 interior
4. **Restore**：根據 snapshot 補完邊界

LC 73 是這套骨架最典型的例子：邊界 row 0 / col 0 被拿去當其他 row / col 的旗標，所以它們自己原本是否該被清零，要用兩個 bool 先記下。

## Template Code
```cpp
// 第一階段：snapshot 邊界
bool flag1 = /* 邊界原本狀態 */;
bool flag2 = /* 另一個邊界 */;

// 第二階段：用邊界做 marker
for (/* interior */) {
    if (/* condition */) {
        mark(boundary);
    }
}

// 第三階段：依 marker 處理 interior
for (/* interior */) {
    if (boundary_is_marked) {
        modify(interior);
    }
}

// 第四階段：根據 snapshot 修邊界
if (flag1) zero_boundary1();
if (flag2) zero_boundary2();
```

## Pitfalls
- **Snapshot 在 mutate 之前**：兩步順序顛倒就丟原始資訊
- **旗標值不能跟合法資料衝突**：例如 board 用 `'.'` 當 visited 因為 `'.'` 不在 `[A-Z]`；陣列用負號則要求原值都是正數
- **`matrix[0][0]` 雙重身份**：當 row 0、col 0 都拿來當旗標時，左上角會被兩個身份共用無法區分。要把其中一個移到獨立 bool
- **修改順序**：先處理 interior 再處理 boundary，否則邊界一變，interior 看到的旗標就錯
- **題目允不允許改 input**：有些題明文禁止修改原 array（如 [287] Find the Duplicate Number），這時 in-place marker 不適用，要改用其他 O(1) 招（Floyd's cycle 等）

---

## Problems

### [[73] Set Matrix Zeroes](../../problems/array/set_matrix_zeroes.md)
**Complexity:** Time O(m·n), Space O(1)
- **Trigger:** Matrix 裡任一格是 0 → 該 row 與 col 全清零；follow-up 要 O(1) space
- **Insight:** 用 row 0 / col 0 當其他 row / col 的旗標；邊界自己用兩個 bool snapshot 保留原始狀態
- **Pitfall:** `matrix[0][0]` 雙重身份要拆開；順序必須是 snapshot → mark → use → restore
