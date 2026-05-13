# [79] Word Search
**Pattern:** [Backtracking → Grid Backtracking](../../patterns/backtracking/grid-backtracking.md)
**Complexity:** Time O(m·n·4^L), Space O(L)（L = `word.size()`）
**Link:** https://leetcode.com/problems/word-search/

## Trigger Signals
- 2D grid，需要找出一條相鄰路徑拼出某 string
- 「the same letter cell may not be used more than once」→ 同一條路徑不能重用 → 需 backtrack restore
- 不同起點各自獨立 → 每個起點 DFS 完都要把 grid 還原

## Core Insight
以每個 `board[i][j] == word[0]` 的格子為起點，做 DFS：進入時把該格改成 `'.'` 標記為 visited，遞迴探索 4 個鄰居匹配 `word[idx]`，若失敗就還原。`'.'` 不在原字元集（A-Z/a-z）所以可以安全當 sentinel。

## Complexity Analysis
- **Time O(m·n·4^L)**：`m·n` 個起點，每個起點最壞做 4^L 的搜尋（每步 4 個方向、深度 L）。實際上因為「不能回頭走自己」，分支數平均約 3，但最壞仍是 4^L。Pruning（提前 mismatch 就 return）只能降常數。
- **Space O(L)**：遞迴堆疊深度等於 `word` 長度；in-place mark 不額外耗空間。

## Solution Code
```cpp
class Solution {
public:
    bool exist(vector<vector<char>>& board, string word) {
        /*
            Try every cell as the starting point. On entering a cell,
            mark it visited ('.') and recurse into 4-neighbors that
            match the next character; restore the original letter on
            return so other branches can reuse the cell.
        */
        int m = board.size();
        int n = board[0].size();
        /* O(mn) pruning */
        unordered_map<int, int> freq;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                freq[board[i][j]]++;
            }
        }
        for (auto c : word) {
            if (--freq[c] < 0) {
                return false;
            }
        }
        // O(mn) feasibility prune: board must contain
        // every character word needs
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (board[i][j] != word[0] || board[i][j] == '.') {
                    continue;
                }
                char saved = board[i][j];
                board[i][j] = '.';
                if (solve(board, i, j, 1, word)) {
                    return true;
                }
                board[i][j] = saved;
            }
        }
        return false;
    }

private:
    bool solve(vector<vector<char>>& board, int i, int j, int idx,
               const string& word) {
        if (idx == word.size()) {
            return true;
        }
        int m = board.size();
        int n = board[0].size();
        static int dirs[5] = {-1, 0, 1, 0, -1};
        for (int k = 0; k < 4; k++) {
            int ni = i + dirs[k];
            int nj = j + dirs[k + 1];
            // out of bound
            if (ni < 0 || nj < 0 || ni >= m || nj >= n) {
                continue;
            }
            char saved = board[ni][nj];
            // prune
            if (saved == '.' || saved != word[idx]) {
                continue;
            }
            // push
            board[ni][nj] = '.';
            if (solve(board, ni, nj, idx + 1, word)) {
                return true;
            }
            // pop
            board[ni][nj] = saved;
        }
        return false;
    }
};
```

## Follow-up: Pruning for Larger Board
原題 follow-up：「Could you use search pruning to make your solution faster with a larger board?」

### Frequency Feasibility Check（已實作）
**做了什麼**：DFS 之前先 O(m·n) 統計 `board` 每個字元次數，逐字元扣 `word` 的需求，任一字元不夠就 `return false`。

**為什麼有效**：larger board 上若根本拼不出 `word`，樸素做法會把每個合法起點 DFS 一遍才放棄。一次線性掃描就把整批不可能的 case 擋在 DFS 之外。

**`--freq[c] < 0` 慣用法**：pre-decrement 回傳「扣完之後」的新值，把「扣 1 + 檢查 < 0」綁在同一 expression。語意是「扣完還合法嗎」。若用 post-decrement `freq[c]-- < 0` 就變成「扣之前合法嗎」，會晚一輪偵測，語意錯誤。

**沒做**：reverse word（比較 `word.front()` 與 `word.back()` 在 `board` 出現次數，少的那邊當起點）。對「能拼出來但起點數懸殊」的測資仍有空間。

## Pitfalls
- 起點 cell 也必須 mark 為 `'.'`，否則 DFS 可能繞回起點當作有效鄰居
- Prune 條件 `saved == '.' || saved != word[idx]`：兩個都不可少。少了 `'.'` 檢查會走回頭路；少了字元比對就完全沒剪枝
- 找到答案後直接 `return true` 一路向上傳，不要在 caller 還做還原（其實還原也無妨，但會浪費）。本實作在主 loop 找到時直接 return，沒有把起點 cell 還原 —— 若題目要求保持 board 不變，需在 return 前還原
- `word` 長度可能大於 `m*n`，但這不會破壞正確性（DFS 會在無路可走時 return false）

## Related Problems
- _尚無_
