# Backtracking

## When to Use
- 需要列舉所有可能解（permutations、combinations、subsets）
- 解空間是樹狀結構，每個節點代表「目前的部分解」
- 有「選 / 不選」或「選哪一個」的決策點，且選錯後可以放棄回頭
- 題目敘述出現：所有可能、是否存在一條路徑、enumerate、generate all
- 與 DP 的差別：backtracking 列舉「具體的解」，DP 計算「解的個數或最佳值」而不還原路徑

## Typical Complexity
**Time:** 通常是指數級，O(b^d) 其中 b 是每層分支數、d 是搜尋深度。剪枝（pruning）只能改善常數，不會改變最壞情況的階。
**Space:** O(d) 遞迴堆疊深度；若需要紀錄目前路徑也是 O(d)。

## General Template
```cpp
void backtrack(State& state, /* problem-specific args */) {
    if (/* found a solution */) {
        record(state);
        return;
    }
    for (auto& choice : candidates(state)) {
        if (!isValid(choice, state)) continue;  // prune
        apply(choice, state);                   // make choice
        backtrack(state, ...);                  // recurse
        undo(choice, state);                    // restore
    }
}
```

三個關鍵動作：**make choice → recurse → undo**。Undo 是 backtracking 與一般 DFS 的分界線。

## Common Variations
- [Grid Backtracking](grid-backtracking.md) — 在 2D grid 上 DFS，需 mark visited + restore
