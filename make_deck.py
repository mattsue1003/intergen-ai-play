# 由基隆 ICOPE 工作坊簡報（keelung-icope-ai/deck.html）組出「玩轉世代」新簡報
# python3 make_deck.py → deck.html，再 zsh build.sh → index.html
import re, html, pathlib
ROOT = pathlib.Path(__file__).parent
SRC = (ROOT.parent / "keelung-icope-ai" / "deck.html").read_text()
GH = "https://mattsue1003.github.io/"
DECK_URL = GH + "intergen-ai-play/"

head = SRC[:SRC.index("<!-- 1 封面 -->")]
tail = SRC[SRC.index("</div></main>"):]
old = {}
for m in re.finditer(r'(?:<!--[^\n]*-->\n)?<section class="slide[^"]*" data-title="([^"]+)">.*?</section>\n', SRC, re.S):
    old[m.group(1)] = m.group(0)

def keep(title, *subs):
    s = old[title]
    for a, b in subs:
        assert a in s, (title, a[:40])
        s = s.replace(a, b)
    return s

esc = html.escape

# ── 新元件 CSS ──
css = """
/* ── 教案範例卡（截圖＋QR） ── */
.exgrid{display:grid;grid-template-columns:repeat(var(--m,3),minmax(0,1fr));grid-auto-rows:minmax(0,1fr);gap:12px 14px;min-height:0;flex:1;max-height:560px}
.ex{display:flex;flex-direction:column;gap:6px;min-height:0;border:1px solid var(--line);border-radius:10px;padding:8px;background:var(--paper);text-decoration:none;color:var(--ink);transition:border-color .2s}
.ex:hover{border-color:var(--ink)}
.ex .ph{flex:1;min-height:60px;border-radius:6px;overflow:hidden;background:var(--soft)}
.ex .ph img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.ex .row{display:grid;grid-template-columns:minmax(0,1fr) 62px;gap:8px;align-items:center}
.ex b{display:block;font-size:15px;line-height:1.3}
.ex small{display:block;font-size:12.5px;color:var(--muted);line-height:1.4}
.ex .q{width:62px;height:62px;background:#fff;border-radius:4px}
.slide>.cols>.exgrid{display:grid;justify-content:stretch;gap:12px 14px}.slide>.cols>.typecol{justify-content:flex-start}
.exgrid.tight .ex .ph{display:none}.exgrid.tight{grid-auto-rows:auto;align-content:start}
.typecol{display:flex;flex-direction:column;gap:12px;min-width:0}
.keys{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.keys li{display:grid;grid-template-columns:24px 1fr;gap:10px;font-size:16px;line-height:1.5}
.keys li i{font-style:normal;width:24px;height:24px;border-radius:6px;background:var(--c);color:#fff;display:grid;place-items:center;font-family:var(--f-display);font-weight:900;font-size:12px;margin-top:2px}
.tools{display:flex;flex-wrap:wrap;gap:6px}.tools .tag{background:color-mix(in srgb,var(--c) 14%,var(--paper))}
.typeslide .prompt{font-size:14.5px;line-height:1.6}
/* 四大機制 */
.mech{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;flex:1;min-height:0;max-height:520px}
.mech .box{display:flex;flex-direction:column;gap:8px;padding:16px;border-top:6px solid var(--c)}
.mech h3{font-size:28px;color:var(--c)}
.mech p{font-size:16.5px;line-height:1.55}.mech .ig{border-top:1px dashed var(--line);padding-top:8px}.mech p b{color:var(--ink)}
.mech .say{margin-top:auto;font-size:15.5px!important;background:color-mix(in srgb,var(--c) 12%,var(--paper));border-radius:8px;padding:8px 10px;font-size:14.5px;font-weight:700}
/* 發展 */
.dev{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:22px;flex:1;min-height:0;max-height:540px}
.ladder{display:flex;flex-direction:column;gap:8px}
.ladder div{display:grid;grid-template-columns:42px 1fr;gap:12px;align-items:center;border:1px solid var(--line);border-radius:10px;padding:10px 14px;background:var(--paper)}
.ladder div i{font-style:normal;width:42px;height:42px;border-radius:10px;display:grid;place-items:center;font-family:var(--f-display);font-weight:900;color:#fff;background:var(--c)}
.ladder div b{font-size:17px}.ladder div small{display:block;color:var(--muted);font-size:13.5px;line-height:1.45}
.ladder div.mid{border:2px solid var(--ink)}
/* 七種教案總覽 */
.types7{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;flex:1;min-height:0;max-height:540px}
.t7{display:flex;flex-direction:column;gap:6px;padding:16px;border-radius:12px;background:color-mix(in srgb,var(--c) 10%,var(--paper));border:1px solid color-mix(in srgb,var(--c) 35%,var(--paper));text-decoration:none;color:var(--ink)}
.t7:hover{border-color:var(--ink)}
.t7 i{font-style:normal;font-family:var(--f-display);font-weight:900;font-size:28px;color:var(--c);line-height:1}
.t7 b{font-size:20px}.t7 small{font-size:14px;color:var(--muted);line-height:1.5}
.t7 .tag{align-self:flex-start;margin-top:auto;background:var(--paper)}
@media (max-width:900px){
  .exgrid{grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:auto;max-height:none}.ex .ph{flex:none;aspect-ratio:16/10}
  .mech,.types7{grid-template-columns:minmax(0,1fr);max-height:none}.dev{grid-template-columns:minmax(0,1fr);max-height:none}
}
@media (max-width:520px){.exgrid{grid-template-columns:minmax(0,1fr)}}
"""
head = head.replace("</style>", css + "</style>", 1)
head = head.replace("<title>基隆 ICOPE × AI 工作坊</title>", "<title>玩轉世代 AI 教案</title>")
head = head.replace('<b>ICOPE × AI</b><span>基隆 ICOPE 培力實務工作坊</span>', '<b>PLAY × AI</b><span>玩轉世代：AI 賦能幼老代間遊戲與創意教學設計</span>')
tail = tail.replace("icopeai-", "intergenai-")

TITLES = {}
for line in (pathlib.Path("/private/tmp/claude-501/-Users-matt-Claude---/da33c463-9979-426f-8d8d-ffdf16a5e4d3/scratchpad/titles.txt")).read_text().splitlines():
    a, b = line.split(" | ", 1); TITLES[a] = b

def ex(slug, title, desc, url=None):
    url = url or GH + slug + "/"
    q = "img/qr/" + slug.replace("/", "_") + ".svg"
    ph = "img/ex/" + slug.replace("/", "_") + ".jpg"
    return (f'<a class="ex" href="{esc(url)}" target="_blank" rel="noopener"><div class="ph"><img src="{ph}" alt="{esc(title)} 畫面" loading="lazy"></div>'
            f'<div class="row"><span><b>{esc(title)}</b><small>{esc(desc)}</small></span><img class="q" src="{q}" alt="{esc(title)} QR code"></div></a>')

QR_LIST = []
def exs(items, m=3, tight=False):
    for it in items: QR_LIST.append((it[0], it[3] if len(it) > 3 else GH + it[0] + "/"))
    cls = "exgrid tight" if tight else "exgrid"
    return f'<div class="{cls}" style="--m:{m}">' + "".join(ex(*it) for it in items) + "</div>"

def typeslide(no, color, title, h2, keys, tools, plab, ptext, items, m=3, note=None):
    k = "".join(f'<li><i>{i+1}</i><span>{t}</span></li>' for i, t in enumerate(keys))
    tl = "".join(f'<span class="tag">{t}</span>' for t in tools)
    nt = f'<div class="note" style="--c:{color}"><b>{note[0]}</b><span>{note[1]}</span></div>' if note else ""
    return f'''<section class="slide typeslide" data-title="{esc(title)}" style="--c:{color}">
  <div class="eyebrow" style="--c:{color}"><span class="sq"></span>教案設計 {no}</div>
  <h2>{h2}</h2>
  <div class="cols" style="--n:2;grid-template-columns:minmax(0,5fr) minmax(0,8fr)">
    <div class="typecol">
      <ul class="keys">{k}</ul>
      <div class="tools">{tl}</div>
      <div class="prompt"><div class="lab">{plab}<button class="copy">複製</button></div>{ptext}</div>
      {nt}
    </div>
    {exs(items, m)}
  </div>
</section>
'''

S = []  # 新簡報的頁

# 1 封面
S.append(f'''<!-- 1 封面 -->
<section class="slide cover" data-title="封面">
  <div class="confetti" aria-hidden="true">
    <i style="left:62%;top:7%;width:46px;height:46px;background:var(--blue)"></i>
    <i style="left:76%;top:12%;width:20px;height:20px;background:var(--lime);animation-delay:-2s"></i>
    <i style="left:92%;top:8%;width:30px;height:30px;background:var(--mag);animation-delay:-1s"></i>
    <i style="left:58%;top:52%;width:16px;height:16px;background:var(--mag);animation-delay:-2.5s"></i>
    <i style="left:62%;top:84%;width:56px;height:56px;background:var(--amber);animation-delay:-3s"></i>
    <i style="left:91%;top:84%;width:34px;height:34px;background:var(--sky);animation-delay:-1.5s"></i>
  </div>
  <div class="cover-grid">
  <div class="cover-main">
  <div class="eyebrow"><span class="sq"></span>家政群科中心 研習</div>
  <h1><span class="en">PLAY <b>×</b> AI</span>玩轉世代</h1>
  <p class="lede" style="font-size:24px;color:var(--ink);font-weight:900">AI 賦能幼老代間遊戲與創意教學設計</p>
  <p class="lede">一副 1–16 數字牌、一副撲克牌，就能玩出祖孫都能玩的遊戲。再用 Gemini、ChatGPT、OpenCode、Canva，把點子做成簡報、影片、音樂、動畫、紙本、桌遊與互動衛教七種教案。</p>
  <div class="meta">
    <div><small>日期</small><strong>11/15（日）</strong></div>
    <div><small>時間</small><strong>09:00–12:00</strong></div>
    <div><small>主辦</small><strong>家政群科中心</strong></div>
    <div><small>講師</small><strong>鍾孟修 職能治療師</strong></div>
  </div>
  </div>
  <div class="coverqrs">
  <div class="coverqr"><img src="img/qr-deck.svg" alt="掃描開啟本網頁型簡報"><span><b>帶走簡報</b>mattsue1003.github.io/intergen-ai-play</span></div>
  </div>
  </div>
</section>
''')

S.append(keep("講師介紹",
    ("<li>五股日間照顧中心及身障日間照顧中心（籌備中）</li>", "<li>五股日間照顧中心及身障日間照顧中心（115）</li>")))

S.append("@@AGENDA@@")

S.append('''<!-- 開始前 -->
<section class="slide" data-title="開始前的準備">
  <div class="eyebrow" style="--c:var(--lime)"><span class="sq"></span>開始前 5 分鐘</div>
  <h2>先把這五件事打勾</h2>
  <div class="cols" style="--n:2">
    <ul class="check" id="prep">
      <li><label><input type="checkbox" id="p1"><span><b>Chrome 登入自己的 Google 帳號</b><br><small class="muted">今天的 Gemini、YouTube、Google 表單都用這個帳號。</small></span></label></li>
      <li><label><input type="checkbox" id="p2"><span><b>登入 ChatGPT：chatgpt.com</b><br><small class="muted">做圖、學習單、桌遊卡牌、PPT 都會用到。</small></span></label></li>
      <li><label><input type="checkbox" id="p3"><span><b>打開 Gemini：gemini.google.com</b><br><small class="muted">做簡報遊戲、互動網頁、讀影片。</small></span></label></li>
      <li><label><input type="checkbox" id="p4"><span><b>登入 Canva：canva.com</b><br><small class="muted">魔法圖層改字改圖，學校帳號也可以。</small></span></label></li>
      <li><label><input type="checkbox" id="p5"><span><b>加入 LINE 學員社群</b><br><small class="muted">右下角綠色按鈕，範例與課後問題都在這裡。</small></span></label></li>
    </ul>
    <div style="display:flex;flex-direction:column;gap:14px;min-width:0">
      <div class="note" style="--c:var(--blue)"><b>語音輸入</b><span>Typeless 建議<b>裝在自己的桌機或筆電</b>，打字最省力；不能安裝的電腦，用 ChatGPT、Gemini 的麥克風也可以。</span></div>
      <div class="note"><b>操作方式</b><span>按 <span class="kbd">→</span> 下一頁、<span class="kbd">↓</span> 下一個步驟、<span class="kbd">T</span> 目錄、<span class="kbd">F</span> 全螢幕。截圖點一下可以放大，每張範例卡都能掃 QR。</span></div>
      <div class="note" style="--c:var(--mag)"><b>今天的原則</b><span>AI 做的是<b>草稿</b>。題目、規則、衛教內容，帶到長輩和孩子面前之前，自己先玩一次、看一次。</span></div>
      <div class="note" style="--c:var(--lime)"><b>範例都能帶走</b><span>所有範例教案都是免費網頁，手機掃 QR 就能打開，回去直接帶。</span></div>
    </div>
  </div>
</section>
''')

S.append(f'''<!-- 暖身成品 -->
<section class="slide" data-title="暖身：AI 做出的幼老教案">
  <div class="eyebrow" style="--c:var(--mag)"><span class="sq"></span>精選作品</div>
  <h2>這些祖孫都能玩的教案，都是用 AI 做的</h2>
  <p class="lede">沒有寫程式背景。今天的方法：講清楚玩法 → AI 做 → 自己試玩 → 上架成網址。</p>
  <div class="works">
    <a class="work" href="{GH}1-16-plus/" target="_blank" rel="noopener"><div class="ph"><img src="img/ex/1-16-plus.jpg" alt="1–16 數字卡加總挑戰" loading="lazy"></div><div class="t">1–16 數字卡加總挑戰</div><div class="k"><span>組合</span><span>投影</span></div></a>
    <a class="work" href="{GH}poker-icebreakers/" target="_blank" rel="noopener"><div class="ph"><img src="img/ex/poker-icebreakers.jpg" alt="撲克牌破冰" loading="lazy"></div><div class="t">撲克牌破冰 7 種玩法</div><div class="k"><span>動畫示範</span><span>抽籤器</span></div></a>
    <a class="work" href="{GH}order-different-slides/" target="_blank" rel="noopener"><div class="ph"><img src="img/ex/order-different-slides.jpg" alt="長者遊戲簡報生成器" loading="lazy"></div><div class="t">遊戲簡報生成器</div><div class="k"><span>8 種玩法</span><span>匯出 PPT</span></div></a>
    <a class="work" href="{GH}slide-game-video/" target="_blank" rel="noopener"><div class="ph"><img src="img/ex/slide-game-video.jpg" alt="簡報遊戲影片工坊" loading="lazy"></div><div class="t">簡報遊戲影片工坊</div><div class="k"><span>配樂音效</span><span>匯出 MP4</span></div></a>
    <a class="work" href="{GH}pop-song-guess/" target="_blank" rel="noopener"><div class="ph"><img src="img/ex/pop-song-guess.jpg" alt="台灣金曲猜歌" loading="lazy"></div><div class="t">台灣金曲猜歌</div><div class="k"><span>300 首</span><span>祖孫對唱</span></div></a>
    <a class="work" href="{GH}paper-cut-workshop/" target="_blank" rel="noopener"><div class="ph"><img src="img/ex/paper-cut-workshop.jpg" alt="對摺剪紙工坊" loading="lazy"></div><div class="t">對摺剪紙工坊</div><div class="k"><span>步驟動畫</span><span>A4 圖樣</span></div></a>
    <a class="work" href="{GH}nutrition-card-play/" target="_blank" rel="noopener"><div class="ph"><img src="img/ex/nutrition-card-play.jpg" alt="營養圖卡工坊" loading="lazy"></div><div class="t">營養圖卡工坊</div><div class="k"><span>桌遊卡牌</span><span>PDF／PPTX</span></div></a>
    <a class="work" href="{GH}emotion-bear-class/" target="_blank" rel="noopener"><div class="ph"><img src="img/ex/emotion-bear-class.jpg" alt="熊熊心情教室" loading="lazy"></div><div class="t">熊熊心情教室</div><div class="k"><span>幼兒情緒</span><span>互動課</span></div></a>
  </div>
</section>
''')

S.append('''<!-- AI 怎麼選 -->
<section class="slide" data-title="Gemini、ChatGPT、OpenCode 怎麼選">
  <div class="eyebrow" style="--c:var(--ink)"><span class="sq"></span>今天會用到的工具</div>
  <h2>Gemini、ChatGPT、OpenCode：做什麼教案，挑哪一個</h2>
  <div class="ai3">
    <div class="box ai" style="--c:var(--blue)"><div class="ai-h"><h3>Gemini</h3><span>gemini.google.com</span></div>
      <p class="ai-best">最適合：互動網頁、讀影片、做 PPT</p>
      <ul class="bio"><li>Canvas 做簡報遊戲、音樂互動、動畫網頁</li><li>讀 YouTube，找出可以停格提問的段落</li><li>「任務」模式做有插圖的 PPT</li></ul>
      <p class="ai3-today"><b>今天做</b>簡報遊戲、簡報影片、音樂互動、動畫、互動衛教簡報</p></div>
    <div class="box ai" style="--c:#10A37F"><div class="ai-h"><h3>ChatGPT</h3><span>chatgpt.com</span></div>
      <p class="ai-best">最適合：做圖、學習單、卡牌、出檔案</p>
      <ul class="bio"><li>參考喜歡的版面，畫學習單、海報、牌卡</li><li>直接產出 Word、PDF、PPT 下載</li><li>接 Canva 外掛，做好丟進 Canva 改</li></ul>
      <p class="ai3-today"><b>今天做</b>紙本教案、桌遊卡牌、工作模式做 PPT</p></div>
    <div class="box ai" style="--c:var(--ink)"><div class="ai-h"><h3>OpenCode</h3><span>opencode.ai</span></div>
      <p class="ai-best">最適合：一次做完一整包</p>
      <ul class="bio"><li>AI 代理人：自己建資料夾、寫檔案、開瀏覽器</li><li>做 Google 報名表、回饋單</li><li>蒐集資料、整理教案資料夾</li></ul>
      <p class="ai3-today"><b>今天做</b>選模型、做表單、整理資料夾、蒐集資料</p></div>
  </div>
  <div class="note" style="--c:var(--amber)"><b>再加一個 Canva</b><span>AI 做的圖，字常常改不了。Canva「魔法圖層」把字和圖拆開，改成自己的內容。三家 AI 都會出錯：規則、數字、衛教說法，帶活動前自己核對。</span></div>
</section>
''')

# 語音
S.append(keep("實作① 語音輸入",
    ("評估完，用講的把紀錄打完", "想到教案點子，用講的就打完"),
    ('<b>下載 Typeless</b><p>官網 typeless.com 下載安裝，用 Google 帳號登入；電腦與手機同一個帳號，個人字典會同步。</p>',
     '<b>下載 Typeless：建議裝在桌機</b><p>官網 typeless.com 下載安裝，用 Google 帳號登入。<b>桌機、筆電體驗最好</b>：任何輸入框（Gemini、ChatGPT、Canva、Word）都能直接講。手機同帳號，個人字典會同步。</p>'),
    ("教室電腦不能裝軟體：Windows 按 <span class=\"kbd\">Win</span>＋<span class=\"kbd\">H</span> 用內建聽寫。", "不能裝軟體的電腦：Windows 按 <span class=\"kbd\">Win</span>＋<span class=\"kbd\">H</span> 用內建聽寫。"),
    ('<b>ICOPE 情境：口述評估結果</b><p>走回辦公室的路上，用手機口述剛剛的評估（用代號），回座把文字貼給 Gemini，加上下方提示詞。</p>',
     '<b>教案情境：把點子講出來</b><p>帶完活動、在車上想到新玩法，直接口述：對象、道具、怎麼玩、怎麼變難。回座把文字貼給 Gemini，加上下方提示詞。</p>'),
    ("data-cap=\"口述完，貼上下方提示詞，整理成評估紀錄\"", "data-cap=\"口述完，貼上下方提示詞，整理成一份教案\""),
    ('''提示詞・口述變評估紀錄<button class="copy">複製</button></div>以下是我剛完成的 ICOPE 評估口述內容，請整理成：
1. 個案代號／性別年齡層
2. 六力結果表（認知、行動、營養、視力、聽力、情緒：正常或異常）
3. 異常項目的衛教重點與轉介建議
4. 下次追蹤方式與時間
不確定的地方用【？】標出，不要加入我沒說的內容。
口述內容：（貼上）''',
     '''提示詞・口述點子變教案<button class="copy">複製</button></div>以下是我用語音口述的活動點子，請整理成一份代間（祖孫）活動教案：
1. 活動名稱、對象（長輩與孩子年齡）、人數、時間
2. 道具清單
3. 玩法步驟（一步一句）
4. 變簡單／變難的方法各 2 個
5. 帶領時可以說的話
不確定的地方用【？】標出，不要加入我沒說的內容。
口述內容：（貼上）''')))

S.append(keep("實作① 不用安裝：ChatGPT、Gemini 的麥克風",
    ("瀏覽器跳出詢問就按「允許」。教室電腦沒有麥克風，請用自己的手機 App 練習。", "瀏覽器跳出詢問就按「允許」。電腦沒有麥克風，就用手機 App 練習。")))
S.append(keep("語音轉文字設定成繁體中文"))

# Chrome
S.append(keep("實作② Chrome 問問 Gemini",
    ('實作②　讀資料</div>\n  <h2>WHO 手冊 168 頁，請 Chrome 幫你讀</h2>', '實作②　Chrome 的應用</div>\n  <h2>長文件、網頁、影片，請 Chrome 的 Gemini 幫你讀</h2>'),
    ('<b>打開 WHO ICOPE 官方頁</b><p>按 Download PDF，用 Chrome 直接開啟（不必存檔）。資料來源是官方原文，AI 的回答才有根據。</p>',
     '<b>先打開你要讀的資料</b><p>課綱、研究報告 PDF、活動網頁、YouTube 影片都可以。用 Chrome 直接開啟，AI 讀的是官方原文，回答才有根據。（截圖示範：WHO 長者照護手冊）</p>'),
    ('<b>問「這一份」的內容</b><p>貼上下方提示詞。它讀的是你正在看的這份 PDF，回答會附頁碼，點開核對。</p>',
     '<b>問「這一份」的內容</b><p>貼上下方提示詞，請它把資料變成活動點子。回答會附頁碼，點開核對。</p>'),
    ('打開影片（例：Lancet 失智照護），問「重點整理，附時間碼」。只看重點片段，備課快很多。', '打開影片，問「重點整理，附時間碼」。挑出可以停格提問的片段，就是簡報影片教案的素材。'),
    ('''提示詞・讀手冊<button class="copy">複製</button></div>請只根據這份文件回答：
1. 用 10 點整理 ICOPE 的核心流程，每點標出頁碼
2. 做一張表：六力｜篩檢題目｜異常判定｜下一步評估或轉介
文件沒有提到的，請寫「文件未提及」。''',
     '''提示詞・資料變活動點子<button class="copy">複製</button></div>請只根據這份資料回答：
1. 用 5 點整理重點，每點標出頁碼或時間碼
2. 把這些重點變成 3 個祖孫可以一起玩的小活動（道具、玩法、帶領說法）
資料沒有提到的，請寫「資料未提及」。''')))

S.append(keep("實作② 讀影片：YouTube 摘要、Gemini 與 ChatGPT",
    ("實作②　讀影片</div>", "實作②　讀影片：簡報影片教案的第一步</div>"),
    ('<b>Gemini：貼影片網址就能讀</b><p>六力逐項整理，每項附時間碼。Flash 轉圈太久時，改用「深度研究（Pro）」重問一次。</p>',
     '<b>Gemini：貼影片網址就能讀</b><p>逐段整理、每段附時間碼（示範影片是長者量六力）。Flash 轉圈太久時，改用 Pro 模型重問一次。</p>'),
    ("實測三支台灣 ICOPE 影片都有（Premium 帳號）。沒按鈕就把網址丟給 Gemini。", "實測三支台灣衛教影片都有（Premium 帳號）。沒按鈕就把網址丟給 Gemini。")))

# ── 遊戲化教學原則 ──
S.append('''<!-- 遊戲化：發展 -->
<section class="slide" data-title="遊戲化原則：從發展看幼老">
  <div class="eyebrow" style="--c:var(--green)"><span class="sq"></span>遊戲化教學原則①</div>
  <h2>孩子的遊戲能力往上長，長輩的往下退：代間遊戲挑「中間那層」</h2>
  <div class="dev">
    <div class="ladder" style="--c:var(--sky)">
      <p class="muted" style="font-weight:700">遊戲能力的階梯（孩子由下往上長，長輩失能時由上往下退）</p>
      <div style="--c:var(--mag)"><i>4</i><span><b>自主、複雜規則</b><small>策略、計分、輪流出題。樂齡、能力好的長輩；國小以上孩子</small></span></div>
      <div class="mid" style="--c:var(--amber)"><i>3</i><span><b>簡單規則</b><small>一句話講得完的規則：「湊到 10 就拿走」。主活動</small></span></div>
      <div class="mid" style="--c:var(--green)"><i>2</i><span><b>配對、分類</b><small>找一樣的、分顏色、排大小。入門引導，3 歲孩子到認知退化長輩都能玩</small></span></div>
      <div style="--c:var(--blue)"><i>1</i><span><b>感覺、動作</b><small>摸、拍、丟、搶。破冰暖身，所有人都能參與</small></span></div>
    </div>
    <div style="display:flex;flex-direction:column;gap:12px;min-width:0">
      <div class="box"><h3 style="color:var(--green)">代間遊戲怎麼設計</h3>
        <ul class="bio" style="margin-top:8px;font-size:16px;gap:8px">
          <li><b>從第 1、2 層開始</b>：祖孫一起破冰，誰都不會輸</li>
          <li><b>主活動放第 3 層</b>：規則一句話，孩子懂、長輩也懂</li>
          <li><b>角色互換</b>：孩子當出題老師，長輩當示範的師傅</li>
          <li><b>同一副道具分級</b>：孩子玩難的版本、長輩玩簡單的版本，同一桌一起玩</li>
        </ul></div>
      <div class="cols" style="--n:2;gap:12px">
        <div class="box fill"><b>深度運作（專注式）</b><p class="muted" style="font-size:14.5px;margin-top:4px">理解規則、做判斷、從錯誤修正。1–16 排序、湊 10。最累，一次 5–10 分鐘。</p></div>
        <div class="box fill"><b>連結已知（發散式）</b><p class="muted" style="font-size:14.5px;margin-top:4px">接到本來就會的事：老歌、童玩、拿手菜。請長輩教孩子，最有成就感。</p></div>
      </div>
      <div class="note" style="--c:var(--green)"><b>帶法</b><span>連結已知暖場 → 深度運作挑戰 5–10 分鐘 → 回到連結已知收尾。</span></div>
    </div>
  </div>
</section>
''')

def mech(color, name, how, easy, hard, say, ig=""):
    return f'<div class="box" style="--c:{color}"><h3>{name}</h3><p><b>做法</b>　{how}</p><p><b>變簡單</b>　{easy}</p><p><b>變難</b>　{hard}</p><p class="ig"><b>代間版</b>　{ig}</p><p class="say">「{say}」</p></div>'

S.append(f'''<!-- 1-16 四大機制 -->
<section class="slide" data-title="遊戲化原則：1–16 數字牌四大機制">
  <div class="eyebrow" style="--c:var(--green)"><span class="sq"></span>遊戲化教學原則②　一副 1–16 數字牌</div>
  <h2>四大認知遊戲機制：配對、組合、排序、線索</h2>
  <p class="lede">4×4 的 1–16 數字牌，每個機制玩 2–3 分鐘；同一副牌分難易，祖孫同一桌玩。</p>
  <div class="mech">
    {mech("var(--mag)","配對","桌上排 4 張，你拿 1 張，請他找一樣的。","只放 2 張選。","找「比它大 1」的。","我這張是 7，你那邊有沒有？", "孫子出牌、阿嬤找；再交換。")}
    {mech("var(--amber)","組合","兩張牌加起來等於 10。","只用 1–9，先示範一組。","口字型每邊 3 張，加起來一樣大。","哪兩張湊起來是 10？", "孩子算加法、長輩當檢查員。")}
    {mech("var(--blue)","排序","1–8 打亂，從小排到大。","只用 1–5。","1–16、倒著排，或只排單數。","幫我排好，我找不到 6。", "長輩排 1–8、孩子排 1–16，比誰先好。")}
    {mech("var(--green)","線索","蓋 3 張，你給提示「比 10 大、是雙數」，他來猜。","牌面朝上，只給一個提示。","兩個以上提示，或換他出題考你。","猜猜我藏了哪一張？", "孩子出提示、阿公來猜。")}
  </div>
  <div class="note" style="--c:var(--green)"><b>遊戲化四原則</b><span>一次 5–10 分鐘｜牌從少開始｜答錯不糾正，陪他再找一次｜最後一題讓他成功。</span></div>
</section>
''')

S.append(f'''<!-- 1-16 教案連結 -->
<section class="slide" data-title="1–16 數字牌教案範例">
  <div class="eyebrow" style="--c:var(--green)"><span class="sq"></span>遊戲化教學原則②　1–16 教案範例</div>
  <h2>1–16 數字牌，玩出多元花樣：投影版、紙本版、摺紙版</h2>
  {exs([
    ("1-16-plus","1–16 數字卡加總挑戰","組合：口字型每條線加起來一樣，投影全班算"),
    ("1-16number","數字排列挑戰產生器","排序：產生排列題卡，列印給每桌"),
    ("3x3numberg","數字推理大偵探（投影版）","組合：九宮格橫直加總一樣，大螢幕出題"),
    ("3x3number","數字推理大偵探（紙本版）","組合：列印桌遊版，每桌一份"),
    ("number-slot","1~16 算術密碼抽籤器","組合／線索：拉霸抽數字，哪兩張湊得出來"),
    ("samenumber","數字矩陣尋寶","配對：數字矩陣找一樣的"),
    ("fold-4x4-game","16 格數字摺紙挑戰","4×4 紙格摺出指定數字，練空間"),
    ("random","數字多型態抽籤器","1–16 抽籤、算式、找缺少，全螢幕投影"),
  ], m=4)}
</section>
''')

S.append(f'''<!-- 撲克 四大機制 -->
<section class="slide" data-title="遊戲化原則：撲克牌四大機制">
  <div class="eyebrow" style="--c:var(--green)"><span class="sq"></span>遊戲化教學原則③　一副撲克牌</div>
  <h2>家裡都有的撲克牌：同樣四個機制，換個道具再玩一輪</h2>
  <div class="mech">
    {mech("var(--mag)","配對","翻開 6 張，找數字一樣的兩張湊一對。","只分紅色、黑色。","牌蓋著翻，記位置找一對。","這張 5 的好朋友在哪裡？", "祖孫同一隊翻牌，一人記左邊、一人記右邊。")}
    {mech("var(--amber)","組合","兩張加起來等於 10（A 當 1，人頭牌先拿掉）。","只用 A–5，湊 6。","三張湊 15。","7 要配哪一張才是 10？", "長輩湊 10、孩子湊 15，同一桌一起玩。")}
    {mech("var(--blue)","排序","同一花色 A–10 打亂，從小排到大。","只用 A–5。","抽掉一張，問少了哪一張。","幫我排好，我老是亂掉。", "長輩排一個花色、孩子排兩個花色。")}
    {mech("var(--green)","線索","你心裡想一張牌，他用是非題問：「紅色嗎？比 5 大嗎？」","桌上只留 4 張讓他猜。","換他想、你來問。","我心裡想一張，你問我。", "孩子想牌、阿嬤問，看幾題猜到。")}
  </div>
  <div class="note" style="--c:var(--green)"><b>帶法</b><span>不說「我們來上課」，說「陪我玩一下牌」｜輸贏不重要，讓他多贏幾次｜長輩當師傅、孩子當出題老師。</span></div>
</section>
''')

S.append(f'''<!-- 撲克 教案連結 -->
<section class="slide" data-title="撲克牌教案範例">
  <div class="eyebrow" style="--c:var(--green)"><span class="sq"></span>遊戲化教學原則③　撲克牌教案範例</div>
  <h2>一副撲克牌玩到底：破冰、資料庫、桌遊產生器</h2>
  {exs([
    ("poker-icebreakers","撲克牌破冰 7 種玩法","四人輪流的動畫示範，看動畫就會玩"),
    ("card-games-108","一副牌玩到底","撲克牌破冰＋108 張手繪卡牌遊戲簡報"),
    ("poker-database","撲克牌玩法大全","70 種玩法，文字＋影片教學"),
    ("poker-dice-game","牌與骰・玩法教案資料庫","只要撲克牌或骰子就能玩"),
    ("boardgame1-13","1–13 邏輯解碼大師","線索：依提示推理藏起來的牌"),
    ("pokerrandom","撲克牌拉霸抽籤器","抽牌決定題目或動作"),
  ], m=3)}
</section>
''')

S.append("@@TYPES7@@")

S.append(typeslide("①", "var(--mag)", "教案設計① 簡報遊戲", "簡報遊戲：投影出來，全場一起搶答、一起動",
    ["<b>一頁一題</b>：題目大、選項少，祖孫一眼看懂", "<b>加動作</b>：答案用拍手、舉手、踏步回答，變體智遊戲", "<b>能匯出 PPT</b>：沒網路也能帶，字可以自己改"],
    ["Gemini Canvas", "Gemini 任務做 PPT", "ChatGPT 工作模式"],
    "提示詞・簡報遊戲", "幫我做一個「找不同」簡報遊戲網頁，給祖孫一起玩：每頁 4 張動物圖，其中 1 張不一樣，按空白鍵翻下一題，答案出現時有音效。共 10 題，前 5 題簡單、後 5 題變難。字要大，繁體中文。",
    [("order-different-slides","長者遊戲簡報生成器","8 種玩法：規律接龍、找不同、數一數"),
     ("dobble-presentation-generator","找一樣簡報生成器","上傳自己的主題圖片做題目"),
     ("judgment-ppt-game","分一分 動一動","分類反應：看到就做動作"),
     ("dance-game-slides","九宮格跳舞機","跟著格子踩，簡報版跳舞機"),
     ("arrow-slides-arm-leg","手忙腳亂","箭頭方向＋左右手腳反應"),
     ("3x3shapecolorg","九宮格形色排排樂","大螢幕出題，團體同樂")], note=("代間玩法","孫子按下一題、阿公阿嬤搶答；或分祖孫兩隊，答對的人帶大家做一個動作。")))

S.append(keep("實作④ 做互動網頁",
    ('實作④　做互動網頁</div>\n  <h2>同一招做互動網頁：團康用的「六力小問答」</h2>', '教案設計①　實作：Gemini Canvas</div>\n  <h2>Gemini Canvas：講清楚玩法，兩分鐘做出搶答遊戲</h2>'),
    ("給誰用（社區長輩團康）、內容（六力各 2 題）、互動（大按鈕、煙火、兩組計分）、外觀（大字、溫暖配色）", "給誰用（祖孫一起玩）、內容（題目與題數）、互動（大按鈕、煙火、兩組計分）、外觀（大字、溫暖配色）"),
    ("投影到電視就能帶團康。", "投影到電視就能帶活動。"),
    ('''提示詞・團康互動網頁<button class="copy">複製</button></div>幫我做一個互動網頁：「ICOPE 六力小問答」，給社區長輩團康用。認知、行動、營養、視力、聽力、情緒各 2 題是非題，大字、大按鈕，答對會放煙火並顯示一句衛教重點，可分兩組計分。繁體中文，溫暖配色。''',
     '''提示詞・祖孫搶答網頁<button class="copy">複製</button></div>幫我做一個互動網頁：「阿公阿嬤的童年 vs 我的童年」搶答遊戲，給祖孫一起玩。10 題二選一（例：小時候玩彈珠還是玩平板？），大字、大按鈕，答完顯示一句「請阿公阿嬤分享當年」的提問，可分祖孫兩隊計分，答對放煙火。繁體中文，溫暖配色。''')))

S.append(typeslide("②", "var(--blue)", "教案設計② 簡報影片", "簡報影片：一段影片、一個問題，看完就聊",
    ["<b>影片切段</b>：每段 1–3 分鐘，停格就提問", "<b>先找段落</b>：YouTube 提問／Gemini 讀影片，拿到時間碼", "<b>簡報遊戲變影片</b>：加配樂音效匯出 MP4，沒有老師也能播"],
    ["YouTube 提問", "Gemini 讀影片", "簡報遊戲影片工坊"],
    "提示詞・影片變停格提問教案", "這是一支（主題）影片：（貼網址）。請幫我切成 4–6 段，每段寫：時間碼、這段在講什麼、停格時問祖孫的 2 個問題（一題給孩子、一題給長輩），最後設計一個 5 分鐘的動手活動。只根據影片內容，看不到的寫「影片未提及」。",
    [("slide-game-video","簡報遊戲影片工坊","圖文配對、相反動作，加音樂匯出 MP4"),
     ("cinema-teaching-method","感動短片・帶領資料庫","17 部可討論的短片＋引導流程"),
     ("god-eye-lessons","守護家人・上帝之眼","看一段影片、做一段作品"),
     ("kokedama-lessons","苔玉（水苔球）","園藝手作，影片段落帶領"),
     ("functional-training-lesson","站起來才算數","衛教動畫分 7 段＋互動問答"),
     ("cholesterol-video-lesson","膽固醇影片互動課","9:16 影片分段＋行動卡")], note=("代間玩法","停格時先問孩子「你看到什麼」，再問長輩「你們以前也這樣嗎」，讓兩代對話。")))

S.append(typeslide("③", "var(--amber)", "教案設計③ 音樂互動", "音樂互動：老歌連結長輩、節奏帶動孩子",
    ["<b>連結已知</b>：長輩年輕時的歌，一聽就打開話匣子", "<b>跟著拍子</b>：念字、拍手、踏步，節奏就是遊戲規則", "<b>祖孫對唱</b>：阿嬤唱老歌、孫子唱兒歌，互相猜歌名"],
    ["Gemini Canvas", "YouTube 律動影片", "ChatGPT 出題"],
    "提示詞・節奏遊戲網頁", "幫我做一個節奏遊戲網頁：畫面中央每拍出現一個圖片（蘋果、香蕉、西瓜、葡萄），跟著 90 BPM 的節拍器一起唸出名稱。可以調整速度（60–120 BPM）與每輪拍數，有開始／暫停大按鈕，可全螢幕投影。繁體中文，字要大。",
    [("pop-song-guess","台灣金曲猜歌","15 組 300 首，國語台語都有"),
     ("beatgame2","節奏唸字遊戲","跟著拍子唸出圖片名稱，可自己 DIY"),
     ("rhythmexercise","長輩律動產生器","設定 BPM，畫面出動作口令"),
     ("oldsongdance","音樂律動影片資料庫","378 支徒手律動，坐姿站姿"),
     ("song-lyrics-guess","看歌詞猜老歌","懷舊金曲 20 首"),
     ("oldsongdata","長者回憶高峰金曲 200","依年代找長輩年輕時的歌")], note=("代間玩法","阿嬤唱一句老歌、孫子接一句兒歌；節奏遊戲請孩子當指揮。")))

S.append(typeslide("④", "var(--sky)", "教案設計④ 動畫", "動畫教案：步驟一步一步動給你看",
    ["<b>手作步驟動畫</b>：剪紙、繞線、畫畫，比看照片好懂", "<b>反應動畫</b>：看到相反詞、指令就做動作", "<b>可調速度</b>：長輩慢一點、孩子快一點，同一個畫面"],
    ["Gemini Canvas", "OpenCode 做一整套", "ChatGPT 畫步驟圖"],
    "提示詞・步驟動畫網頁", "幫我做一個步驟動畫網頁：「對摺剪一顆愛心」，共 5 步（對摺、畫半邊、沿線剪、打開、裝飾）。每一步用 SVG 動畫畫出紙張和剪刀的動作，下方一行大字說明，有上一步／下一步／重播按鈕與速度調整。繁體中文。",
    [("contrast-animation","相反詞動畫訓練","設定節奏與程度，全螢幕帶團"),
     ("cogniciseanimation","群體節奏自訂指令訓練器","自訂指令，跟著節奏做"),
     ("visual234","視力活動檢測動畫","張大眼睛一起玩"),
     ("paper-cut-workshop","對摺剪紙工坊","16 課剪紙步驟動畫＋A4 圖樣"),
     ("mandala-lessons","曼陀羅一圈一圈畫","24 課步驟動畫＋學習單"),
     ("gods-eye-weaving","上帝之眼編織","3D 繞線動畫 24 步")], note=("代間玩法","孩子看動畫當小老師，一步一步教阿公阿嬤做；做完交換作品。")))

S.append(typeslide("⑤", "var(--lime)", "教案設計⑤ 紙本", "紙本教案：印出來就能玩，回家還能繼續",
    ["<b>產生器</b>：一鍵換題目，每桌拿到不一樣的", "<b>分級</b>：同一張學習單出簡單版、挑戰版", "<b>參考版面</b>：找喜歡的學習單截圖給 AI，做出同風格"],
    ["ChatGPT 做學習單", "Canva 魔法圖層", "Gemini 建立圖像"],
    "提示詞・祖孫學習單", "幫我做一張 A4 直式學習單「祖孫連連看：童玩今昔」：左邊 6 個古早童玩（陀螺、彈珠、跳房子、竹蜻蜓、尪仔標、扯鈴），右邊 6 個現在的玩具，請孩子和阿公阿嬤一起連出「玩法很像」的配對。下方留兩行「阿公阿嬤小時候怎麼玩？」給孩子記錄。字要大，繁體中文，線條清楚好列印。",
    [("cognitive-playbook-generator","認知手冊生成器","7–28 天動腦手冊，每天一頁"),
     ("dot-copy-drawing","點格仿畫・運筆練習","333 題 A4 紙本"),
     ("dot-to-dot-lessons","連點成畫","24 課連連看動畫＋學習單"),
     ("new-bingo-generator","賓果生成器","骰子賓果、主題賓果卡"),
     ("tangle-steps","纏繞畫步驟示範","13 種圖樣一筆一筆畫"),
     ("fold-4x4-game","16 格數字摺紙","4×4 紙格摺出指定數字")],
    note=("代間玩法","同一張學習單出祖孫兩個難度。接下來 4 頁：參考風格做學習單、Canva 改字、Gemini 免費做圖。")))

S.append(keep("方法：參考別人的 UI 風格",
    ("今天做圖、做網頁的共同方法", "教案設計⑤⑦　做圖、做網頁的共同方法")))
S.append(keep("實作③ ChatGPT 參考風格做衛教圖",
    ("實作③　做衛教圖：ChatGPT</div>\n  <h2>拿一張喜歡的衛教海報當參考，做出同風格的 ICOPE 海報</h2>", "教案設計⑤　紙本：ChatGPT 參考風格</div>\n  <h2>拿一張喜歡的海報當參考，做出同風格的學習單、海報</h2>"),
    ('<b>檢查成品</b><p>版面跟參考海報一樣好讀，內容換成「篩檢→複評→轉介」。逐字看：錯字、數字、醫療說法。</p>', '<b>檢查成品</b><p>版面跟參考海報一樣好讀，內容換成自己的（示範主題：長者量六力）。逐字看：錯字、數字、說法。</p>'),
    ('''請參考這張海報的 UI 設計（右側直排大標題、粉彩粉橘配淡藍、手繪線條人物、彩色小標籤標題、左下圓角「溫馨提醒」框），只參考版面與配色，不要複製它的文字、QR code 和標誌。幫我做一張 A4 直式衛教海報：右側直排標題「長者量六力 從篩檢到轉介」，副標「家屬指南」。三個標籤段落：篩檢：65 歲以上每年量一次六力；複評：有一項異常，由醫事人員再仔細評估；轉介：依結果連結復能、營養、眼科或耳鼻喉科。溫馨提醒：按時篩檢，及早發現、及早介入。繁體中文、字要大、不要錯字。''',
     '''請參考這張海報的 UI 設計（右側直排大標題、粉彩粉橘配淡藍、手繪線條人物、彩色小標籤標題、左下圓角「溫馨提醒」框），只參考版面與配色，不要複製它的文字、QR code 和標誌。幫我做一張 A4 直式活動海報：右側直排標題「祖孫遊戲日」，副標「一副牌玩一下午」。三個標籤段落：配對：找出一樣的牌；組合：兩張湊成 10；排序：從小排到大。溫馨提醒：輸贏不重要，一起笑最重要。繁體中文、字要大、不要錯字。''')))
S.append(keep("實作③ Canva 魔法圖層改字改圖",
    ("實作③　Canva 魔法圖層</div>", "教案設計⑤　Canva 魔法圖層</div>")))
S.append(keep("實作③ 免費版：Gemini 建立圖像",
    ("實作③　免費替代：Gemini</div>", "教案設計⑤　免費替代：Gemini</div>"),
    ('<b>先備好正確內容</b><p>到國健署「健康九九＋」衛教資源搜尋 ICOPE 聽力篇，挑出 6 個重點。AI 負責畫，內容由你決定。</p>', '<b>先備好正確內容</b><p>衛教圖先到國健署「健康九九＋」找正確資料，挑出 6 個重點（示範：聽力保健）。AI 負責畫，內容由你決定。</p>')))

S.append(typeslide("⑥", "var(--green)", "教案設計⑥ 桌遊卡牌", "桌遊卡牌：自己的主題，做成一副牌",
    ["<b>一套牌、多種玩法</b>：配對、記憶翻牌、湊數、搶答都用同一副", "<b>正反面</b>：正面圖、背面字，孩子看圖、長輩讀字", "<b>真實尺寸列印</b>：A4 每頁 4／6 張，有牌背、裁切線"],
    ["ChatGPT 畫卡圖", "Gemini Canvas 做產生器", "OpenCode 批次產生"],
    "提示詞・桌遊卡牌產生器", "幫我做一個卡牌產生器網頁：主題「台灣水果」，20 張卡，正面是水果圖、背面是名稱與一句冷知識。可以選 A4 每頁 4 張或 6 張，有裁切線、統一的牌背，按鈕下載 PDF。下方附 3 種玩法說明（配對、記憶翻牌、誰先湊到 3 種顏色）。繁體中文。",
    [("nutrition-card-play","營養圖卡工坊","自己的主題做卡牌，PDF／可改字 PPTX"),
     ("card-games-108","108 張手繪卡牌遊戲","形色棋、拉密、數字撞鐘"),
     ("poker-icebreakers","撲克牌破冰 7 種玩法","動畫示範＋現場抽籤器"),
     ("colored-paper-board-game","雙色摺色塊","依題目摺出指定色塊"),
     ("boardgame1-13","1–13 邏輯解碼大師","列印桌遊版產生器"),
     ("cardssame","圖卡配對拉霸機","上傳自己的圖卡做配對")], note=("代間玩法","孩子負責洗牌、發牌，長輩負責讀卡上的字；記憶翻牌時祖孫同一隊。")))

S.append(typeslide("⑦", "var(--mag)", "教案設計⑦ 主題式衛教", "主題式衛教：多互動問答的網頁型簡報",
    ["<b>每 3 頁一個互動</b>：猜猜看、選選看、動一動，不讓人只是聽", "<b>一個主題講透</b>：護眼、血壓、手指操、情緒", "<b>手機也能看</b>：投影上課，課後掃 QR 自己複習"],
    ["Gemini Canvas", "參考設計做網頁簡報", "GitHub Pages 上架"],
    "提示詞・互動衛教簡報", "參考這兩張網站截圖的設計風格，幫我做一份 12 頁的互動網頁型簡報「保護眼睛，祖孫一起來」：每 3 頁穿插一個互動（二選一搶答、找不同、跟著做眼睛運動 30 秒倒數），左右鍵換頁，上方頁碼與進度條，最後一頁是回家任務卡。字要大，繁體中文，不要用截圖裡的人和商標。",
    [("eye-brain-taigi","目睭大腦作伙動","台語護眼動腦，39 頁互動"),
     ("bp-722-guide","血壓機講啥物？","25 頁問答＋紙劇場小電影"),
     ("finger-brain-taigi","健腦手指協調操","手指動畫＋跟著做"),
     ("emotion-bear-class","熊熊心情教室","3 歲幼兒情緒辨識互動課"),
     ("essential-oil-special-kids","特殊兒精油放鬆與調節","證據等級標籤＋教案連結"),
     ("eye-health-for-seniors","眼睛顧好不吃虧","長者視力保健互動簡報")], note=("代間玩法","每個互動設計成「孩子答一題、長輩分享一段」；課後掃 QR 回家再玩一次。")))

S.append(keep("實作④ 參考設計做網頁型簡報",
    ('實作④　做網頁型簡報</div>', '教案設計⑦　實作：參考設計做網頁型簡報</div>'),
    ("再用實作⑦放上 GitHub Pages。今天這份簡報就是這樣做出來的。", "再放上 GitHub Pages（後面會教）。今天這份簡報就是這樣做出來的。"),
    ('幫我做一份 6 頁的網頁型簡報：「ICOPE 長者量六力」，給社區醫護人員看。用左右鍵換頁、上方有頁碼和進度條，第 1 頁封面、第 2 頁用數字統計列、後面六力各一張卡片。', '幫我做一份 8 頁的網頁型簡報：「祖孫一起動一動」，給社區祖孫活動用。用左右鍵換頁、上方有頁碼和進度條，第 1 頁封面、第 2 頁用數字統計列、後面每頁一個祖孫小遊戲卡片，每張卡有「搶答」按鈕。')))

# PPT
S.append(keep("實作⑤ Gemini 做 PPT：要用「任務」",
    ("實作⑤　做簡報</div>", "做 PPT　Gemini 任務模式</div>"),
    ("幫我做一份 6 頁的 PowerPoint 簡報（.pptx）：「長者量六力：社區衛教」，對象是社區長輩。每頁一個重點、字要大；每頁配一張溫暖插圖（台灣長輩）；最後一頁寫「65 歲以上可以到哪裡免費評估」。", "幫我做一份 8 頁的 PowerPoint 簡報遊戲（.pptx）：「祖孫猜猜看：台灣小吃」，對象是祖孫一起玩。每頁一題、字要大，題目頁配一張溫暖插圖（台灣阿公阿嬤和孫子），下一頁公布答案；最後一頁是「回家一起做」的小任務。")))
S.append(keep("實作⑤ ChatGPT 工作模式：自己生圖放進簡報", ("實作⑤　ChatGPT 也可以</div>", "做 PPT　ChatGPT 也可以</div>")))
S.append(keep("實作⑤ NotebookLM 做簡報", ("實作⑤　NotebookLM 自己做</div>", "做 PPT　NotebookLM 自己做</div>"),
    ("Canva 魔法圖層拆好後：每段字都變回文字框，插圖變成獨立圖片（實作③ 的示範）", "Canva 魔法圖層拆好後：每段字都變回文字框，插圖變成獨立圖片（紙本那一段的示範）")))
S.append(keep("實作⑤ ChatGPT＋Canva 外掛：記得檢查圖層", ("實作⑤　ChatGPT 的 Canva 外掛</div>", "做 PPT　ChatGPT 的 Canva 外掛</div>"),
    ("回到 Canva 首頁用「魔法圖層」自己拆（實作③ 那一頁）。", "回到 Canva 首頁用「魔法圖層」自己拆（紙本那一段）。")))

S.append(keep("實作⑦ 上架 GitHub Pages",
    ("實作⑦　上架分享</div>", "上架分享</div>"),
    ("輸入英文名稱，例如 icope-quiz", "輸入英文名稱，例如 family-quiz"),
    ("帳號.github.io/<b>icope-quiz</b>", "帳號.github.io/<b>family-quiz</b>")))

S.append(keep("實作⑧ OpenCode：選資料夾、選模型", ("實作⑧　AI 代理人 OpenCode</div>", "AI 代理人 OpenCode</div>")))
S.append(keep("實作⑧ OpenCode 代理人做 Google 表單", ("實作⑧　代理人幫你操作網頁</div>", "AI 代理人　幫你操作網頁</div>"),
    ("<h2>出題 → 它自己開瀏覽器，把 Google 表單建好</h2>", "<h2>活動報名表、回饋單：它自己開瀏覽器建好 Google 表單</h2>")))
S.append(keep("實作⑧ OpenCode 代理人整理資料夾", ("實作⑧　代理人幫你整理檔案</div>", "AI 代理人　幫你整理教案資料夾</div>"),
    ("依用途分成子資料夾（活動照片、簽到表、個案評估、核銷單據、會議記錄、海報、參考資料、其他）", "依用途分成子資料夾（教案、學習單、簡報、活動照片、簽到表、核銷單據、參考資料、其他）")))
S.append(keep("實作⑧ OpenCode 代理人蒐集資料", ("實作⑧　代理人幫你上網蒐集資料</div>", "AI 代理人　幫你上網蒐集資料</div>"),
    ('<b>說清楚：查什麼、去哪查、查不到怎麼辦</b><p>「只用政府網站」「每項附來源」「查不到寫查無資料，不要猜」這三句最重要。</p>', '<b>說清楚：查什麼、去哪查、查不到怎麼辦</b><p>「只用政府網站」「每項附來源」「查不到寫查無資料，不要猜」這三句最重要。（示範：查基隆市長者功能評估資訊）</p>'),
    ("幫我上網蒐集「（縣市）」65 歲以上長者功能評估（ICOPE 長者量六力）的官方資訊：誰可以做、多久一次、在哪裡做、要帶什麼、聯絡電話。只用政府網站（gov.tw），每一項附來源網址。整理成「資料蒐集/（縣市）ICOPE資訊.md」和一份 Excel 表。",
     "幫我上網蒐集「（縣市）」可以辦祖孫代間活動的地點與資源：社區關懷據點、樂齡學習中心、公共圖書館，以及代間活動補助計畫。只用政府網站（gov.tw），每一項附名稱、地址、電話、來源網址。整理成「資料蒐集/（縣市）代間活動資源.md」和一份 Excel 表。")))

S.append(f'''<!-- 更多教案 -->
<section class="slide" data-title="更多教案資料庫">
  <div class="eyebrow" style="--c:var(--sky)"><span class="sq"></span>帶回去用</div>
  <h2>更多教案資料庫：找點子、找影片、找玩法</h2>
  {exs([
    ("gamelearn","互動式與遊戲化教學法知識圖卡","問答、案例、電影、桌遊、實作、反思"),
    ("home-play-library","在家動一動 活動庫","運動、認知、體智能 78 個活動"),
    ("sensory-play-lessons","感覺遊戲教案庫","100 個感覺遊戲，幼兒長輩都適用"),
    ("eye-games-for-seniors","護眼同樂會","8 種團體視力遊戲，投影帶領"),
    ("classroom-screen","教室螢幕","計時、分組、抽籤 33 個小工具"),
    ("japan-dayservice-activity-videos","日本日照團康影片資料庫","350 支團康與體操，中文整理"),
    ("finger-database","手指操影片資料庫","50 支帶著做的示範影片"),
    ("temponumber","節奏挑戰・數字版","跟著拍子念數字，團體版"),
  ], m=4)}
</section>
''')

S.append('''<!-- 提示詞庫 -->
<section class="slide" data-title="提示詞庫">
  <div class="eyebrow" style="--c:var(--sky)"><span class="sq"></span>帶回去用</div>
  <h2>提示詞庫：把（ ）換掉就能用</h2>
  <div class="cols" style="--n:2">
    <div class="prompt"><div class="lab">代間活動教案<button class="copy">複製</button></div>設計一堂 60 分鐘的祖孫代間活動，主題（台灣小吃），孩子（5–8 歲）、長輩（70–85 歲）各 10 位。包含破冰（感覺動作）、主活動（配對或排序遊戲）、連結已知（請長輩分享）、收尾。每段寫時間、道具、帶領說法，以及孩子版／長輩版的難度調整。</div>
    <div class="prompt"><div class="lab">一副道具玩四種<button class="copy">複製</button></div>我有一副（撲克牌／1–16 數字牌），請依「配對、組合、排序、線索」四個機制各設計一個玩法，每個寫：做法、變簡單、變難、帶領時可以說的一句話。適合祖孫一起玩。</div>
    <div class="prompt"><div class="lab">簡報遊戲網頁<button class="copy">複製</button></div>幫我做一個（找不同／搶答／分類反應）簡報遊戲網頁，主題（ ），共 10 題、前易後難，按空白鍵換題，答案出現時有音效，可分兩隊計分。字要大、繁體中文。</div>
    <div class="prompt"><div class="lab">影片停格提問<button class="copy">複製</button></div>把這支影片（網址）切成 4–6 段，每段寫時間碼、重點、給孩子一題、給長輩一題，最後設計一個 5 分鐘的動手活動。看不到的寫「影片未提及」。</div>
    <div class="prompt"><div class="lab">學習單分級<button class="copy">複製</button></div>把這張學習單（貼內容）做成兩個版本：簡單版（題數少、字更大、有提示）給長輩，挑戰版（多 2 題、要推理）給孩子，兩張可以一起做。A4 直式、繁體中文。</div>
    <div class="prompt"><div class="lab">先問我再做<button class="copy">複製</button></div>在開始之前，請先問我 5 個你需要知道的問題（對象年齡、人數、道具、時間、場地），等我回答完再做。</div>
  </div>
</section>
''')

S.append('''<!-- 課後任務 -->
<section class="slide" data-title="課後任務">
  <div class="eyebrow" style="--c:var(--sky)"><span class="sq"></span>課後任務</div>
  <h2>兩週內，做出你的第一個代間教案</h2>
  <div class="cols" style="--n:2">
    <ul class="check">
      <li><label><input type="checkbox" id="h1"><span><b>用 Typeless 口述一個活動點子</b>，貼給 AI 整理成教案</span></label></li>
      <li><label><input type="checkbox" id="h2"><span><b>用撲克牌或 1–16 數字牌</b>，設計四大機制各一個玩法</span></label></li>
      <li><label><input type="checkbox" id="h3"><span><b>做一個簡報遊戲</b>，祖孫或同事試玩一次</span></label></li>
      <li><label><input type="checkbox" id="h4"><span><b>做一張分級學習單</b>，簡單版、挑戰版各一張</span></label></li>
      <li><label><input type="checkbox" id="h5"><span><b>用 OpenCode 做一份活動報名表</b>，自己按發布</span></label></li>
      <li><label><input type="checkbox" id="h6"><span><b>上架一個教案網頁</b>，把網址貼到 LINE 社群</span></label></li>
    </ul>
    <div style="display:flex;flex-direction:column;gap:14px;min-width:0">
      <div class="note" style="--c:var(--blue)"><b>卡住了</b><span>截圖貼到 LINE 學員社群，寫「哪一步、出現什麼畫面」。</span></div>
      <div class="note" style="--c:var(--mag)"><b>記得</b><span>不放孩子和長輩的姓名、照片給 AI；AI 做的規則與內容，帶活動前自己玩一次。</span></div>
      <div class="note" style="--c:var(--lime)"><b>勾選</b><span>打勾會記在這台電腦的瀏覽器裡，下次打開還在。</span></div>
    </div>
  </div>
</section>
''')

end = keep("謝謝聆聽",
    ('mattsue1003.github.io/keelung-icope-ai/基隆ICOPE_AI工作坊_講義.pptx', 'mattsue1003.github.io/intergen-ai-play/玩轉世代_AI代間教案_講義.pptx'),
    ("練習資料皆為虛擬資料", "範例教案皆可免費使用"))
end = re.sub(r'\s*<a class="fbcard survey".*?</a>', '', end, flags=re.S)
end = re.sub(r'\s*<a class="pill" href="[^"]*講義\.pptx"[^>]*>下載講義 PPT</a>', '', end)
end = end.replace('<div class="endqrs">', '<div class="endqrs">\n      <a class="fbcard" href="' + DECK_URL + '" target="_blank" rel="noopener"><img src="img/qr-deck.svg" alt="本簡報 QR code"><b>帶走<br>這份簡報</b><span class="fbbtn" style="background:var(--ink)">開啟簡報 ↗</span></a>')
S.append(end)

# 七種總覽（連結到各 type 頁）
T7 = [("①","var(--mag)","簡報遊戲","投影搶答、看到就動","教案設計① 簡報遊戲"),
      ("②","var(--blue)","簡報影片","影片切段、停格提問","教案設計② 簡報影片"),
      ("③","var(--amber)","音樂互動","老歌、節奏、律動","教案設計③ 音樂互動"),
      ("④","var(--sky)","動畫","步驟動畫、反應動畫","教案設計④ 動畫"),
      ("⑤","var(--lime)","紙本","學習單、產生器、分級","教案設計⑤ 紙本"),
      ("⑥","var(--green)","桌遊卡牌","自己的主題做一副牌","教案設計⑥ 桌遊卡牌"),
      ("⑦","var(--mag)","主題式衛教","多互動問答的網頁簡報","教案設計⑦ 主題式衛教")]
def idx(title):
    for i, s in enumerate(S):
        if f'data-title="{esc(title)}"' in s or f'data-title="{title}"' in s: return i + 1
    raise KeyError(title)

def build_types7():
    tiles = "".join(f'<a class="t7" href="#s{{{t[4]}}}" style="--c:{t[1]}"><i>{t[0]}</i><b>{t[2]}</b><small>{t[3]}</small><span class="tag">看範例 →</span></a>' for t in T7)
    tiles += '<div class="t7" style="--c:var(--ink)"><i>＋</i><b>工具</b><small>Gemini、ChatGPT、OpenCode、Canva：每一種都附提示詞，複製就能做</small></div>'
    return f'''<!-- 七種教案 -->
<section class="slide" data-title="七種教案設計總覽">
  <div class="eyebrow" style="--c:var(--ink)"><span class="sq"></span>教案設計</div>
  <h2>七種教案：先看範例，再教你怎麼用 AI 做</h2>
  <p class="lede">每一種都附 6 個範例（點卡片或掃 QR 打開）、設計重點，和一段可以直接複製的提示詞。</p>
  <div class="types7">{tiles}</div>
</section>
'''

AG = [("var(--mag)",None,"開場：講師與今天的成品","看完就知道做得到什麼","暖身：AI 做出的幼老教案","10′"),
      ("var(--blue)",None,"實作①　語音輸入","Typeless（建議裝桌機）、麥克風技巧、繁體設定","實作① 語音輸入","15′"),
      ("var(--blue)",None,"實作②　Chrome 的應用","問問 Gemini 讀資料、YouTube 讀影片","實作② Chrome 問問 Gemini","10′"),
      ("var(--green)",None,"遊戲化教學原則","發展階梯、四大機制、1–16 數字牌、撲克牌","遊戲化原則：從發展看幼老","25′"),
      ("var(--mag)",None,"教案①②　簡報遊戲、簡報影片","Gemini Canvas 實作、影片切段提問","七種教案設計總覽","20′"),
      ("var(--amber)","dk","教案③④　音樂互動、動畫","節奏遊戲、步驟動畫","教案設計③ 音樂互動","15′"),
      ("var(--lime)","dk","教案⑤⑥　紙本、桌遊卡牌","ChatGPT 參考風格、Canva 魔法圖層","教案設計⑤ 紙本","20′"),
      ("var(--mag)",None,"教案⑦　主題式衛教網頁簡報","多互動問答、參考設計","教案設計⑦ 主題式衛教","10′"),
      ("var(--mag)",None,"做 PPT","Gemini 任務、ChatGPT 工作、NotebookLM、Canva","實作⑤ Gemini 做 PPT：要用「任務」","15′"),
      ("var(--ink)",None,"上架＋AI 代理人 OpenCode","GitHub Pages、選模型、做表單、整理、蒐集","實作⑦ 上架 GitHub Pages","25′"),
      ("var(--sky)",None,"教案資料庫＋提示詞庫","帶回去直接用","更多教案資料庫","5′")]

def build_agenda():
    rows = []
    for i, (c, dk, t, sm, tgt, mins) in enumerate(AG):
        if i == 6: rows.append('<div class="brk">休息 10 分鐘</div>')
        cls = "no dk" if dk else "no"
        rows.append(f'<a href="#s{{{tgt}}}"><span class="{cls}" style="--c:{c}">{i}</span><span><strong>{t}</strong><small>{sm}</small></span><em>{mins}</em></a>')
    return f'''<!-- 地圖 -->
<section class="slide" data-title="今天的地圖">
  <div class="eyebrow" style="--c:var(--amber)"><span class="sq"></span>今天的地圖　09:00–12:00</div>
  <h2>三小時：先學會玩，再用 AI 做出七種教案</h2>
  <nav class="agenda" aria-label="課程地圖">{"".join(rows)}</nav>
</section>
'''

S[S.index("@@AGENDA@@")] = build_agenda()
S[S.index("@@TYPES7@@")] = build_types7()
body = "".join(S)
body = re.sub(r'#s\{([^}]+)\}', lambda m: f'#s{idx(m.group(1))}', body)
RETITLE = {"實作④ 做互動網頁":"教案① 實作：Gemini Canvas 搶答網頁","實作③ ChatGPT 參考風格做衛教圖":"教案⑤ ChatGPT 參考風格做學習單","實作③ Canva 魔法圖層改字改圖":"教案⑤ Canva 魔法圖層改字改圖","實作③ 免費版：Gemini 建立圖像":"教案⑤ 免費版：Gemini 建立圖像","實作④ 參考設計做網頁型簡報":"教案⑦ 參考設計做網頁型簡報","實作⑤ Gemini 做 PPT：要用「任務」":"做 PPT：Gemini 要用「任務」","實作⑤ ChatGPT 工作模式：自己生圖放進簡報":"做 PPT：ChatGPT 工作模式","實作⑤ NotebookLM 做簡報":"做 PPT：NotebookLM","實作⑤ ChatGPT＋Canva 外掛：記得檢查圖層":"做 PPT：ChatGPT＋Canva 外掛","實作⑦ 上架 GitHub Pages":"上架 GitHub Pages","實作⑧ OpenCode：選資料夾、選模型":"OpenCode：選資料夾、選模型","實作⑧ OpenCode 代理人做 Google 表單":"OpenCode 代理人做 Google 表單","實作⑧ OpenCode 代理人整理資料夾":"OpenCode 代理人整理資料夾","實作⑧ OpenCode 代理人蒐集資料":"OpenCode 代理人蒐集資料"}
for a, b in RETITLE.items():
    assert f'data-title="{a}"' in body, a
    body = body.replace(f'data-title="{a}"', f'data-title="{b}"')
mins = sum(int(a[5][:-1]) for a in AG) + 10
print("agenda minutes", mins, "slides", len(S))
(ROOT / "deck.html").write_text(head + body + tail)
(ROOT / "qr_list.txt").write_text("\n".join(f"{a}\t{b}" for a, b in dict(QR_LIST).items()))
