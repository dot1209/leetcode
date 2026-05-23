# [43] Multiply Strings
**Pattern:** [String → Simulation](../../patterns/string/simulation.md)
**Complexity:** Time O(m·n), Space O(m+n) for output（extra space O(1)）
**Link:** https://leetcode.com/problems/multiply-strings/

## Trigger Signals
- 兩個非負整數**以字串給定**，輸出乘積也是字串
- 題目明文禁止使用內建大數型別、也不能直接轉 int（暗示數值可能超過 int64）
- 經典 follow-up：能不能不開額外 buffer？

## Core Insight
直式乘法 `123 × 456` 可拆成 `123×6 + 123×50 + 123×400`。每個單格乘法 `num1[j] * num2[i]` 落在固定位置：

- **個位** → `res[i + j + 1]`
- **進位** → `res[i + j]`

長度 `m + n` 的 `res` 剛好容納所有位數（最高位進位最多落在 index 0）。把所有單格乘積**就地累加**進 result，省掉「先算完每行 partial product 再加總」的中間 buffer。

進一步把 result 直接宣告成 `string(m+n, '0')`，在 char 上做算術，就能達到「除了答案本身外 O(1) extra space」。

## Complexity Analysis
- **Time O(m·n)**：m × n 個單格乘法，每次 O(1)
- **Space O(m+n)**：result 字串本身，這是輸出無法避免的下限。**Extra space O(1)**——沒有額外的 vector / hashmap

真正的 O(1) total 不可能，因為輸出長度至少 `m + n - 1`。

## Solution Code
```cpp
class Solution {
public:
    string multiply(string num1, string num2) {
        if (num1 == "0" || num2 == "0") return "0";

        int m = num1.size(), n = num2.size();
        string res(m + n, '0');

        for (int i = n - 1; i >= 0; i--) {
            for (int j = m - 1; j >= 0; j--) {
                int prod = (num1[j] - '0') * (num2[i] - '0');
                int p1 = i + j + 1;  // units position
                int p2 = i + j;      // carry position

                // Extract res[p1] into sum, then write back.
                int sum = prod + (res[p1] - '0');
                res[p1] = '0' + sum % 10;   // overwrite: value was extracted
                res[p2] += sum / 10;         // accumulate: not yet touched
            }
        }

        size_t pos = res.find_first_not_of('0');
        return pos == string::npos ? "0" : res.substr(pos);
    }
};
```

### 替代解法（避開 char 算術陷阱）
```cpp
vector<int> buf(m + n, 0);
for (int i = n - 1; i >= 0; i--) {
    for (int j = m - 1; j >= 0; j--) {
        int sum = (num1[j] - '0') * (num2[i] - '0') + buf[i + j + 1];
        buf[i + j + 1] = sum % 10;
        buf[i + j]    += sum / 10;
    }
}
string res;
for (int d : buf) if (!(res.empty() && d == 0)) res += ('0' + d);
return res.empty() ? "0" : res;
```
多 O(m+n) extra space，但完全沒有 char 算術 → 心智負擔小。

## Pitfalls
- **char 算術三雷**：
  - index：個位 `i+j+1`（右），進位 `i+j`（左）
  - `'0'` 偏移：char 加減要 `±'0'`；純 int 不要再 `+'0'`
  - `=` vs `+=`：剛 extract 的格子用 `=` 覆蓋，沒動過的格子用 `+=` 累加
  - **收斂原則**：先抽出來變 int，最後再寫回 char
- **`"0"` edge case**：任一 operand 是 `"0"` 必須先短路，否則 `find_first_not_of('0')` 回傳 `npos`，`substr(npos)` 會 throw
- **進位不會撐爆 char**：同一格被當「carry 接收位」最多累積一輪（次輪會被覆蓋為 `'0' + sum%10`），上限 `'9' + 8 = ':' (58)`，char 範圍安全
- **長度為什麼是 `m+n` 不是 `m+n-1`**：最高位 `i=0, j=0` 的進位會落在 index 0，需要那一格

## Related Problems
- [415] Add Strings — 同類 char-by-char 模擬，只有加法、只有單一進位鏈
- [67] Add Binary — Base 2 版本的 Add Strings
- [66] Plus One — array 形式的加法模擬，重點在進位傳遞與長度擴展
- [2] Add Two Numbers — Linked list 版加法，同樣的進位模型
