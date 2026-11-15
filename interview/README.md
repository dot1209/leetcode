# Google L4 Interview Practice Tracker

此目錄記錄 Google Taiwan L4 Coding Interview 的**解題獨立性與實際表現**。它不取代 `problems/`、`patterns/` 的演算法筆記。

- [sessions.md](sessions.md) — 每次練習的結果、提示程度、程式碼狀態、概念缺口與下一步。
- [coverage.md](coverage.md) — 依領域彙總證據與待驗證的變形。

## 評估維度

「題目是否已解」與「有沒有獨立解出」必須分開；L4 品質與獨立性也不完全相同。

| Independence | 定義 |
|---|---|
| Independent | 遇到陌生題，未收到演算法 Hint，獨立完成正確 Code、複雜度與正確性說明。 |
| Minor Hint | 只需釐清需求、輕微提醒或反例，之後能自行完成。 |
| Major Hint | 面試官必須提供關鍵 Pattern、狀態表示、核心轉換或主要不變量才能繼續。 |
| Unsolved | 給予提示後，仍無法完成正確解法。 |
| In Progress | 尚未完成 Code／評估；不可冒充最後成績。 |

L4 Quality 獨立標記為 `Strong / Borderline / Weak / Not Assessed`。評分需要根據推理、正確性證明、複雜度、程式碼、溝通與測試等具體證據；這是**模擬面試評分**，不是 Google 官方規則，也不是錄取機率。

## 記錄規則

- 首次選題先檢查 GitHub Commit、`problems/`、`patterns/`、本目錄，以及最近對話的出題史。
- **相同題目至少間隔完整 7 天**；期間優先用相同弱點的不同變形進行練習。
- 當場不提前揭露 Pattern、不主動給 Hint；糾正錯誤時給具體 Counterexample。分清楚 Conceptual Gap 與 Implementation Slip。
- **解題結束才寫正式 Session Outcome。** 只有看到原始結果、提示程度與 Code 狀態，才決定 Independence；單純講出正確 Approach 不能標成 Independent AC。
- `Verified` 需要在新題／陌生變形上獨立完成。某題 AC 不代表整個 Pattern 所有變形都已熟練。
- 優先安排約 70% 尚未驗證的題型、30% 已知弱點的複習變形；依近期題目分布動態平衡，不必機械式每天符合比例。
- 追蹤 Invariant／Tie-breaking／Overflow／Boundary，也追蹤完整流程是否漏步，例如 BFS／DFS 的 Discover → Mark/Create → Enqueue/Push → Process。
- 每次 Session 完成後，如 GitHub 可寫入，將結果加入 `sessions.md`，同步更新 `coverage.md` 並 Commit。若 GitHub 不可用，先在對話中提供完整紀錄，清楚標示尚未寫入，不得聲稱已 Push。
- `problems/`、`patterns/` 繼續沿用既有格式；原始 AC Code 完整保留。

## 舊紀錄說明

初始條目只依可核實的 GitHub／近期對話內容回填。若缺少獨立寫 Code 的證據，狀態應寫 `Not Assessed` 或 `In Progress`，不能推測為 Independent。使用者後續提供更完整的過往資料時，可再更新。

**注意：** 此儲存庫目前可公開瀏覽；寫在這裡的練習紀錄可能被他人看到。若想保密，應改用 Private Repo。
