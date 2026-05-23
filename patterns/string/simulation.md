# String — Simulation

## When to Use
- 題目本質是**在字串上模擬人類筆算的算術過程**：multiply / add / subtract / plus one / atoi / add binary
- 不能用內建大數型別（題目明文禁止，或數值會 overflow int64）
- 操作的單位是「一位數字」，需要處理**位數對齊**與**進位 / 借位**
- Follow-up 常要求壓掉中間 buffer，直接在 output 字串上就地累加

跟一般 string parsing 的差別：simulation 類有明確的算術模型（位數、進位、權重），錯誤通常來自 index 算錯或 char↔int 轉換漏寫；parsing 類比較像狀態機，錯誤來自 case 沒覆蓋全。

## Core Technique: 位數定位 + char-as-buffer

### 1. 位數定位公式
兩數相乘 `num1[j] * num2[i]`（兩字串都從左到右 index）：
- 個位放 `res[i + j + 1]`
- 進位放 `res[i + j]`
- result 長度設 `m + n` 剛好夠容納（最高位進位最多落在 index 0）

推導：`num1[j]` 代表 `10^(m-1-j)`，`num2[i]` 代表 `10^(n-1-i)`，乘積落在 `10^(m+n-2-i-j)`，反推位置即 `i+j+1`。

### 2. 把 output 字串當 buffer（O(1) extra space）
原本要開 `vector<int>(m+n, 0)` 累加再轉字串，可以直接用 `string res(m+n, '0')` 在 char 上做算術，省掉中間 buffer。代價是 char↔int 轉換的心智負擔。

## Template Code
```cpp
// Pattern: simulate multi-digit arithmetic char-by-char,
// accumulate directly into the result string.

string res(m + n, '0');
for (int i = n - 1; i >= 0; i--) {
    for (int j = m - 1; j >= 0; j--) {
        int prod = (num1[j] - '0') * (num2[i] - '0');
        int p1 = i + j + 1;  // units position
        int p2 = i + j;      // carry position

        // Extract current value into int, then write back.
        int sum = prod + (res[p1] - '0');
        res[p1] = '0' + sum % 10;   // overwrite (already extracted)
        res[p2] += sum / 10;         // accumulate (not touched yet)
    }
}

size_t pos = res.find_first_not_of('0');
return pos == string::npos ? "0" : res.substr(pos);
```

## Pitfalls

### 三大常錯點
| 雷 | 記法 |
|---|---|
| index `i+j+1` vs `i+j` | 「**個位在右、進位在左**」，個位是 `+1` |
| char ± `'0'` 何時做 | 「**進去 char 加 `'0'`、出來 int 減 `'0'`**」，純 int 之間運算不要再 ±`'0'` |
| `=` vs `+=` | 「**抽過用 `=`、沒抽過用 `+=`**」——剛 extract 的格子覆蓋，未動過的格子累加 |

收斂成一個原則：**先抽出來變 int，最後再寫回 char**。

### 其他
- **空字串 / "0" edge case**：任一 operand 是 `"0"` 要先短路，否則最後 `find_first_not_of('0')` 會回傳 `npos` 而當機
- **`find_first_not_of` 回傳 `npos` 時**：結果全是 `'0'`（理論上前面短路掉了，但保險起見要處理）
- **carry char 不會爆**：每格最多累積一輪進位（次輪會被 `=` 覆蓋），上限約 9 + 8 = 17，char 範圍安全
- **替代解法**：若不想碰 char 算術，用 `vector<int>(m+n, 0)` 當 buffer 完全避開陷阱，多 O(m+n) 空間但寫一次就對

## When NOT to Use
- 數值範圍能塞進 int64 → 直接轉成數字運算
- 純解析（沒有算術模型，只是切 token / 驗格式）→ 用一般 string parsing / 狀態機
- 模式比對 → KMP / Rabin-Karp 等專門演算法

---

## Problems

### [[43] Multiply Strings](../../problems/string/multiply_strings.md)
**Complexity:** Time O(m·n), Space O(m+n) for output（extra space O(1)）
- **Trigger:** 兩字串相乘且禁用大數型別；要求 O(1) extra space
- **Insight:** `num1[j]*num2[i]` 的個位落在 `res[i+j+1]`、進位落在 `res[i+j]`；直接拿 result string 當 buffer 在 char 上做算術，省掉中間 int array
- **Pitfall:** char 算術三雷——index 位置、`±'0'` 時機、`=` vs `+=`；用「先抽成 int 再寫回 char」收斂
