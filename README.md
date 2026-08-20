 
<div align="center">

<img src="./assets/banner.svg" alt="KIO.ai banner" width="100%" />

<br/>

[![Made by](https://img.shields.io/badge/made%20by-Hu%E1%BB%B3nh%20Th%C6%B0%C6%A1ng-ff69b4?style=for-the-badge)](https://github.com/zskbot)
[![Repo](https://img.shields.io/badge/repo-zskbot%2Fkio.ai-7dd3fc?style=for-the-badge&logo=github)](https://github.com/zskbot/kio.ai)
[![License](https://img.shields.io/badge/license-MIT-a78bfa?style=for-the-badge)](#-license)
[![Status](https://img.shields.io/badge/status-active%20development-4ade80?style=for-the-badge)](#)

**KIO.ai** â€” trá»£ lĂ½ láº­p trĂ¬nh dáº¡ng *Agent* tá»± chá»n **skill** vĂ  **tool** phĂ¹ há»£p cho tá»«ng tĂ¡c vá»¥, quĂ©t workspace, lĂªn káº¿ hoáº¡ch thá»±c thi vĂ  bĂ¡o cĂ¡o káº¿t quáº£.

</div>

<br/>

## đŸ“ Má»¥c lá»¥c

- [Giá»›i thiá»‡u](#-giá»›i-thiá»‡u)
- [Demo](#-demo)
- [Kiáº¿n trĂºc hoáº¡t Ä‘á»™ng](#-kiáº¿n-trĂºc-hoáº¡t-Ä‘á»™ng)
- [TĂ­nh nÄƒng ná»•i báº­t](#-tĂ­nh-nÄƒng-ná»•i-báº­t)
- [Bá»™ cĂ´ng cá»¥ (Tools)](#-bá»™-cĂ´ng-cá»¥-tools)
- [Bá»™ ká»¹ nÄƒng (Skills)](#-bá»™-ká»¹-nÄƒng-skills)
- [Cáº¥u trĂºc dá»± Ă¡n](#-cáº¥u-trĂºc-dá»±-Ă¡n)
- [Báº¯t Ä‘áº§u nhanh](#-báº¯t-Ä‘áº§u-nhanh)
- [Cáº¥u hĂ¬nh](#-cáº¥u-hĂ¬nh)
- [Lá»™ trĂ¬nh phĂ¡t triá»ƒn](#-lá»™-trĂ¬nh-phĂ¡t-triá»ƒn)
- [ÄĂ³ng gĂ³p](#-Ä‘Ă³ng-gĂ³p)
- [Giáº¥y phĂ©p](#-giáº¥y-phĂ©p)
- [TĂ¡c giáº£](#-tĂ¡c-giáº£)

<br/>

## âœ¨ Giá»›i thiá»‡u

**KIO.ai** lĂ  má»™t *AI coding agent* cháº¡y trĂªn ná»n **Python** (`server.py`, `agent_router.py`) káº¿t há»£p giao diá»‡n web nháº¹ (`index.html`, `app.js`, `style.css`). TrĂ¡i tim cá»§a dá»± Ă¡n lĂ  bá»™ Ä‘á»‹nh tuyáº¿n (`agent_router.py`): vá»›i má»—i yĂªu cáº§u ngÆ°á»i dĂ¹ng, KIO sáº½:

1. **Chuáº©n hoĂ¡** ná»™i dung tĂ¡c vá»¥ (`normalize`)
2. **Cháº¥m Ä‘iá»ƒm** vĂ  chá»n ra cĂ¡c **skill** & **tool** liĂªn quan nháº¥t (`select_skills`, `select_tools`)
3. **QuĂ©t workspace** Ä‘á»ƒ náº¯m cáº¥u trĂºc thÆ° má»¥c (`inspect_workspace`)
4. **Lá»c ra cĂ¡c tá»‡p** bá»‹ áº£nh hÆ°á»Ÿng theo pháº§n má»Ÿ rá»™ng & Ä‘á»™ Æ°u tiĂªn (`choose_files`)
5. **Láº­p káº¿ hoáº¡ch thá»±c thi** tá»«ng bÆ°á»›c (`make_plan`) vĂ  tráº£ káº¿t quáº£ dáº¡ng JSON

Nhá» váº­y, KIO cĂ³ thá»ƒ tá»± thĂ­ch á»©ng vá»›i nhiá»u loáº¡i tĂ¡c vá»¥ khĂ¡c nhau â€” tá»« dá»±ng giao diá»‡n web, sá»­a lá»—i backend, cháº¡y test, cho tá»›i thao tĂ¡c Git/GitHub vĂ  triá»ƒn khai dá»± Ă¡n â€” mĂ  khĂ´ng cáº§n cáº¥u hĂ¬nh thá»§ cĂ´ng cho tá»«ng trÆ°á»ng há»£p.

<br/>

## đŸ¬ Demo

<div align="center">
<img src="./assets/demo.gif" alt="KIO.ai agent console demo" width="720" />
</div>

<br/>

## đŸ§  Kiáº¿n trĂºc hoáº¡t Ä‘á»™ng

<img src="./assets/architecture.svg" alt="SÆ¡ Ä‘á»“ kiáº¿n trĂºc agent_router.py" width="100%" />

> Luá»“ng xá»­ lĂ½: **Task â†’ Router (score & chá»n skill/tool) â†’ QuĂ©t workspace & chá»n file â†’ Láº­p káº¿ hoáº¡ch â†’ Tráº£ káº¿t quáº£.**

<br/>

## đŸ€ TĂ­nh nÄƒng ná»•i báº­t

| | TĂ­nh nÄƒng | MĂ´ táº£ |
|---|---|---|
| đŸ§© | **Router thĂ´ng minh** | Cháº¥m Ä‘iá»ƒm tá»« khoĂ¡ Ä‘á»ƒ tá»± chá»n skill/tool phĂ¹ há»£p nháº¥t vá»›i tá»«ng yĂªu cáº§u |
| đŸ“ | **QuĂ©t workspace** | Tá»± Ä‘á»™ng liá»‡t kĂª file dá»± Ă¡n, bá» qua `.git`, `node_modules`, `.venv`, `.env` |
| đŸ¯ | **Chá»n file Æ°u tiĂªn** | Æ¯u tiĂªn cĂ¡c tá»‡p lĂµi nhÆ° `index.html`, `style.css`, `app.js`, `server.py` |
| đŸ—ºï¸ | **Láº­p káº¿ hoáº¡ch tá»«ng bÆ°á»›c** | Sinh plan rĂµ rĂ ng: phĂ¢n tĂ­ch â†’ chá»n skill/tool â†’ quĂ©t â†’ build â†’ validate â†’ bĂ¡o cĂ¡o |
| đŸ”Œ | **Kiáº¿n trĂºc plugin** | Má»Ÿ rá»™ng qua `plugins.json`, `plugins/`, `skills/` |
| đŸŒ | **Giao diá»‡n web nháº¹** | `index.html` + `app.js` + `style.css`, khĂ´ng phá»¥ thuá»™c framework náº·ng |
| đŸ™ | **TĂ­ch há»£p Git/GitHub** | Há»— trá»£ thao tĂ¡c repo, branch, pull request ngay trong agent |

<br/>

## đŸ›  Bá»™ cĂ´ng cá»¥ (Tools)

| Tool | NhĂ³m | Icon | MĂ´ táº£ |
|---|---|:---:|---|
| `terminal` | Core | âŒ˜ | Cháº¡y lá»‡nh dá»± Ă¡n qua KIO build console |
| `file-manager` | Core | â—‡ | Kiá»ƒm tra file & cáº¥u trĂºc workspace |
| `code-search` | Core | âŒ• | TĂ¬m kiáº¿m vĂ  Ä‘á»‹nh vá»‹ code liĂªn quan |
| `build` | Build | â–¶ | Cháº¡y build vĂ  cĂ¡c bÆ°á»›c kiá»ƒm chá»©ng dá»± Ă¡n |
| `test` | Build | âœ“ | Cháº¡y test vĂ  bĂ¡o cĂ¡o lá»—i |
| `git` | Developer | â‘‚ | Kiá»ƒm tra tráº¡ng thĂ¡i repo, chuáº©n bá»‹ thao tĂ¡c Git |
| `github` | Developer | â—ˆ | TĂ­ch há»£p repository, issue, pull request |
| `deploy` | Developer | â†‘ | Chuáº©n bá»‹ luá»“ng triá»ƒn khai cho cĂ¡c ná»n táº£ng há»— trá»£ |
| `browser` | Web | â— | Kiá»ƒm tra giao diá»‡n & xĂ¡c thá»±c á»©ng dá»¥ng web |
| `http` | Web | â†— | Kiá»ƒm tra API vĂ  HTTP endpoint |

<br/>

## đŸ§¬ Bá»™ ká»¹ nÄƒng (Skills)

`agent_router.py` cháº¥m Ä‘iá»ƒm tá»« khoĂ¡ Ä‘á»ƒ chá»n tá»‘i Ä‘a **4 skill** phĂ¹ há»£p nháº¥t cho má»—i tĂ¡c vá»¥:

`frontend` Â· `backend` Â· `debugging` Â· `testing` Â· `git-workflow` Â· `deployment` Â· `project-analysis`

Náº¿u khĂ´ng cĂ³ tá»« khoĂ¡ nĂ o khá»›p, KIO máº·c Ä‘á»‹nh dĂ¹ng skill `project-analysis` (tools: `file-manager`, `code-search`, `build`) Ä‘á»ƒ Ä‘áº£m báº£o luĂ´n cĂ³ hÆ°á»›ng xá»­ lĂ½ an toĂ n.

<br/>

## đŸ—‚ Cáº¥u trĂºc dá»± Ă¡n

```text
kio.ai/
â”œâ”€â”€ .github/            # Workflow / cáº¥u hĂ¬nh GitHub
â”œâ”€â”€ assets/             # áº¢nh, banner, tĂ i nguyĂªn tÄ©nh
â”œâ”€â”€ backup/             # Báº£n sao lÆ°u
â”œâ”€â”€ plugins/            # Plugin má»Ÿ rá»™ng cho agent
â”œâ”€â”€ skills/             # Äá»‹nh nghÄ©a cĂ¡c skill
â”œâ”€â”€ agent_router.py     # Bá»™ Ä‘á»‹nh tuyáº¿n task â†’ skill/tool â†’ plan
â”œâ”€â”€ server.py           # Backend phá»¥c vá»¥ agent & giao diá»‡n
â”œâ”€â”€ index.html           # Giao diá»‡n web
â”œâ”€â”€ app.js               # Logic phĂ­a client
â”œâ”€â”€ style.css             # Giao diá»‡n style
â”œâ”€â”€ plugins.json         # Danh sĂ¡ch plugin Ä‘Äƒng kĂ½
â”œâ”€â”€ tools.json           # Danh má»¥c tool kháº£ dá»¥ng
â”œâ”€â”€ .env.example          # Máº«u biáº¿n mĂ´i trÆ°á»ng
â””â”€â”€ README.md
```

<br/>

## â¡ Báº¯t Ä‘áº§u nhanh

```bash
# 1. Clone dá»± Ă¡n
git clone https://github.com/zskbot/kio.ai.git
cd kio.ai

# 2. Cáº¥u hĂ¬nh biáº¿n mĂ´i trÆ°á»ng
cp .env.example .env
# â†’ má»Ÿ .env vĂ  Ä‘iá»n cĂ¡c giĂ¡ trá»‹ cáº§n thiáº¿t (API key, cá»•ng cháº¡y, v.v.)

# 3. CĂ i Ä‘áº·t phá»¥ thuá»™c Python (náº¿u cĂ³ requirements riĂªng)
pip install -r requirements.txt   # bá» qua náº¿u dá»± Ă¡n khĂ´ng cĂ³ file nĂ y

# 4. Khá»Ÿi cháº¡y server
python server.py
```

Sau khi server cháº¡y, má»Ÿ trĂ¬nh duyá»‡t tá»›i Ä‘á»‹a chá»‰ Ä‘Æ°á»£c `server.py` in ra (máº·c Ä‘á»‹nh thÆ°á»ng lĂ  `http://localhost:PORT`) Ä‘á»ƒ sá»­ dá»¥ng giao diá»‡n KIO.

<br/>

## â™ï¸ Cáº¥u hĂ¬nh

ToĂ n bá»™ biáº¿n mĂ´i trÆ°á»ng cáº§n thiáº¿t Ä‘Æ°á»£c liá»‡t kĂª máº«u trong [`.env.example`](./.env.example). HĂ£y sao chĂ©p thĂ nh `.env` vĂ  cáº­p nháº­t theo mĂ´i trÆ°á»ng cá»§a báº¡n trÆ°á»›c khi cháº¡y `server.py`.

Danh sĂ¡ch tool kháº£ dá»¥ng cĂ³ thá»ƒ má»Ÿ rá»™ng qua [`tools.json`](./tools.json) vĂ  plugin Ä‘Äƒng kĂ½ qua [`plugins.json`](./plugins.json).

<br/>

## đŸ§­ Lá»™ trĂ¬nh phĂ¡t triá»ƒn

- [ ] Má»Ÿ rá»™ng thĂªm skill chuyĂªn biá»‡t theo ngĂ´n ngá»¯/framework
- [ ] ThĂªm giao diá»‡n quáº£n lĂ½ plugin trá»±c quan
- [ ] Há»— trá»£ Ä‘a ná»n táº£ng triá»ƒn khai (deploy) má»Ÿ rá»™ng
- [ ] Viáº¿t bá»™ test tá»± Ä‘á»™ng cho `agent_router.py`

<br/>

## đŸ¤ ÄĂ³ng gĂ³p

Má»i Ä‘Ă³ng gĂ³p Ä‘á»u Ä‘Æ°á»£c chĂ o Ä‘Ă³n!

1. Fork dá»± Ă¡n
2. Táº¡o nhĂ¡nh tĂ­nh nÄƒng: `git checkout -b feature/ten-tinh-nang`
3. Commit thay Ä‘á»•i: `git commit -m "feat: mo ta thay doi"`
4. Push nhĂ¡nh: `git push origin feature/ten-tinh-nang`
5. Má»Ÿ Pull Request

<br/>

## đŸ“„ Giáº¥y phĂ©p

PhĂ¡t hĂ nh theo giáº¥y phĂ©p **MIT** â€” xem chi tiáº¿t táº¡i file `LICENSE` (náº¿u cĂ³) trong repository.

<br/>

## đŸ‘¤ TĂ¡c giáº£

<div align="center">

**Huá»³nh ThÆ°Æ¡ng â¤ï¸**

Chá»§ dá»± Ă¡n Â· Thiáº¿t káº¿ & phĂ¡t triá»ƒn KIO.ai

[![GitHub](https://img.shields.io/badge/GitHub-zskbot-181717?style=flat-square&logo=github)](https://github.com/zskbot)

</div>

<br/>

<div align="center">
<sub>Made with â¤ï¸ by <b>Huá»³nh ThÆ°Æ¡ng</b> â€” powered by KIO.ai</sub>
</div>