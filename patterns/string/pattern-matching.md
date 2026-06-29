# String — Pattern Matching (KMP)

## When to Use
- 要判斷 / 尋找一個**小字串**是否出現在一個**大字串**裡（substring search）
- brute force 的 `string::find` 每次 mismatch 都把小字串從頭再比，最壞 **O(N·M)**；當大字串長、或同一段文字要被反覆查時，想要 **O(N+M)**
- 小字串自身有**重複前綴結構**時，KMP 省最多（失敗時能直接跳過「已知一定會 match」的前綴）
- 訊號詞：`appears as a substring`、`find the index of`、`does pattern occur in text`、`count occurrences of`

跟 brute-force `find` 的差別：`find` 一 mismatch 就把大字串指標退回去逐位重試（O(N·M)）。KMP 先花 O(M) 把小字串的「失敗就退到哪」算成 **failure function**，之後**大字串指標永不後退** → O(N+M)。

## 核心：大字串 vs 小字串，兩個階段

目標是「**小字串是否在大字串裡**」。整條演算法只有兩個指標、兩個階段：

- `i` 掃**大字串**，`j` 掃**小字串**
- 先 **build failure**（只看小字串，自己跟自己比），再 **search**（大字串 vs 小字串）

最關鍵的前提：**failure 一定建在「小字串」（要找的那個 / 針）身上**。因為它編碼的是「小字串自己的 前綴=後綴 結構」，好讓配對失敗時知道 `j` 該退到哪。建在大字串上就等於把方向搞反了。

### failure function 的定義
`failure[k]` = 小字串前綴 `P[0..k]` 裡，**最長**、**proper**（比自己短）的 prefix，同時也是 suffix 的「**長度**」。

單一字元恆為 0：proper prefix / suffix 都只剩空字串。而且「proper」這個限制是演算法成立的根本——它逼著退格只能退到**更短**的狀態，否則退格不會收斂。

### Build：小字串自己跟自己比
兩個指標各自的身分（**容易貼反，記牢**）：

- `len` = **prefix 端**：已配好的前綴長度，也是「下一個要比的前綴 index」→ `P[len]` 是前綴字元
- `i` = **suffix 端**：往後長出來的新尾巴 → `P[i]` 是當前後綴的最後一個字元

三種情況：
- `P[i] == P[len]` → 可延長，`failure[i] = ++len`
- 不等且 `len > 0` → 退到更短的候選：`len = failure[len-1]`（**跟搜尋的退格同一招**）
- `len == 0` → 沒有 前綴=後綴，`failure[i] = 0`

### Search：大字串 vs 小字串
- `小字串[j] == 大字串[i]` → match，兩指標同進；`j` 配到小字串長度 → **完全找到**，起點 = `i - 小字串.size()`
- mismatch 且 `j > 0` → **退小字串指標**：`j = failure[j-1]`；**大字串指標 `i` 原地不動**
- mismatch 且 `j == 0` → 沒得退了，`i++`（大字串往前一格，小字串從頭重來）

> **KMP 的靈魂：大字串指標 `i` 永不後退。** 所有「重來」只發生在小字串指標 `j` 上，而且是 O(1) 查表跳轉。這就是 O(N+M) 而非 O(N·M) 的原因。

Build 和 Search 其實是**同一個骨架**：都是「相等就前進 / 不等且還有退路就 `失敗指標 = failure[失敗指標-1]` / 退無可退就推進外層指標」。Build 不過是把小字串當大字串、拿自己比自己而已。

## Typical Complexity
**Time:** 單次比對 **O(N + M)**。Build O(M)：只掃小字串一遍（攤還——`len` 的增與減總量有界）。Search O(N)：大字串指標 `i` 單調前進，`j` 的退格總次數 ≤ `i` 前進的總次數，攤還線性。
**Space:** **O(M)** — failure 陣列大小等於小字串長度。

> 多個小字串對同一個大字串（如 [[1967]]）：純 KMP 對每個小字串各建一次 failure，總和 **O(L·(N+M))**。想把大字串「只預處理一次、之後每個小字串快速查」，那是 suffix automaton 的領域（較冷門），純 KMP 做不到。

## Template Code
```cpp
// Build failure on the SMALL string (the needle we search for).
// failure[k] = length of the longest proper prefix of small[0..k]
//              that is also a suffix of small[0..k].
vector<int> build_failure(const string& small) {
    int slen = small.size();
    vector<int> failure(slen, 0);
    int len = 0;   // PREFIX side: matched prefix length = next prefix index
    int i = 1;     // SUFFIX side: current window end
    while (i < slen) {
        if (small[i] == small[len]) failure[i++] = ++len;   // extend
        else if (len > 0)           len = failure[len - 1]; // fall back to shorter
        else                        failure[i++] = 0;       // no prefix == suffix
    }
    return failure;
}

// Is `small` inside `big`? Return start index in `big`, or -1.
int kmp(const string& small, const string& big) {
    int blen = big.size(), slen = small.size();
    vector<int> failure = build_failure(small);
    int i = 0;   // BIG-string pointer — NEVER moves backward
    int j = 0;   // SMALL-string pointer (chars matched so far)
    while (i < blen) {
        if (big[i] == small[j]) {            // match: advance both
            i++; j++;
            if (j == slen) return i - slen;  // small fully matched -> found
        } else if (j > 0) {
            j = failure[j - 1];              // retreat SMALL pointer; i stays put
        } else {
            i++;                             // nothing to fall back to; advance BIG
        }
    }
    return -1;
}
```

> 變數用 `small` / `big` 命名是刻意的：KMP 最常見的 bug 就是把長度變數跟指標的身分接反。記住綁定關係即可，字母叫什麼不重要——`i` 走大字串就用大字串長當界線，`j` 數小字串就用小字串長判定找到。

## Pitfalls

| 雷 | 說明 |
|---|---|
| **failure 建錯對象** | failure 一定建在**小字串（針）**上，不是大字串。搞反 = 變成「在小字串裡找大字串」，方向整個錯 |
| **長度變數與指標不對齊** | `i` 走大字串 → 迴圈界線用**大字串長**；`j` 數小字串 → 找到用**小字串長**。接反會 early-stop（漏配，false negative）或 `大字串[i]` 越界（UB） |
| **build 的 prefix/suffix 貼反** | build 裡 `len` 是 **prefix 端**、`i` 是 **suffix 端**，不是反過來 |
| **以為 fail 動的是大字串指標** | fail 時退的是**小字串指標 `j = failure[j-1]`**；**大字串指標 `i` 永不後退**（這正是 O(N) 的來源） |
| **想對大字串建一次表重複用** | 純 KMP 做不到——failure 綁在針（小字串）上，每個小字串各建一次。要預處理大字串一次 → suffix automaton |

---

## Problems

### [[1967] Number of Strings That Appear as Substrings in Word](../../problems/string/number_of_strings_as_substrings.md)
**Complexity:** Time O(L·(N+M)), Space O(M)（L=小字串數量, N=大字串長, M=小字串長）
- **Trigger:** 問一堆小字串各自是否為大字串的 substring → 逐個做 substring search
- **Insight:** 對每個小字串建 failure、再到大字串裡跑 KMP，命中就 +1；大字串指標永不後退
- **Pitfall:** 方向別反（failure 建在小字串上、在大字串裡找小字串）；constraints ≤ 100，其實 `word.find` 一行就夠，KMP 是練手
