# [48] Rotate Image
**Pattern:** [Array → In-place Transform](../../patterns/array/in-place-transform.md)
**Complexity:** Time O(n²), Space O(1)
**Link:** https://leetcode.com/problems/rotate-image/

## Trigger Signals
- n×n matrix，要做 90° 順時針旋轉
- 題目明文要求 **in-place**（不能 alloc 新 matrix）
- 直接套座標公式 `(r, c) -> (c, n-1-r)` 會踩到「來源是別人的目的地」的依賴環，無法單次 swap

## Core Insight
把目標變換**拆成兩個 in-place primitive 的組合**：

```
(r, c) ──transpose──> (c, r) ──reverse each row──> (c, n-1-r)   ✓ = 90° CW
```

每個 primitive 都是兩兩配對的 swap，因此可以 in-place 完成。

## Complexity Analysis
- **Time O(n²)**：transpose 走下三角共 n(n-1)/2 個 swap，reverse 每行走前半共 n·(n/2) 個 swap，合計 ~n² 次 swap
- **Space O(1)**：只有迴圈 index 與 swap 用的 temp 變數

## Solution Code
```cpp
class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        // 90 clockwise: (r, c) -> (c, n-1-r)
        // = transpose (r,c)->(c,r), then reverse each row (r,c)->(r,n-1-c)

        int n = matrix.size();

        // Step 1: transpose. Lower triangle only, otherwise swap twice = no-op.
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                swap(matrix[i][j], matrix[j][i]);
            }
        }

        // Step 2: reverse each row. Swap j with n-1-j, half is enough.
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n / 2; j++) {
                swap(matrix[i][j], matrix[i][n - 1 - j]);
            }
        }
    }
};
```

## Pitfalls
### Transpose 必須只走下三角
若寫成 `for (j = 0; j < n; j++)`，每對 `(i,j)` 與 `(j,i)` 會被 swap 兩次，等於沒做。掃 `j < i` 或 `j > i` 皆可，但必須擇一。

### 順序顛倒會變成逆時針
- `transpose ∘ reverse-row` = 90° CW
- `reverse-row ∘ transpose` = 90° CCW（等價於 270° CW）

推導完目標公式 `(r,c) -> (c,n-1-r)` 後一定要驗證合成方向，不能憑直覺。

### 註解的習慣
- 寫**為什麼**這樣做（why），不是寫**做了什麼**（what）
- 例如 `// lower triangle, avoid double-swap` 比 `// only diagonal` 清楚
- `// swap j with n-1-j, half is enough` 比 `// only first half` 清楚

### 座標表記
matrix 裡 `matrix[i][j]` 第一個 index 是 row。註解寫 `(r, c)` 比 `(x, y)` 不易混淆（x 通常是橫軸，但 row 是縱向）。

## Related Problems
- [54] Spiral Matrix — 同樣 2D 走訪，但走訪順序而非 in-place 變換
- [867] Transpose Matrix — Primitive 之一，但允許 alloc 新 matrix
- [189] Rotate Array — 1D 版本，同樣可用 reverse 三次組合達成 in-place
