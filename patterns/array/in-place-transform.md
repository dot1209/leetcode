# Array — In-place Transform

## When to Use
- 題目要對 array / matrix 做**結構性變換**（旋轉、轉置、reverse、layer 重排），且要求 **O(1) extra space**
- 目標座標公式跟原座標差距大，**直接搬一次就會覆蓋掉還沒用到的值**
- 輸入允許就地修改

跟 [[in-place-marker]] 的差別：marker 是「把布林狀態藏進位置」，transform 是「把複雜變換拆成幾個簡單的 in-place primitive 組合」。兩者共同目標都是 O(1) extra space，但動機與技巧不同。

## Core Technique: Decompose into Primitives
直接套目標公式 `(r, c) -> (r', c')` 會踩到「來源位置同時是別人的目的地」的依賴環，必須整層暫存。

正確做法是**把目標變換拆成兩個（或更多）primitive in-place 操作**，每個 primitive 的特性是「來源與目的地兩兩配對」，可以靠 `swap` 一次完成：

| Primitive       | 對應的 swap                              | 走訪範圍              |
|-----------------|------------------------------------------|-----------------------|
| Transpose       | `swap(a[i][j], a[j][i])`                 | Lower triangle `j<i`  |
| Reverse row     | `swap(a[i][j], a[i][n-1-j])`             | 前半 `j<n/2`          |
| Reverse col     | `swap(a[i][j], a[n-1-i][j])`             | 上半 `i<n/2`          |

組合範例（90° clockwise = transpose ∘ reverse-row）：
```
(r, c) ──transpose──> (c, r) ──reverse row──> (c, n-1-r)   ✓
```

## Template Code
```cpp
// Example: 90° clockwise rotation
// Target: (r, c) -> (c, n-1-r)
// Decompose: transpose, then reverse each row

int n = matrix.size();

// Step 1: transpose. Walk lower triangle only,
// otherwise each pair is swapped twice = no-op.
for (int i = 0; i < n; i++) {
    for (int j = 0; j < i; j++) {
        swap(matrix[i][j], matrix[j][i]);
    }
}

// Step 2: reverse each row. Walk first half only.
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n / 2; j++) {
        swap(matrix[i][j], matrix[i][n - 1 - j]);
    }
}
```

## Pitfalls
- **半範圍掃描**：swap 是對稱操作，掃完整個 range 會把每對 swap 兩次抵銷。Transpose 用下三角 `j<i`，reverse 用前半 `j<n/2`
- **拆解順序不可交換**：`transpose ∘ reverse` 跟 `reverse ∘ transpose` 結果不同（前者 = 順時針 90°，後者 = 逆時針 90°）。推導完目標公式後一定要驗證合成方向
- **奇數邊長 reverse 中點**：`n/2` 自動跳過正中間那格，因為中點 swap 自己沒影響；但若改成 `(n+1)/2` 會多做一次無用 swap
- **不要直接套 `(r,c) -> (r',c')`**：一旦目的地跟還沒處理到的來源重疊就會覆蓋；要不是改用 layer-by-layer ring swap（四值一次到位），要不就拆成 primitive

## When NOT to Use
- 直接公式可以無衝突 mapping（罕見；通常只有 identity / reverse 自己這種對合）
- 允許 O(n²) extra space 且追求易讀性 → 直接 alloc 新 matrix 通常更清楚
- 變換不是線性座標 mapping（如 Game of Life 的 cell-based 規則）→ 看 [[in-place-marker]]

---

## Problems

### [[48] Rotate Image](../../problems/array/rotate_image.md)
**Complexity:** Time O(n²), Space O(1)
- **Trigger:** Matrix 90° 順時針旋轉，要求 in-place
- **Insight:** `(r,c) -> (c,n-1-r)` 拆成 transpose 再 reverse 每行；兩個 primitive 各自能 in-place swap
- **Pitfall:** Transpose 只走下三角、reverse 只走前半，否則做兩次抵銷；順序顛倒會變成逆時針
