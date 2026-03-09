<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>ポケカ速報ラボ | 抽選・再販・予約を速く、正確に、見やすく</title>
<meta name="description" content="ポケモンカードの抽選販売、再販、予約、Amazon招待、楽天・Yahoo導線を見やすく整理する情報サイトテンプレート。" />
<link rel="stylesheet" href="style.css" />
<link rel="manifest" href="site.webmanifest" />

<meta property="og:title" content="ポケカ速報ラボ" />
<meta property="og:description" content="抽選・再販・予約を、速く、正確に、見やすく。" />
<meta property="og:type" content="website" />
<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"WebSite",
  "name":"ポケカ速報ラボ",
  "url":"https://YOUR-DOMAIN/"
}
</script>

</head>
<body>

<header class="hero">
  <div class="container">
    <p class="eyebrow">pokeka authority template</p>
    <h1>ポケカ速報ラボ</h1>
    <p class="lead">抽選・再販・予約を、速く、正確に、見やすく。ポケカ情報を整理し、見る人に「このサイトが一番分かる」と思ってもらうための構成に仕上げています。</p>
    <div class="hero-actions">
      <a class="btn primary" href="#latest">新着を見る</a>
      <a class="btn" href="#alerts">通知設定</a>
      <a class="btn" href="calendar.html">抽選カレンダー</a>
    </div>
  </div>
</header>

<nav class="topnav container">
  <a href="index.html">トップ</a>
  <a href="lotteries.html">抽選一覧</a>
  <a href="calendar.html">抽選カレンダー</a>
  <a href="resale.html">再販・予約</a>
  <a href="shops.html">ショップ一覧</a>
  <a href="guides/index.html">攻略ガイド</a>
  <a href="faq.html">FAQ</a>
  <a href="editorial-policy.html">編集方針</a>
  <a href="about.html">運営情報</a>
</nav>

<main class="container">
  <section class="grid-hero">
    <section class="card">
      <span class="kicker">更新時刻 <strong id="updatedAt">-</strong></span>
      <h2>監視サマリー</h2>
      <p>トップページは「新着の把握」と「抽選一覧の実用性」を両立させています。そこからカレンダー、ショップ一覧、ガイド記事へ自然に流せる導線にしています。</p>
      <div class="stats">
        <div class="stat"><div class="label">抽選件数</div><div class="value" id="statLottery">0</div></div>
        <div class="stat"><div class="label">受付中</div><div class="value" id="statOpen">0</div></div>
        <div class="stat"><div class="label">販売導線</div><div class="value" id="statCommerce">0</div></div>
        <div class="stat"><div class="label">X情報</div><div class="value" id="statSocial">0</div></div>
      </div>
      <div class="pill-row">
        <span class="pill">新着順</span>
        <span class="pill">締切カウントダウン</span>
        <span class="pill">ショップ別通知</span>
        <span class="pill">Amazon / 楽天 / Yahoo導線</span>
      </div>
    </section>
    <section class="card">
      <h2>収益導線</h2>
      <p class="small">Amazon・楽天・Yahooの導線はプレースホルダーです。自分のアフィリエイトURLに差し替えて使ってください。</p>
      <div class="hero-actions">
        <a id="amazonLink" class="btn" href="#" rel="nofollow sponsored" target="_blank">Amazon</a>
        <a id="rakutenLink" class="btn" href="#" rel="nofollow sponsored" target="_blank">楽天</a>
        <a id="yahooLink" class="btn" href="#" rel="nofollow sponsored" target="_blank">Yahoo</a>
      </div>
      <div class="notice" style="margin-top:14px">
        広告を入れる場合は、審査通過後にトップと記事ページの本文上部・下部に実装すると自然です。
      </div>
    </section>
  </section>

  <section class="card">
    <h2>絞り込み</h2>
    <div class="toolbar">
      <input id="searchBox" type="search" placeholder="ショップ名・商品名・状態で検索" />
      <select id="shopFilter"></select>
      <select id="statusFilter">
        <option value="">すべての状態</option>
        <option value="受付中">受付中</option>
        <option value="予告">予告</option>
        <option value="告知待ち">告知待ち</option>
      </select>
    </div>
  </section>

  <section id="alerts" class="card">
    <h2>通知設定</h2>
    <div class="settings-grid">
      <label><input type="checkbox" id="enableStartAlert" checked> 抽選開始アラート</label>
      <label><input type="checkbox" id="enableDeadlineAlert" checked> 締切前アラート</label>
      <label>締切前通知
        <select id="deadlineLead">
          <option value="24">24時間前</option>
          <option value="3">3時間前</option>
          <option value="1">1時間前</option>
        </select>
      </label>
    </div>
    <div id="shopToggles" class="toggle-grid"></div>
    <div class="hero-actions">
      <button id="notifyPermissionBtn" class="btn">通知を許可</button>
      <button id="saveSettingsBtn" class="btn primary">設定を保存</button>
    </div>
    <p class="small">この通知は、ブラウザでサイトを開いている間に動きます。</p>
  </section>

  <section id="latest" class="card">
    <h2>新着情報</h2>
    <div id="latestFeed" class="feed-list"></div>
  </section>

  <section class="grid-two">
    <section class="card">
      <h2>抽選一覧</h2>
      <table id="lotteryTable">
        <thead>
          <tr>
            <th>ショップ</th>
            <th>商品</th>
            <th>状態</th>
            <th>受付期間</th>
            <th>結果</th>
            <th>締切まで</th>
            <th>リンク</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </section>
    <section class="card">
      <h2>再販・予約導線</h2>
      <div id="commerceFeed" class="feed-list"></div>
    </section>
  </section>

  <section class="grid-three">
    <section class="card">
      <h2>X情報</h2>
      <div id="socialFeed" class="feed-list"></div>
    </section>
    <section class="card">
      <h2>ショップの見どころ</h2>
      <div id="shopFeed" class="feed-list"></div>
    </section>
    <section class="card">
      <h2>ガイド導線</h2>
      <div id="guideFeed" class="feed-list"></div>
    </section>
  </section>
</main>

<footer class="footer">
  <div class="container">
    <div class="footer-links">
      <a href="guides/index.html">ガイド一覧</a>
      <a href="faq.html">FAQ</a>
      <a href="editorial-policy.html">編集方針</a>
      <a href="privacy.html">プライバシーポリシー</a>
      <a href="contact.html">お問い合わせ</a>
    </div>
    <p>本サイトは公開情報の整理テンプレートです。最終確認は必ず各公式ページで行ってください。</p>
  </div>
</footer>

<script src="app.js"></script>
</body>
</html>