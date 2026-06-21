# [30] Substring with Concatenation of All Words
**Pattern:** [Sliding Window](../../patterns/sliding-window.md)
**Complexity:** Time O(S·word_len + W), Space O(S+W)
**Link:** https://leetcode.com/problems/substring-with-concatenation-of-all-words/

## Trigger Signals
- 給字串 `s` 和一組**等長**的 `words`,找出所有起點,使從該起點開始的子字串**剛好**是 words 全部串接(任意順序)而成
- 「連續區間 + 涵蓋一組目標(含重複次數)+ 等長」→ 固定大小 sliding window,但**以「詞」為單位**而非字元
- 「等長」是關鍵條件:它讓目標視窗長度固定(`target_size = words.size() * word_len`),也讓字串能切成整齊的詞格

## Core Insight
這是 fixed window,但有兩個跟一般 fixed window 不一樣的轉折。

**1. 視窗以「詞」為單位滑動。**
先對 words 建頻率表,算出滿視窗長度 `target_size = words.size() * word_len`。右指針每次吃進一個 `word_len` 長的詞;視窗長度達到 `target_size` 就檢查詞頻是否全中,中了記下當前 `l`,然後固定滑掉最左一個詞。用 `formed`(已達標的詞種數)把「合不合法」壓到 O(1)——和 LC76 同一招,只是 key 從字元換成詞。

**2. 起點不一定對齊 word_len 的倍數 → 要跑 word_len 條獨立視窗。(最容易漏)**
合法答案必須是「整顆詞首尾相接」,起點 `p` 一旦定了,所有切點 `p, p+word_len, p+2·word_len...` 就鎖死。起點差 1 格,整排切點全部錯開,切出來是完全不同的詞。所以候選起點按 `start mod word_len` 分成 **word_len 個類別**,每類是一條獨立的「詞格線」。`offset` 從 `0` 跑到 `word_len-1`,每條格線各跑一次 fixed window。

> `s = "barfoo"`、word_len=3,三條格線切出完全不同的詞:
>
> | start mod 3 | 切法 | 詞 |
> |---|---|---|
> | 0 | `bar \| foo` | bar, foo |
> | 1 | `b \| arf \| oo` | arf, … |
> | 2 | `ba \| rfo \| o` | rfo, … |

關鍵體悟:位置上,所有 offset 的內層 `r` 加起來確實連續覆蓋了整個 `s` 的每個位置,但那是 **word_len 條平行視窗在位置上交錯**,不是一條連續視窗。window 存的是「這條格線下各詞出現幾次」,**狀態綁在格線上**——換 offset = 換格線 = 換一整套詞,所以 `window` / `formed` / `l` 每個 offset 都必須從頭來過,否則是拿 A 格線的詞數去算 B 格線的帳。

## Complexity Analysis
先記我原本算錯的地方,免得再犯。

**Time:我一開始寫 O(S + W),漏了一個 `word_len` 因子。**
- 滑動每一步做的是 `s.substr(r, word_len)` + 丟進 `unordered_map<string>`,那是**複製 + 雜湊一個長度 word_len 的字串 = O(word_len)**,不是 O(1)。
- 長度 word_len 的詞在 `s` 裡的起始位置共 `~S` 個,每個只在它自己的 offset 被看一次,每次 O(word_len)。
- 所以滑動是 **O(S · word_len)**;建表 O(W);合計 **O(S·word_len + W)**,主項 O(S·word_len)。
- 想真的做到 O(S + W),得讓「辨認一個詞」降到 O(1):rolling / prefix hash 預處理,或把每個 distinct 詞預先編號成 int。substr 版沒做這層,所以帶 word_len。

(W = 所有 words 的總字元數 = `words.size() · word_len`,也就是建表成本。)

**Space: O(S + W),這個算對了。**
- `O(max(S, W))` 和 `O(S + W)` 是**同一個 class**(`max(a,b) ≤ a+b ≤ 2·max(a,b)`),寫哪個都行。
- 拆開:`target` 表 O(W);`window` 在沒有 erase 時,連非目標詞都會累積成 key,最壞存下整條 offset 的所有 distinct 子字串 → O(S)。
- 修正一個用詞:window 裡的子字串**個數**是 `O(S / word_len)`(每條 offset 最多這麼多 slot),不是 O(S);但每個長度 word_len,乘起來空間才是 O(S)。
- 若「count 歸零就 `erase`」或「遇到非目標詞就清空 window」,window 可壓到 O(W),總空間變 O(W)。

## Solution Code
```cpp
class Solution {
public:
    vector<int> findSubstring(string s, vector<string>& words) {
        unordered_map<string, int> target;
        int word_len = words[0].size();
        for (const auto& w : words) {
            target[w]++;
        }
        int required = target.size();
        int target_size = words.size() * word_len;

        vector<int> res;
        for (int offset = 0; offset < word_len; offset++) {
            int l = offset;
            int formed = 0;
            unordered_map<string, int> window;
            for (int r = offset; r + offset < s.size(); r += word_len) {
                string r_word = s.substr(r, word_len);
                window[r_word]++;
                if (window[r_word] == target[r_word]) {
                    formed++;
                }
                // concatenated substring
                if (r - l + word_len == target_size) {
                    // check
                    if (formed == required) {
                        res.push_back(l);
                    }
                    // shrink
                    string l_word = s.substr(l, word_len);
                    if (window[l_word] == target[l_word]) {
                        formed--;
                    }
                    window[l_word]--;
                    l += word_len;
                }
            }
        }
        return res;
    }
};
```

## Pitfalls

### 視窗滿了但沒配對時,也要縮(我最初的 bug)
最初我把縮視窗關在 `while (formed == required && 視窗長度 == target_size)` 裡。視窗填滿但 `formed != required` 時,**沒有任何東西縮左邊**,下一輪視窗長度變成 `target_size + word_len`,`視窗長度 == target_size` 從此再也不成立 → 後面全漏。這就是「改一個壞另一邊」的根源:把「何時縮」和「何時記錄」綁在同一個條件裡。
修法是拆成三件獨立的事:**長視窗**(for 右進)、**縮視窗**(只看超不超長)、**記答案**(滿了 + 全配對)。

### fixed window 用 `if` 縮,不是 `while`
這裡每步只加一個詞、超標最多一格,縮一次就回到 `target_size` → 用 `if`。判準:一次右移後左指針最多要追幾步,一步 `if`、多步 `while`。

### 每個 offset 都要重置 window / formed / l(這個我踩了,而且測資很挑)
共用 window 會讓上一條格線的詞數殘留,污染下一條。但**這個 bug 不是隨便一個測資都打得到**:
- 我原本拿 `s = "dddddddd"`(8 個 d)、`words = ["dddd","dddd"]` 想證明會錯,**結果兩種寫法都吐 `[0]`**。因為 `s.size() == target_size`,只有 offset 0 塞得下滿視窗,offset 1~3 連視窗長度 `== target_size` 都到不了,殘留再多也用不到。
- **實測掃長度 8~14:len 8、9 都過,len 10 才第一次出錯**(reset 得 `[0,1,2]`,共用得 `[0,1]`,漏掉 2)。
- 為什麼是 10?殘留會越積越多:offset 1 開始時殘留 `{dddd:1}`,offset 2 開始時 `{dddd:2}`。關鍵在 `window[r_word]++;` 之後那個 `if (window[r_word] == target[r_word]) formed++;`——`formed` 只在 `window[r_word]` **正好等於 target(=2)** 那一次才加:offset 1 殘留 1,加一個變 2 → **歪打正著還是對的**;offset 2 殘留 2,再加變 3、4 → **跳過 2**,formed 永遠加不上去 → 漏。所以第一個真正爆掉的是 offset 2,而 offset 2 要湊滿視窗需要 `s.size() ≥ 2 + target_size = 10`。

### `unordered_map::operator[]` 讀不存在的 key 會偷插 0
`window[r_word] == target[r_word]` 對非目標詞會在 `target` 插入 value=0 的 entry。這題因為 `required` 一開始就存起來、之後不再讀 `target.size()`,所以**不影響答案**;但仍是髒資料。對照 LC76:那裡若拿 `target.size()` 當判準就會 WA,這題剛好躲過。

## 延伸 / Follow-up
LC30 官方沒有明列 follow-up;最自然的延伸是:**如果 `words` 不等長呢?**
這個解法的三根支柱全建立在「等長」上——
- 滿視窗長度 `target_size = words.size() * word_len` 能事先算出;
- 內層 `r += word_len` 有統一步長;
- 按 `start mod word_len` 切成 word_len 條格線。

不等長的話三根全倒,就不再是乾淨的滑動視窗,而變成更一般的多模式配對(得換別的技巧,如回溯 / trie),難度高一截。等長正是讓這題「可滑動」的關鍵前提。

## Related Problems
- [76] Minimum Window Substring — 同樣用 `formed` 計數,但 variable window + 字元粒度
- [567] Permutation in String / [438] Find All Anagrams — fixed window 找 anagram,字元粒度;一步一字元所以**沒有 offset 問題**
- 對照記:LC76 先記後縮(`while` 合法才縮);LC30 是 fixed window → `if` 縮、後記
