# [73] Set Matrix Zeroes
**Pattern:** [Array → In-place Marker](../../patterns/array/in-place-marker.md)
**Complexity:** Time O(m·n), Space O(1)
**Link:** https://leetcode.com/problems/set-matrix-zeroes/

## Trigger Signals
- 2D matrix，任一格是 0 → 整 row 與整 col 都要清零
- Follow-up 要求 O(1) extra space（不能用 O(m+n) 的旗標陣列、也不能拷貝整個 matrix）
- 觀察：旗標的本質是「每個 row / col 一個 bool」 → 想辦法把這些 bool 收進 matrix 自身

## Core Insight
用 **matrix 的 row 0 與 col 0 當其他 row / col 的旗標**：
- `matrix[i][0] == 0` 代表 row i 要清零
- `matrix[0][j] == 0` 代表 col j 要清零

但 row 0 / col 0 自己原本是否有 0（決定它們最後該不該清）會被自己的旗標身份覆蓋，所以需要**兩個 bool 先 snapshot** 原始狀態。

關鍵順序：**snapshot → mark → use → restore**。

## Complexity Analysis
- **Time O(m·n)**：四個階段都是線性掃 matrix 或邊界，最壞 O(m·n)
- **Space O(1)**：只多兩個 bool 與幾個 index 變數，沒開新陣列

## Solution Code
```cpp
class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        int rows = matrix.size();
        int cols = matrix[0].size();

        // 1. Snapshot: row 0 / col 0 原本有沒有 0
        bool firstRowZero = false;
        bool firstColZero = false;
        for (int j = 0; j < cols; j++)
            if (matrix[0][j] == 0) { firstRowZero = true; break; }
        for (int i = 0; i < rows; i++)
            if (matrix[i][0] == 0) { firstColZero = true; break; }

        // 2. Mark: 用 row 0 / col 0 當其他 row / col 的旗標
        for (int i = 1; i < rows; i++)
            for (int j = 1; j < cols; j++)
                if (matrix[i][j] == 0) {
                    matrix[i][0] = 0;
                    matrix[0][j] = 0;
                }

        // 3. Use: 依旗標清 interior（i, j >= 1）
        for (int i = 1; i < rows; i++)
            for (int j = 1; j < cols; j++)
                if (matrix[i][0] == 0 || matrix[0][j] == 0)
                    matrix[i][j] = 0;

        // 4. Restore: 根據 snapshot 處理 row 0 / col 0 本身
        if (firstRowZero)
            for (int j = 0; j < cols; j++) matrix[0][j] = 0;
        if (firstColZero)
            for (int i = 0; i < rows; i++) matrix[i][0] = 0;
    }
};
```

## Pitfalls
### 順序錯亂的後果
- **先 mark 再 snapshot**：snapshot 看到的已是「marker 後」的狀態，永遠是 true（只要 interior 有 0），原始資訊已經被毀
- **先 restore 再 use**：邊界先變成全 0，interior 看到旗標都是 0，會把整個 matrix 清零
- **正確順序**：snapshot 一定最先、restore 一定最後

### 邊界迴圈別 off-by-one
Mark / Use 兩個迴圈是 `i = 1..rows-1`、`j = 1..cols-1`（不含邊界）。
Snapshot / Restore 兩個迴圈是 `0..rows-1`、`0..cols-1`（含整邊界）。
常見錯誤：mark loop 寫成 `i < rows-1` 漏掉最後一列。

### 為什麼 Use 階段不會誤清旗標
Use 階段只處理 i, j ≥ 1 的格子，不會動 row 0 / col 0，所以旗標在這階段保持有效。如果用 j = 0 開始掃，就會把旗標自己也視為「需要清零」的資料而提前清掉。

## Related Problems
- [41] First Missing Positive — 用負號當「值 i 已出現」的旗標，同樣是 in-place marker
- [442] Find All Duplicates in an Array — 同上招式
- [287] Find the Duplicate Number — 反例：題目禁止修改 input，這時 in-place marker 不適用，要用 Floyd's cycle
