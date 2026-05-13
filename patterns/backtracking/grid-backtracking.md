# Backtracking — Grid Backtracking

## When to Use
- 在 2D `board` / `grid` 上做 DFS，且**同一條路徑不能重複經過同一格**
- 需要「進入 → 標記 → 探索鄰居 → 還原」的流程；還原這一步是與單純 grid traversal（如 Number of Islands）的關鍵差別
- 題目敘述出現：是否存在路徑、是否能拼出某字串、word / path / visited 不能重複

與單純 grid DFS（flood fill 類）的區別：flood fill 只需 mark visited 不需 restore，因為一旦走過的格子永遠不會再被「重新使用」；grid backtracking 走過的格子在 backtrack 後會被「釋放」給其他分支使用。

## Template Code
```cpp
bool dfs(vector<vector<char>>& board, int i, int j, /* state */) {
    if (/* base: found */) return true;
    int m = board.size(), n = board[0].size();
    static int dirs[5] = {-1, 0, 1, 0, -1};
    for (int k = 0; k < 4; k++) {
        int ni = i + dirs[k], nj = j + dirs[k + 1];
        if (ni < 0 || nj < 0 || ni >= m || nj >= n) continue;
        char saved = board[ni][nj];
        if (saved == VISITED_MARK || !match(saved, /* state */)) continue;
        board[ni][nj] = VISITED_MARK;          // make
        if (dfs(board, ni, nj, /* next state */)) return true;
        board[ni][nj] = saved;                 // undo
    }
    return false;
}
```

關鍵技巧：
- **Direction array**：`int dirs[5] = {-1, 0, 1, 0, -1}` 用 `(dirs[k], dirs[k+1])` 取出 4 方向，比 `{{-1,0},{1,0},{0,-1},{0,1}}` 簡潔
- **In-place visited**：直接改 `board[i][j]` 為某個原字元集不會出現的值（如 `'.'`），省去額外 `visited` array；backtrack 時還原。代價是修改了輸入

## Pitfalls
- 忘了 restore，等同於普通 DFS 而非 backtracking，會錯誤地禁止其他起點走過該格
- Mark visited 與 prune 的順序：先 prune 再 mark，否則無效路徑也會被無謂修改
- 起點本身也需要 mark；不要只在進入鄰居時才 mark
- 用 in-place mark 時，挑的「visited 標記值」必須跟原字元集不重疊

---

## Problems

### [[79] Word Search](../../problems/backtracking/word_search.md)
**Complexity:** Time O(m·n·4^L), Space O(L)
- **Trigger:** 2D grid 找相鄰路徑拼字串、同 cell 不能重用
- **Insight:** 每格當起點 DFS，in-place mark `'.'` 為 visited，失敗就還原
- **Pitfall:** 起點也要 mark；`saved == '.'` 與字元比對兩個 prune 都不能少
