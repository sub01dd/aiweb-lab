# ハンバーガーメニュー実装の必須チェックリスト

スマホのハンバーガーメニュー（モバイル展開ナビ）を実装するとき、以下のバグが頻発します。**実装前に必ず読んで、すべての項目をクリアしてください。**

---

## 🔴 致命バグ：祖先要素の containing block 問題

**症状**：ナビに `position:fixed; inset:0` を指定しても、画面全体を覆わず**ヘッダーの高さ分しか表示されない**。下半分が透明で背景が見えてしまう。

**原因**：`backdrop-filter` / `filter` / `transform` / `perspective` / `will-change:transform` のいずれかが**祖先要素に指定されている**と、CSS仕様により新しい containing block が作られ、子要素の `position:fixed` は viewport ではなく **その祖先要素の bounding box が基準**になる。

**対処法（いずれか）**：
1. 祖先要素（特にヘッダー `.hdr`）から `backdrop-filter` / `transform` / `filter` を**削除**する。背景はsolidカラー or 半透明 background のみで表現。
2. ハンバーガーで展開するナビ要素を、ヘッダーの内側ではなく **`<body>` の直下に配置**する（DOM構造変更）。

```css
/* ❌ 罠：これがあると子の inset:0 が壊れる */
.hdr { backdrop-filter: blur(10px); }

/* ✅ 解決 */
.hdr { background:#f7f3ec; /* 不透明色で代替 */ }
```

---

## 🟡 z-index 競合

**症状**：ナビが展開されたが、他の sticky 要素（デモバナー / トップ通知バー / フローティングCTA）に上書きされて隠れる。

**対処**：プロジェクト内の全 fixed/sticky 要素の z-index を洗い出し、ナビに**それより高い値**を割り当てる。`z-index:90` 以上を目安に。

```css
/* 他の sticky 要素より明確に高く */
.nav { z-index:90; }
.burger { position:relative; z-index:95; } /* 展開後も×ボタンとして押せるように */
```

---

## 🟡 opacity アニメーションで透ける

**症状**：ナビ展開アニメーション中、`opacity:0 → 1` の transition で**背景が半透明になる瞬間**があり、背後のコンテンツが透けて違和感。

**対処**：opacity をやめて **transform のみで切替**。

```css
/* ❌ アニメ中に透ける */
.nav { transform:translateY(-110%); opacity:0; transition:transform .4s, opacity .3s; }
.nav.is-open { transform:none; opacity:1; }

/* ✅ 透けない */
.nav { transform:translateY(-110%); transition:transform .35s; }
.nav.is-open { transform:none; }
```

---

## 🟡 背景スクロールロック漏れ

**症状**：ナビ展開中に背後のページがスクロールできて、後ろのコンテンツがチラチラ動く違和感。

**対処**：JSで `body.style.overflow = 'hidden'` をトグル。

```js
const setOpen = (open) => {
  burger.classList.toggle('is-open', open);
  nav.classList.toggle('is-open', open);
  burger.setAttribute('aria-expanded', String(open));
  document.body.style.overflow = open ? 'hidden' : ''; // ←必須
};
```

---

## 🟡 背景透明（半透明color）で背後コンテンツが透ける

**症状**：ナビの background に `rgba(...,.96)` のような半透明色を指定。完全不透明ではないため、背景の太字や濃い色が透けて見える。

**対処**：完全不透明色を使う。`background: var(--c-paper)` のように CSS 変数経由だと未解決リスクもあるので、**直書き or 二重指定**で保険。

```css
.nav {
  background:#f7f3ec; /* 完全不透明 */
  /* または */
  background: var(--c-paper, #f7f3ec); /* fallback付き */
}
```

---

## 🟢 アクセシビリティ忘れ

- バーガーボタン：`aria-expanded="false"`（初期）→ JSでトグル
- バーガーボタン：`aria-controls="<nav id>"`、`aria-label="メニューを開く"`
- ナビ要素：`role="navigation"` または `<nav>` タグ、 `aria-label`
- ESCキーで閉じる：`document.addEventListener('keydown', e => { if(e.key==='Escape') setOpen(false); })`
- ナビ内のリンククリック時に自動的に閉じる：`nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)))`

---

## 🟢 タップ領域

- バーガー本体：最小 **44×44px**（Appleガイドライン）
- ナビ内リンク：縦 padding 14-18px 以上、`width:100%; text-align:center` で押しやすく

---

## 🟢 デザイン

- ナビが展開された状態が「上に浮いている層」と分かるように **`box-shadow:0 0 40px rgba(0,0,0,.18)`** を付ける
- ナビの padding-top はヘッダー高さ分（80-96px）確保して、上部に空白を作る
- `overflow-y:auto` でリンクが多い時にスクロール可能に

---

## 実装テンプレ（コピペOK）

```html
<header class="hdr">
  <div class="hdr-inner">
    <a href="#" class="brand">BRAND</a>
    <nav class="nav" id="nav" aria-label="メインナビ">
      <a href="#a">項目1</a>
      <a href="#b">項目2</a>
      <a href="#c">項目3</a>
    </nav>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="nav" aria-label="メニューを開く">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<script>
(() => {
  const burger = document.getElementById('burger');
  const nav = document.getElementById('nav');
  const setOpen = open => {
    burger.classList.toggle('is-open', open);
    nav.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  };
  burger.addEventListener('click', () => setOpen(!nav.classList.contains('is-open')));
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setOpen(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') setOpen(false); });
})();
</script>

<style>
/* ⚠️ .hdr に backdrop-filter / transform / filter を絶対に付けない */
.hdr { position:sticky; top:0; z-index:50; background:#fff; border-bottom:1px solid #e5e5e5; }
.hdr-inner { display:flex; align-items:center; justify-content:space-between; height:64px; padding:0 20px; }
.burger { display:none; width:44px; height:44px; position:relative; z-index:95; background:transparent; border:0; }
.burger span { display:block; width:22px; height:2px; background:#1a1a1a; margin:5px auto; transition:transform .25s, opacity .25s; }
.burger.is-open span:nth-child(1) { transform:translateY(7px) rotate(45deg); }
.burger.is-open span:nth-child(2) { opacity:0; }
.burger.is-open span:nth-child(3) { transform:translateY(-7px) rotate(-45deg); }

@media (max-width:900px) {
  .nav {
    position:fixed; inset:0; z-index:90;
    background:#fff; /* 完全不透明 */
    display:flex; flex-direction:column; align-items:stretch;
    padding:88px 24px 32px; overflow-y:auto;
    transform:translateY(-110%);
    transition:transform .35s ease;
    pointer-events:none;
    box-shadow:0 0 40px rgba(0,0,0,.18);
  }
  .nav.is-open { transform:none; pointer-events:auto; }
  .nav a { padding:18px 0; font-size:16px; border-bottom:1px solid #eee; text-align:left; }
  .burger { display:flex; flex-direction:column; }
}
</style>
```

---

## チェックリスト（実装後の自己確認）

- [ ] `.hdr` / 祖先要素に `backdrop-filter` / `transform` / `filter` / `perspective` / `will-change` が**ない**
- [ ] ナビ展開時、画面全体が完全不透明色で覆われ、背後のコンテンツが**1px も見えない**
- [ ] ナビの z-index が、プロジェクト内の他の sticky/fixed 要素より**確実に高い**
- [ ] アニメーションは `transform` のみで、`opacity` は使っていない
- [ ] ナビ展開中、`body.style.overflow = 'hidden'` で背後がスクロールできない
- [ ] バーガーは展開後も押せる位置・z-index で、×ボタンとして機能する
- [ ] `aria-expanded` / `aria-controls` / `aria-label` が設定済み
- [ ] ESCキーで閉じる、ナビ内リンクをクリックすると自動で閉じる
- [ ] バーガーが 44×44px 以上、ナビリンクの縦 padding が 14px 以上
