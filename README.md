# GG Li Learning Hub｜13 堂訓練課程目錄

這是一套可直接部署到 GitHub Pages 的靜態課程目錄網站。  
本版已更新為 06/09 至 09/01 共 13 堂正式課表，並保留 06/09 簡宏鈞處經理「目標設定、心態調整」與 06/23 李孟珊業務經理「富邦之星」互動筆記頁。

## 目前課程

| 日期 | 講師 | 職稱 | 主題 | 狀態 |
|---|---|---|---|---|
| 06/09 | 簡宏鈞 | 處經理 | 目標設定、心態調整 | 互動筆記完成 |
| 06/16 | 范毓斌 | 業務經理 | 銷售自我 | 已上課・待整理 |
| 06/23 | 李孟珊 | 業務經理 | 富邦之星 | 互動筆記完成 |
| 06/30 | 詹呂欣蓓 | 行銷襄理 | 社群開發 | 下一堂 |
| 07/07 | 陳昶宇 | 行銷襄理 | 九宮格（前） | 未開始 |
| 07/14 | 吳虹儀 | 行銷襄理 | 好感型客戶經營 | 未開始 |
| 07/21 | 王昱文 | 業務襄理 | 客戶開發 | 未開始 |
| 07/28 | 張恩煒 | 行銷襄理 | 故事行銷 | 未開始 |
| 08/04 | 周純伃 | 行銷經理 | 話題轉議題 | 未開始 |
| 08/11 | 鄭占禮 | 處經理 | 條款理賠 | 未開始 |
| 08/18 | 洪敬忠 | 分處經理 | 投資財富 | 未開始 |
| 08/25 | 鄭捷宇 | 業務經理 | 高資產客戶 | 未開始 |
| 09/01 | 趙家詡 | 行銷襄理 | 九宮格（後） | 未開始 |

## 檔案內容

```text
index.html
css/style.css
js/main.js
assets/brand-mark.svg
notes/goal-setting-0609/index.html
notes/fubon-star-0623/index.html
.nojekyll
README.md
```

## 怎麼改課程資料

打開 `js/main.js`，修改上方的 `courses` 陣列。

每一堂課長這樣：

```js
{
  no: 14,
  date: '09/08',
  month: '09',
  title: '新課程名稱',
  lecturer: '講師姓名',
  role: '職稱',
  status: 'planned',
  ability: 'social',
  url: '',
  desc: '這堂課要解決什麼問題',
  tags: ['標籤一', '標籤二']
}
```

## status 狀態

```text
ready    互動筆記完成，可以放筆記網址
done     已上課・待整理
next     下一堂
planned  未開始
```

如果互動筆記已經做好：

```js
status: 'ready',
url: 'notes/你的課程資料夾/index.html'
```

如果已經上課但還沒整理：

```js
status: 'done',
url: ''
```

## ability 能力分類

目前可用：

```text
mindset       目標與心態
selfbrand     銷售自我與故事
star          穩定績效系統
social        社群與開發
grid          九宮格與需求拆解
relationship  好感經營與議題轉換
claims        條款與理賠
wealth        投資財富與高資產
```

如果要新增能力分類，請修改 `js/main.js` 裡面的 `abilities` 物件。

## GitHub Pages 部署方式

1. 到 GitHub 建立新的 repository，例如 `tp799_learning_hub`
2. 把這包檔案全部上傳到 repo 根目錄
3. 進入 Settings → Pages
4. Source 選 `Deploy from a branch`
5. Branch 選 `main`，資料夾選 `/root`
6. 儲存後等待 GitHub 產生網址

網址會類似：

```text
https://你的帳號.github.io/tp799_learning_hub/
```

## 06/23 富邦之星互動筆記

本版已將 `06/23 李孟珊業務經理｜富邦之星` 整理成互動筆記頁：

- 課程章節重點
- 富邦之星行動自評
- 約訪主題與開場產生器
- 名單水池盤點
- 30 日行動計畫
- 課後測驗
- 主管複訓帶領流程

為避免內部資料外流，本壓縮檔不包含原始錄音與完整逐字稿，只保留整理後的課程頁面。


## 品牌更新

本版品牌已更新為 **GG Li Learning Hub**，首頁、內頁導覽列、README 與 favicon 皆已同步。
