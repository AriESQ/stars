<div align="center">

# Opus 5.5 Video Prompts

**Claude Opus 5.5 “用代码拍视频”：全网案例与可直接复制的提示词**

18 份完整提示词 · 54 个公开案例 · 9 种技术路线 · 持续更新

[提示词速查](#-提示词速查) · [精选提示词](#-精选提示词) · [案例总览](#-案例总览) · [写法经验](#-写法经验) · [资料来源](#-资料来源)

</div>

---

## 这是什么

Opus 5.5 本身**不输出视频文件**。它的做法是写代码画出每一帧：HTML Canvas、p5.js、Three.js、Remotion、Manim、Blender 脚本都有人用。然后用无头浏览器逐帧截图，再用 FFmpeg 合成 MP4；配乐一般用 Web Audio 或 Python 合成，旁白接 TTS。

所以它擅长**动态图形、手绘/线稿/水墨动画、科普讲解、产品发布片、歌词 MV**，不擅长写实的真人镜头。真要写实画面，常见做法是让它调用 Seedance、Runway、Higgsfield 这类视频模型，自己负责编排和剪辑。

本仓库整理了 Opus 5.5 发布后第一周（2026-09-22 至 09-25）X、B 站、Linux.do、GitHub、YouMind 等处公开的案例，**只收作者本人公开的提示词原文**，每条都附原帖链接。

## ⚡ 三分钟上手

```text
1. 装好 Claude Code，模型切到 Opus 5.5，effort 调到 high / xhigh
2. 本机准备 Node.js、Chrome、FFmpeg（渲染 MP4 用）
3. 新建空目录，从下面挑一条提示词粘进去
4. 等它写代码、渲染、自检，拿到 MP4
```

最短的测试提示词（Deedy 用它做出了发布片，作者说约 1 分钟、2 美元）：

```text
make a modern slick and punchy video for a modern startup that works on inference
```

中文用户可以直接试这条（WY）：

```text
做一个动画，快速回顾中华五千年的历史。风格轻松有趣，动画格式为线稿，添加合适的音乐，请务必做到引人入胜
```

## 📋 提示词速查

| # | 提示词 | 作者 | 类型 | 文件 |
|---|---|---|---|---|
| 01 | 推理创业公司发布视频 | Deedy (@deedydas) | 一句话 | [打开](prompts/01-inference-startup-launch.md) |
| 02 | 15 秒动态设计作品集（Max effort） | Stephan Livera | 一句话 | [打开](prompts/02-motion-showreel-15s.md) |
| 03 | 中华五千年历史速览（线稿动画） | WY (@akokoi1) | 一句话 · 中文 | [打开](prompts/03-china-5000-years-lineart.md) |
| 04 | 一个 30 秒的 Opus 5 广告（致敬苹果《1984》） | 1LittleCoder（据 YouMind 收录） | 一句话 | [打开](prompts/04-opus-1984-ad.md) |
| 05 | 讲解 Transformer 的 JS 视频 | 宝玉（据 YouMind 收录） | 一句话 · 中文 | [打开](prompts/05-transformer-explainer-js.md) |
| 06 | 从房间一路放大到夸克 | Taelin（据 YouMind 收录，英文原文的中文转述） | 一句话 | [打开](prompts/06-room-to-quarks-zoom.md) |
| 07 | 30 秒企业讲解片模板 | Alex Prompter (@alex_prompter) | 模板 · 填空 | [打开](prompts/07-business-explainer-30s.md) |
| 08 | 鸡尾酒配方动态图解（Negroni） | Rory Flynn (@Ror_Fly) | 参考图 | [打开](prompts/08-negroni-recipe-explainer.md) |
| 09 | 大气环流科普（带 TTS 旁白与双语字幕） | WY (@akokoi1) | 中文 · TTS | [打开](prompts/09-atmospheric-circulation-tts.md) |
| 10 | 真人口播改成线稿动画讲解 | Axton (@AxtonLiu) | 中文 · 改编已有视频 | [打开](prompts/10-talking-head-to-lineart.md) |
| 11 | 奥斯特里茨战役历史电影（4 到 5 分钟） | Winter (@WinterArc2125) | 长提示词 · 参考图 | [打开](prompts/11-austerlitz-film.md) |
| 12 | App 宣传片（Remotion，第 1 支） | Danny Stuart | Remotion | [打开](prompts/12-remotion-app-promo-1.md) |
| 13 | App 宣传片（Remotion，第 2 支） | Danny Stuart | Remotion | [打开](prompts/13-remotion-app-promo-2.md) |
| 14 | SaaS 发布片（抓真实素材） | Joe Davies（LinkedIn） | 品牌 · 网络素材 | [打开](prompts/14-saas-launch-real-assets.md) |
| 15 | UI 形态变换循环（1440×1440） | zero (@twoclipping) | 专业模板 | [打开](prompts/15-ui-morph-loop.md) |
| 16 | 高端极简产品片（1920×1080，接入真实素材） | zero (@twoclipping) | 专业模板 · 真实素材 | [打开](prompts/16-high-end-product-video.md) |
| 17 | 像素巫师施法动画 | Majid Manzarpour | 规格型 | [打开](prompts/17-pixel-wizard.md) |
| 18 | 交互式史前岛屿（Three.js） | Vib3Coded | 规格型 · 3D | [打开](prompts/18-prehistoric-island-threejs.md) |

另有两份超长提示词只给要点和原帖链接：Rikuo 的[彩虹路像素跑酷](https://x.com/riku720720/status/2102515058010132554)（日文，约 3000 字），donald 的 [Claude Pop 混合流程 MV](https://x.com/donaldjewkes/status/2102801469976248500)（约 2000 词，流程是 fal 出角色图 → Seedance 2.5 生成底片 → JS 逐帧重绘）。

## ✨ 精选提示词

短提示词直接展开，长提示词折叠了，点开即可复制。

### 2.1 一句话即可出片

#### 01. 推理创业公司发布视频

作者：Deedy (@deedydas) · [原帖](https://x.com/deedydas/status/2102787937482252537) · [单独文件](prompts/01-inference-startup-launch.md)

作者称 1 分钟、约 2 美元做完。只有一句话，没有指定任何工具。

```text
make a modern slick and punchy video for a modern startup that works on inference
```

#### 02. 15 秒动态设计作品集（Max effort）

作者：Stephan Livera · [原帖](https://x.com/stephanlivera/status/2103315922098470926) · [单独文件](prompts/02-motion-showreel-15s.md)

effort 调到 Max，让模型自由发挥。

```text
make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.
```

#### 03. 中华五千年历史速览（线稿动画）

作者：WY (@akokoi1) · [原帖](https://x.com/akokoi1/status/2102584165220962502) · [单独文件](prompts/03-china-5000-years-lineart.md)

作者表示提示词“只有一句”。

```text
做一个动画，快速回顾中华五千年的历史。风格轻松有趣，动画格式为线稿，添加合适的音乐，请务必做到引人入胜
```

#### 04. 一个 30 秒的 Opus 5 广告（致敬苹果《1984》）

作者：1LittleCoder（据 YouMind 收录） · [原帖](https://youmind.com/opus-5-5-prompts) · [单独文件](prompts/04-opus-1984-ad.md)

YouMind 只收录了开头一句，完整原文以原帖为准。

```text
create a 30 second ad for Opus 5
```

#### 05. 讲解 Transformer 的 JS 视频

作者：宝玉（据 YouMind 收录） · [原帖](https://youmind.com/opus-5-5-prompts) · [单独文件](prompts/05-transformer-explainer-js.md)

```text
帮我用 JS 做一个视频，主题是：什么是 Transformer
```

#### 06. 从房间一路放大到夸克

作者：Taelin（据 YouMind 收录，英文原文的中文转述） · [原帖](https://youmind.com/opus-5-5-prompts) · [单独文件](prompts/06-room-to-quarks-zoom.md)

```text
做一段动画：从一个房间开始，镜头推进到一台 MacBook，再进入 Apple M4 芯片，然后到原子，最后到夸克
```

### 2.2 带结构的讲解与营销片模板

#### 07. 30 秒企业讲解片模板

作者：Alex Prompter (@alex_prompter) · [原帖](https://x.com/alex_prompter/status/2103499977632997524) · [单独文件](prompts/07-business-explainer-30s.md)

作者建议：Claude 会在对话里直接播放，录屏即得视频；之后一次只提一条修改意见，例如“慢一点”“更有活力”“加一个讲价格的场景”。

```text
Adopt the role of an expert motion designer. Build a 30-second animated explainer for my business as a single HTML page. 5 scenes. The customer's problem, what I do, how it works in 3 steps, one proof point, and my name at the end. Bold text, smooth transitions, my brand colours. My business [DESCRIBE WHAT YOU SELL, WHO IT'S FOR AND YOUR COLOURS]
```

#### 08. 鸡尾酒配方动态图解（Negroni）

作者：Rory Flynn (@Ror_Fly) · [原帖](https://x.com/Ror_Fly/status/2102853258582880547) · [单独文件](prompts/08-negroni-recipe-explainer.md)

只给了 1 张参考图。成片有步骤计数器、ml/oz 用量、进度条，最后以“THAT'S A NEGRONI / 1:1:1”收尾。

```text
We're going to try a little test. Do you think you could render a recipe motion graphic animation using javascript or html (w/e you think will produce the best) to show the full recipe from start to finish (empty glass to completed cocktail) - Explainer video style - Showing the recipe ingreidents + measurements as they're going into the cup. Should be a 30s video.
```

#### 09. 大气环流科普（带 TTS 旁白与双语字幕）

作者：WY (@akokoi1) · [原帖](https://x.com/akokoi1/status/2102606609574941028) · [单独文件](prompts/09-atmospheric-circulation-tts.md)

用时 26 分钟，生成近 5 分钟视频。准备步骤：把 TTS 厂商（豆包、智谱、海螺、千问等均可）的文本转语音文档存为 TTS.md，在 .env 里写 API KEY 和音色。安全提示：在 .claude/settings.json 加 `"deny": ["Read(./.env)"]`，Claude 就读不到 key。同一提示词把知识点换成具体题目，就能做成物理竞赛题讲解。

```text
做一个动画，讲解高中地理知识点“大气环流”。风格轻松有趣，动画格式为线稿，添加合适的音乐，请务必做到引人入胜，字幕用中英双语，解说用TTS，如果 TTS 接口有关闭水印的参数就关掉，文档在TTS.md，API KEY 和音色分别是 .env 里的 APIKEY 和 VOICE，最终视频要能直接导出。
```

#### 10. 真人口播改成线稿动画讲解

作者：Axton (@AxtonLiu) · [原帖](https://x.com/AxtonLiu/status/2102827887732932956) · [单独文件](prompts/10-talking-head-to-lineart.md)

条件：干净的 Claude Code、safe mode、effort high，不加载任何 Skill，也不给外部素材。按字幕切了约 30 个镜头，用时 28 分 53 秒，全程没有人工介入。

```text
把 short-1.mp4 做成一条新的竖屏短片 short-1-v5.mp4：

1. 我的人像缩小成右下角的圆形画中画，能看清我在讲话，不遮字幕。
2. 主画面换成一段动画 B-roll，跟着我讲的内容走：我说到哪个概念，画面就画哪个概念。风格轻松有趣，线稿动画就可以，不要写实。
3. 原声、原字幕、时长都不变。
```

#### 11. 奥斯特里茨战役历史电影（4 到 5 分钟）

作者：Winter (@WinterArc2125) · [原帖](https://x.com/WinterArc2125/status/2103116689944502720) · [单独文件](prompts/11-austerlitz-film.md)

附了几幅战争油画作为视觉参考。开源仓库：[Battle-of-Austerlitz-Film](https://github.com/WinterArc21/Battle-of-Austerlitz-Film)，包含 WebGL 渲染器、地形数据、Kokoro 旁白、合成音效，以及 Chromium 到 FFmpeg 的渲染流程。

<details>
<summary>展开提示词（847 字符）</summary>

```text
Create a 4–5 minute cinematic video about the Battle of Austerlitz (1805), built entirely in code.

Research the battle thoroughly and decide for yourself how to tell the story, structure the pacing, explain the strategy, and visualize the events. I want it to be historically accurate, dramatic, easy to understand, and visually exceptional.

Use the attached paintings as visual inspiration, not a strict style requirement. I love their scale, atmosphere, smoke, dramatic skies, cavalry, massed formations, landscape, and sense of chaos. Find a way to translate that feeling into code — but if you can invent a stronger visual language, do it.

Don't make it feel like a generic infographic or strategy game. It should feel like a cinematic historical film that happens to be rendered with code.

You have complete creative control. Surprise me.
```

</details>

### 2.3 SaaS/产品宣传片

#### 12. App 宣传片（Remotion，第 1 支）

作者：Danny Stuart · [原帖](https://dannystuart.substack.com/p/claude-code-opus-remotion-agentic-promo-video) · [单独文件](prompts/12-remotion-app-promo-1.md)

每支大约 10 分钟。作者的经验：先出分镜再写代码，之后可以针对单个镜头修改；描述质量时，给参考视频比堆形容词有效；用“dramatic cuts”“orbiting camera”这类镜头语言。草稿阶段关掉动态模糊、用半分辨率，或直接在 Remotion Studio 里拖动预览。

```text
I want you to create a promotional video in an app/saas style. It will be to promote a fictional app that helps designers have a visual tool to manage Git... It must be 10-15 seconds long. Use dramatic cuts and kinetic typography. Dynamic apple style video... Light style/theme... Storyboard the video and plan carefully before coding anything.
```

#### 13. App 宣传片（Remotion，第 2 支）

作者：Danny Stuart · [原帖](https://dannystuart.substack.com/p/claude-code-opus-remotion-agentic-promo-video) · [单独文件](prompts/13-remotion-app-promo-2.md)

```text
I want to create a similar promo video to the level of quality that we created the twig promo video... Glass Materials which is part of the Vanta Supply family... It must be 15 seconds long. Use dramatic cuts and kinetic typography... dark style with grainey gradients... Storyboard the video and plan carefully before coding anything.
```

#### 14. SaaS 发布片（抓真实素材）

作者：Joe Davies（LinkedIn） · [原帖](https://community.startuptalky.com/discussions/post/opus-5-5-is-very-good-at-creating-videos-this-is-the-prompt-i-used-i-f6nYoYyvteUj6bd) · [单独文件](prompts/14-saas-launch-real-assets.md)

转载页面的原文在结尾处被截断。

```text
I want you to create a highly professional SaaS style product launch video for fatjoe.com/grow. Go and find some SaaS, preferably just one that people know, so it's easier to identify with it. Pick that, and then make sure to get actual assets and images and all of that stuff from the internet. Turn it into these typical, very professionally edited, motion-graphics-styled product launch videos that you see people making on Twitter when they launch new SaaS products (which are showing off the features, the benefits, and all of these things). Use fatjoe branding like …
```

### 2.4 专业级 Motion Design 模板（@zero）

#### 15. UI 形态变换循环（1440×1440）

作者：zero (@twoclipping) · [原帖](https://x.com/twoclipping/status/2103273003555402193) · [单独文件](prompts/15-ui-morph-loop.md)

<details>
<summary>展开提示词（2711 字符）</summary>

```text
<inputs>
Ask me for: 8 to 12 UI states I want the shape to become (e.g. button, loader, player, slider, toggle, tabs, chart, command palette, toast), pure black and white or one accent color, and a royalty-free song around 120 BPM (e.g. Mixkit, free for commercial use).
</inputs>

<direction>
Dribbble-level UI motion. One shape, never cut: every state is the same element morphing its size, radius and color while its content swaps with a short blur. A cursor drives every change with real clicks and drags. Light warm-gray canvas, black and white components, one clean UI font (Geist). Springs everywhere, a tiny overshoot at most. The camera zooms so each state fills the frame. The last frame is the first frame, so it loops.
Banned: bouncy easing, particle bursts, glows, gradients on UI chrome, mismatched icon strokes, dead time, anything that looks like a template.
</direction>

<structure>
120 BPM, 7 bars, something happens on every beat.
Button → loader → check → dynamic island → music player with a play/pause morph → scrub the progress bar → it becomes a volume slider that stretches when dragged past max → a toggle flips on the beat → the knob becomes a liquid tab indicator → the tabs open into a chart that draws itself, with a tooltip on hover → it collapses into ⌘K → type to filter → enter → toast → back to the button.
</structure>

<build>
1. One HTML file, square 1440x1440. Every style is computed from time inside seek(t): no CSS transitions, no timers, no state carried between frames.
2. Springs are closed-form step responses. A value that changes target many times is the sum of one spring per change, so it stays a pure function of time.
3. The tab indicator's two edges ride different springs, so the leading edge stretches ahead of the trailing one. Same trick for the toggle knob.
4. Drags are direct manipulation: while the cursor is held, the value is computed from its position. On release it springs back from wherever it was.
5. Analyze the song with numpy for the beat grid and start on a downbeat. Place every UI sound by its measured peak.
6. Render with Playwright: 4 subframes per frame, blended with ffmpeg tmix for motion blur at 60fps.
7. Render one frame per beat before the full render. Fix anything off the grid, cramped or hard to read.
</build>

<gotchas>
Never put will-change on anything the camera scales or the text renders blurry. Text that swaps inside a morphing container needs its own enter and exit timing or it overlaps. Make the last frame identical to the first, cursor position and speed included, or the loop stutters.
</gotchas>

<start>
Ask me for the inputs, then show me the state list on the beat grid before you write any code.
</start>
```

</details>

#### 16. 高端极简产品片（1920×1080，接入真实素材）

作者：zero (@twoclipping) · [原帖](https://youmind.com/video-prompts/high-end-product-video-prompt-11292) · [单独文件](prompts/16-high-end-product-video.md)

YouMind 收录，1.4K 收藏。

<details>
<summary>展开提示词（2494 字符）</summary>

```text
<inputs>
Ask me for: the product name and a one-line promise, 3 to 5 UI moments to show, one accent color, 10 to 20 real vertical clips I own, and a royalty-free song with a clear drop (e.g. Mixkit, free for commercial use).
</inputs>
<direction>
High-end minimal. One idea per shot, lots of empty space, one accent color, one clean sans (Geist or Inter) with tight tracking. Masked type reveals, match cuts, one smooth camera language. Real footage only, never placeholder cards. No full stops in on-screen text.
Banned: shockwave rings, particle bursts, RGB split, camera shake, lens flares, neon glows, grid floors, flashing backgrounds, bouncy easing.
</direction>
<structure>
10 bars at 120 BPM, 2 seconds each.
Bar 1: the hook lands word by word on the beats.
Bar 2: one hook word morphs into the product UI. A cursor types and clicks.
The drop: a circle opens out of the button into a dark scene.
Then one move per bar: a wall of real clips with a scan line and 3 winners, the key output as big type, a 3D carousel of real videos with floor reflections and a motion-blurred whip onto one hero clip, the hero in a phone next to a panel that flips into results, big stats on push cuts, a 3-word ticker, a logo reveal, a fade to black.
</structure>
<build>
1. One HTML file at 1920x1080. Every style is computed from time inside seek(t): no CSS animations, no timers, no state between frames.
2. Real video: extract clips to 30fps JPEG sequences with ffmpeg and swap img sources per frame. seek awaits the image decodes.
3. Analyze the song with numpy: tempo, beat grid, energy per bar, the drop. Calibrate the grid to the real kick hits. Every cut sits on a downbeat, every UI hit on a beat.
4. Render with Playwright: 3 subframes per frame at t minus, at, and plus 1/240s, then blend with ffmpeg tmix for real motion blur at 60fps.
5. Place each sound effect so its measured peak, not its file start, lands on the event. Keep the effects quiet under the music. Loudnorm to -14 LUFS.
6. Probe 20 or more frames before the full render. Fix anything cluttered, overlapping or hard to read.
</build>
<gotchas>
Never set opacity or filter on a preserve-3d element, because it flattens and both faces show. Fade its wrapper instead. Measure element positions at runtime for match cuts. Only use music and sound effects whose license allows commercial use.
</gotchas>
<start>
Ask me for the inputs, then show me a storyboard with every timing on the beat grid before you write any code.
</start>
```

</details>

### 2.5 像素 / 三维场景规格型提示词

#### 17. 像素巫师施法动画

作者：Majid Manzarpour · [原帖](https://x.com/majidmanzarpour/status/2102476499387383834) · [单独文件](prompts/17-pixel-wizard.md)

<details>
<summary>展开提示词（2209 字符）</summary>

```text
Create a single self-contained HTML file that renders an animated pixel art wizard casting a spell, using vanilla JavaScript and Canvas 2D. No external assets, libraries, or network requests.

RENDERING
- Draw everything to an offscreen canvas at a fixed logical resolution of 128x96, then blit to a fullscreen display canvas scaled by the largest integer factor that fits the window, centered, with imageSmoothingEnabled = false and CSS image-rendering: pixelated.
- All drawing snaps to integer coordinates on the logical canvas. No sub-pixel positions, anti-aliasing, gradients, or shadowBlur.
- Fixed palette of ~24 hex colors: deep blues/purples for night sky, warm robe tones, 3-4 bright magic colors. Every pixel comes from this palette.

CHARACTER
- Build the wizard procedurally from filled rects and pixel runs, ~24x32 logical pixels: pointed hat with a bend, long beard, two-shade robe with darker outline, staff with a gem at the tip.
- Parameterize the pose (staff angle, arm raise, head tilt, robe sway). Animate parameters smoothly, then quantize to the pixel grid each frame so motion reads at an 8-12 fps pixel animation feel even though the loop runs at 60fps.

ANIMATION
- Looping state machine: IDLE (2-frame bob, beard sway) -> CHARGE (staff raises, gem flickers, sparks spiral inward) -> CAST (bright burst, projectile fires across the scene, 1-2 pixel screen shake) -> RECOVER (settle back). Ease pose parameters between keyframes.
- Pooled allocation-free particle system: preallocate and reuse. Sparks orbit the gem during CHARGE, explode outward on CAST, each particle stepping its palette index from white to magic color to dark before despawn. Snap particle positions to the grid when drawing.
- Fixed 60hz timestep update with rAF rendering. Zero object allocation inside the loop.

SCENE
- Minimal background: dark sky, a few twinkling 1px stars, moon, stone floor line. Character silhouette must read clearly.
- Subtle 1px rim light on the wizard from the gem, brightening during CHARGE and CAST.

QUALITY BAR
- Crisp pixels at any window size, seamless loop, stable 60fps, readable silhouette. Should look like a polished 16-bit sprite animation, not vector shapes scaled down.
```

</details>

#### 18. 交互式史前岛屿（Three.js）

作者：Vib3Coded · [原帖](https://x.com/vib3coded/status/2102450842070569099) · [单独文件](prompts/18-prehistoric-island-threejs.md)

原本用于和其他模型横向对比，也可以作为三维场景提示词的写法参考。

<details>
<summary>展开提示词（4131 字符）</summary>

```text
Create a beautiful, highly detailed, fully interactive 3D prehistoric island using Three.js and WebGL. Deliver everything in a single standalone HTML file that opens directly in Chrome. Embed assets wherever possible.

VISUAL DIRECTION
Build a large, rounded island surrounded by an ocean with a transparent underwater cross-section. The result should feel like a premium miniature world: lush vegetation, expressive dinosaurs, rich materials, atmospheric lighting, and polished animation. Use a cohesive, stylized art direction rather than basic geometric shapes.
ISLAND
Create varied terrain with beaches, rocky cliffs, dense prehistoric forests, giant ferns, a waterfall, a freshwater pond, and a volcano. Add a small research station, wooden walkways, observation platforms, supply crates, and dinosaur nests. Make the island spacious enough for dinosaurs to move naturally between distinct areas.

WATER CROSS-SECTION
The water must form a deep, rounded volume around the island, with clearly visible underwater scenery through its sides. Include a textured seabed, rocks, aquatic plants, fish, bubbles, and a green marine reptile swimming beneath the surface. Do not place ordinary land dinosaurs underwater, and do not add a submarine.
Use animated waves, Fresnel reflections, underwater light patterns, shoreline foam, and splashes. Avoid transparency sorting artifacts and visible gaps between the island and water.

DINOSAURS
Include several distinct species, such as a long-necked sauropod, Triceratops, Stegosaurus, a large theropod, and smaller herd animals. Add pterosaurs circling overhead.
Give every species recognizable anatomy, shaped bodies, articulated limbs, detailed heads, tails, and appropriate skin patterns. Avoid assembling the finished dinosaurs from obvious boxes or disconnected spheres.

NATURAL ANIMATION
Use hierarchical skeletons with correctly positioned joints. Walking must have distinct stance and swing phases: feet stay planted during contact and lift cleanly during each step. Match stride length to movement speed.

Use terrain sampling and inverse kinematics to keep feet on the ground. Add weight shifts, subtle body movement, balanced tail motion, head turns, and breathing. Dinosaurs must never float, slide, intersect the ground, or walk through buildings, rocks, trees, or each other.
Use obstacle avoidance and safe paths. Different species should have different movement speeds, gait patterns, and behaviors. Marine animals must face their direction of travel.

INTERACTION
Allow users to:

Rotate the camera freely, zoom, and inspect the underwater cross-section.
Select a dinosaur and follow it with a smoothly moving camera.

Place food in suitable locations and watch nearby dinosaurs approach and eat.

Trigger drinking, resting, calling, and herd movement.

Explore nests and watch a hatchling emerge.
Trigger a marine reptile surfacing with a splash.
Switch between daylight, sunset, and night.
Adjust rain, wind, and volcanic activity.
Pause the simulation and reset the scene.
Make every control produce a clear, visible response. Keep interactions repeatable and prevent overlapping animations from breaking character poses.
ATMOSPHERE AND AUDIO
Add moving foliage, drifting clouds, birds, insects, rain particles, and warm research-station lights at night. Include quiet atmospheric music and environmental sounds with a working music toggle and volume slider. Start audio only after user interaction.
INTERFACE
Use a compact, elegant interface with English labels. Keep the scene dominant and avoid large panels covering the island. Make the layout responsive for desktop and mobile.
TECHNICAL QUALITY
Use instancing for repeated vegetation and props, efficient geometry, appropriate shadows, and restrained post-processing. Balance visual richness with smooth real-time performance.
Build a complete scene, not a mockup. Test the final HTML directly in a desktop browser, inspect screenshots and the console, exercise every interaction, and fix loading errors, floating dinosaurs, foot sliding, broken collisions, water artifacts, and camera problems before delivery.
```

</details>

## 🛠 技术路线

| 路线 | 工具栈 | 代表案例 |
|---|---|---|
| 单 HTML + Canvas/JS 逐帧绘制 | 原生 JS、Canvas 2D、Web Audio；Playwright/Puppeteer 截帧 + FFmpeg | 像素巫师、彩虹路、特殊相对论、鸡尾酒图解、UI 形态变换 |
| p5.js + 笔刷库画“手绘”动画 | p5.js、p5.brush（水彩/铅笔笔触）、无头 Chrome、FFmpeg | P(doom) MV、Let Me Go MV、Opus 的一生 |
| Remotion（React 写视频） | React/TypeScript、SVG、Canvas、Remotion Studio、可上 AWS 云渲染 | AI 发展史 3 分钟短片、Danny Stuart 的 App 宣传片 |
| HyperFrames 渲染 HTML 视频 | HyperFrames、单个 index.html、Python 合成音乐 | Shotbase 发布视频、Small Print 动画 |
| Manim 数学/论文讲解 | Manim、Kokoro-82M TTS、FFmpeg | Deedy 的论文动画讲解 |
| Python 逐像素画线稿 | Python（PIL 等）、TTS、FFmpeg | 中华五千年、大气环流、口播转线稿 |
| Three.js/WebGL 三维场景 | Three.js、程序化模型/纹理/音效 | 奥斯特里茨战役、史前岛屿、安提基特拉机械 |
| 操控专业软件 | After Effects、Blender、Higgsfield、Runway MCP、Seedance API | AE 发布广告、Blender 程序化镜头、超级智能纪录片 |
| 剪辑已有素材 | browser-use/video-use、FFmpeg | 13 条原始素材剪成发布视频 |

## 🎬 案例总览

共 54 条，“—”表示原帖没有披露。多数视频可以在 [awesome-claude-video](https://github.com/opusvideo/awesome-claude-video) 里直接播放。结构化数据见 [`cases.json`](cases.json)。

| 类别 | 案例 | 作者 | 实现方式 / 要点 | 耗时成本 |
|---|---|---|---|---|
| 产品广告 | [推理创业公司发布视频](https://x.com/deedydas/status/2102787937482252537) | Deedy | 一句话提示，模型自选工具 | 1 分钟，约 2 美元 |
| 产品广告 | [网站改版汇成预告片](https://x.com/trq212/status/2102477340920152162) | trq212 | 先迭代评审多个网站改版方案，再汇成预告片 | — |
| 产品广告 | [Shotbase 产品发布视频](https://x.com/Miguel07Code/status/2102441708395041170) | Miguel07Code | Opus 5.5 + HyperFrames | — |
| 产品广告 | [可继续编辑的 AE 发布广告](https://x.com/seiiiiiiiiiiru/status/2102636308707287201) | SEIIIRU | Claude 操作 Higgsfield 与 After Effects，工程可在 AE 内继续改 | Pro 套餐 5% 用量，约 150 日元 |
| 产品广告 | [旁白驱动的 AE 广告](https://x.com/seiiiiiiiiiiru/status/2103227982592831846) | SEIIIRU | Gemini 3.8 Flash TTS 生成旁白，Claude 在 AE 中配画面、音乐、音效 | — |
| 产品广告 | [BLVCKOUT 非官方广告](https://x.com/ystknsh/status/2102766871007436993) | ystknsh | MulmoCast 出片，Opus 写脚本和动画，Gemini 出图和配音，ElevenLabs 配乐 | — |
| 产品广告 | [Mole 产品宣传片](https://x.com/berryxia/status/2103419787565216023) | Berryxia | 把“输入产品，产出宣传片”封装成可复用 Skill | — |
| 产品广告 | [App 宣传片两支](https://dannystuart.substack.com/p/claude-code-opus-remotion-agentic-promo-video) | Danny Stuart | Remotion，先出分镜再写代码 | 每支约 10 分钟 |
| 产品广告 | [润唇膏广告（对比 GPT-6 Astra）](https://x.com/higgsfield_ai/status/2102913101926731879) | Higgsfield AI | 同一套品牌素材，在 AE 里做 20 秒卡点产品片 | — |
| 产品广告 | [30 秒企业讲解片模板](https://x.com/alex_prompter/status/2103499977632997524) | Alex Prompter | 单 HTML，5 个场景，对话内播放后录屏 | — |
| 动态图形 | [15 秒动态设计作品集](https://x.com/stephanlivera/status/2103315922098470926) | Stephan Livera | Max effort，一句话 | — |
| 动态图形 | [无缝 UI 形态变换循环](https://x.com/twoclipping/status/2103273003555402193) | zero | 完整模板，Playwright + FFmpeg tmix 动态模糊 | — |
| 科普讲解 | [交互式相机镜头实验室](https://x.com/RyanSael/status/2102591147927654847) | Ryan Sael | 一次成型的可交互镜头模拟 | 1 小时 26 分钟，API 费用 25.66 美元 |
| 科普讲解 | [研究论文动画讲解](https://x.com/deedydas/status/2103141339651350646) | Deedy | Claude 自选 Manim、Kokoro-82M 和 FFmpeg，在网页对话里完成 | — |
| 科普讲解 | [AI 发展史 3 分钟短片](https://x.com/kimmonismus/status/2102844654169575547) | Chubby (kimmonismus) | 约 7400 行 React/TS（Remotion），SVG/Canvas 绘制，开源 TTS，Python 配乐 | 约 1 小时，周额度 7% |
| 科普讲解 | [中华五千年历史速览](https://x.com/akokoi1/status/2102583898865873225) | WY | 一句话，线稿 + 音乐 | — |
| 科普讲解 | [大气环流讲解（近 5 分钟）](https://x.com/akokoi1/status/2102606609574941028) | WY | 线稿 + TTS 旁白 + 中英字幕 | 26 分钟，token 消耗很低 |
| 科普讲解 | [物理竞赛压轴题讲解](https://x.com/akokoi1/status/2102680453912449223) | WY | 复用大气环流提示词，换成具体题目 | — |
| 科普讲解 | [Negroni 鸡尾酒动态图解](https://x.com/Ror_Fly/status/2102853258582880547) | Rory Flynn | 1 张参考图，30 秒 HTML 动画 | — |
| 科普讲解 | [46 秒讲特殊相对论（日文）](https://x.com/masahirochaen/status/2102722719502704941) | チャエン | 参考推文 + 简短指令，Canvas 画 1395 帧，BGM 和音效都由 JS 生成 | 渲染约 2 分钟 |
| 科普讲解 | [奥斯特里茨战役电影](https://x.com/WinterArc2125/status/2103116235009347650) | Winter | WebGL + Kokoro 旁白，代码开源 | — |
| 科普讲解 | [口播改线稿动画讲解](https://x.com/AxtonLiu/status/2102827887732932956) | Axton | Python 逐帧画线稿，约 30 个镜头，保留原声和字幕 | 28 分 53 秒，人工介入 0 次 |
| 科普讲解 | [Transformer 讲解视频](https://youmind.com/opus-5-5-prompts) | 宝玉 | 用 JS 做视频 | — |
| 科普讲解 | [从房间放大到夸克](https://youmind.com/opus-5-5-prompts) | Taelin | 多尺度连续推镜 | — |
| 叙事动画 | [你热爱什么？](https://x.com/kevin_t_ngo/status/2102437977435893771) | Kevin Ngo | JS 逐帧手绘风动画 | — |
| 叙事动画 | [像素巫师](https://x.com/majidmanzarpour/status/2102476258948927543) | Majid Manzarpour | 原生 JS + Canvas 2D，单 HTML | — |
| 叙事动画 | [火星探测器短片](https://x.com/AndrewOnXYZ/status/2102512879258009818) | AndrewOnXYZ | 代码渲染短片 | — |
| 叙事动画 | [Opus 的一生](https://x.com/shfred0/status/2102495989194236158) | shfred0 | 让 Claude 讲自己从诞生到现在的一生，JS 笔触逐帧绘制 | — |
| 叙事动画 | [想象如何解决难题](https://x.com/chetaslua/status/2102478640428773861) | chetaslua | 代码动画 | — |
| 叙事动画 | [Small Print（字里行间）](https://x.com/Voxyz_ai/status/2102531681450119426) | Vox | 单个 index.html，HyperFrames 渲染，Python 合成音乐，逐秒复查打磨 | — |
| 叙事动画 | [啤酒节 30 秒动画](https://x.com/cherry_mx_reds/status/2102493303388475855) | Tak | 角色截图 + 本地音频采样 | — |
| 叙事动画 | [一滴雨的故事](https://x.com/aollivier82/status/2102498589259821559) | aollivier82 | 代码动画 | — |
| 叙事动画 | [小蝌蚪找妈妈（水墨）](https://x.com/akokoi1/status/2102699703309898026) | WY | 水墨风代码动画 | — |
| 叙事动画 | [Rain Station 30 秒 2D 分镜短片](https://youmind.com/opus-5-5-prompts) | Feicai | 2D 动画故事板预览片 | — |
| 艺术/3D | [轨道中的世界](https://x.com/devteamdrew/status/2102436464323661880) | devteamdrew | 纯 JS 动画 | — |
| 艺术/3D | [安提基特拉机械海底探索](https://x.com/edwinarbus/status/2102463453176979794) | edwin | Three.js：2047 条鱼、2.5 万片草叶、4.7 万个粒子、30 个齿轮 | — |
| 艺术/3D | [投石机草图转交互模拟](https://x.com/poolio/status/2102445641205248145) | poolio | 从草图生成物理模拟 | — |
| 艺术/3D | [彩虹路像素跑酷](https://x.com/riku720720/status/2102515055116063144) | Rikuo | 超长规格型日文提示词 | — |
| 艺术/3D | [会动的海岸画](https://x.com/strawhatsu4/status/2102457111787745405) | strawhatsu4 | 代码绘画动画 | — |
| 艺术/3D | [丙烯画风新西兰游记](https://x.com/ann_nnng/status/2102573127192727704) | Ann Nguyen | 旅行照片转丙烯画风，JS 绘制 | — |
| 艺术/3D | [Blender 外骨骼 / 风车 / 眼球解剖](https://x.com/higgsfield_ai/status/2102449278283313303) | Higgsfield AI | Claude 操作 Blender 建模和做动画 | — |
| 艺术/3D | [Blender 程序化 10 秒镜头](https://x.com/Stefan_3D_AI/status/2102471841046786153) | Stefan 3D AI | 只用 Blender、全程序化，外加录制搭建延时 | 35 分钟，19.96 万输出 token，约 13.3 美元 |
| 艺术/3D | [史前岛屿交互场景](https://x.com/vib3coded/status/2102450842070569099) | Vib3Coded | Three.js，单 HTML | — |
| 音乐 MV | [I'm Upping My P(doom)](https://github.com/JohnHeibel/PDoomVideo) | NotinReality / JohnHeibel | p5.js + p5.brush，无头 Chrome 截帧，FFmpeg 合成；156.6 秒，约 3760 帧；跑了两轮 | 10% Max 5x 周额度 |
| 音乐 MV | [《Let Me Go》动画 MV](https://linux.do/t/topic/2943096) | Linux.do 网友 | 上传歌词和音频，effort xhigh，p5.js 逐帧绘制，人工反馈改角色 | 初版 45 分钟，约 200 美元 |
| 音乐 MV | [Claude Pop 混合流程 MV](https://x.com/donaldjewkes/status/2102801274173587569) | donald | fal 角色图 + Seedance 2.5 底片 + JS 逐帧重绘 | fal 预算约 2000 美元 |
| 音乐 MV | [Suno 作曲 + Opus 作词做 MV](https://www.bilibili.com/video/BV1qihf6rE6f/) | B 站 UP 主 | Suno 编曲演唱，Opus 5.5 作词并制作 MV | — |
| 音乐 MV | [EVA 风竖屏歌词视频](https://youmind.com/opus-5-5-prompts) | kurahu | 歌词本身作为主角的竖屏 MV | — |
| 纪录/剪辑 | [5 分钟超级智能纪录片](https://x.com/gavinpurcell/status/2103304514329854102) | Gavin Purcell | 接 Runway MCP，“面向普通人的 Netflix 风纪录片” | — |
| 纪录/剪辑 | [13 条原始素材剪成发布视频](https://x.com/gregpr07/status/2102984873351037161) | gregpr07 | video-use 挑片段，剪辑、调色、字幕 | — |
| B 站合集 | [地球 46 亿年进化史](https://www.bilibili.com/video/BV1Vfau6iE9Q/) | B 站 UP 主 | 代码动画 | — |
| B 站合集 | [群论之美宣传片](https://www.bilibili.com/video/BV12Zhm6oE6m/) | B 站 UP 主 | 代码动画 | — |
| B 站合集 | [“瘫坐长椅看到原子弹爆炸”动画](https://www.bilibili.com/video/BV1jyaA6QEoH/) | B 站 UP 主 | 代码动画 | — |
| B 站合集 | [一句话生成的 MV](https://www.bilibili.com/video/BV1EDhW6LEYU/) | B 站 UP 主 | 一句话 MV | — |

## 💡 写法经验

- **先分镜，后代码。** 高质量案例基本都要求先交分镜或节拍表，确认后再写代码。这样后面可以只改某一个镜头。
- **像导演一样给结构。** 写清总时长、场景数、每个场景讲什么。给参考视频或参考图，比堆形容词好用。多用 dramatic cuts、match cut、kinetic typography 这类镜头语言。
- **列禁用清单。** 比如粒子爆炸、RGB 分离、镜头光晕、霓虹辉光、弹跳缓动。模板味大多来自这些。
- **确定性渲染。** 每一帧必须只由时间 t 决定（`seek(t)`）：不用 CSS transition 和计时器，帧与帧之间不保存状态，否则并行渲染会闪。可参考 [PDoomVideo 的 ANIMATION_GUIDE.md](https://github.com/JohnHeibel/PDoomVideo/blob/main/ANIMATION_GUIDE.md)。
- **让它自己看片、自己返工。** 正式渲染前先抽查关键帧截图，修掉重叠、拥挤、看不清的地方。
- **给足推理强度和工具。** effort 开到 high 以上。TTS、音乐、视频模型的 API 文档放进项目目录，key 放在 `.env` 里。安全起见，在 `.claude/settings.json` 加一条 `"deny": ["Read(./.env)"]`。
- **做成 Skill 复用。** HyperFrames、Remotion 都有现成的 Agent Skill；也可以把“输入产品 → 输出宣传片”封装成自己的 Skill。

## ⚠️ 局限与成本

- 出来的是动态图形，不是写实视频。
- 产物是代码，本地要有 Node、浏览器、FFmpeg 才能变成 MP4。
- 成本差距很大：一句话短片几美元；几分钟的 MV 单次会话可能到 200 美元，或占 Max 周额度的 7%–10%。
- 所谓“一次成型”，很多其实跑了两轮以上，预算按多轮迭代来估比较稳。

## 📚 资料来源

- [awesome-claude-video（中英双语案例合集）](https://github.com/opusvideo/awesome-claude-video)
- [YouMind：Claude Opus 5.5 提示词库](https://youmind.com/opus-5-5-prompts)
- [Danny Stuart：Agentic video production with Claude Code and Opus](https://dannystuart.substack.com/p/claude-code-opus-remotion-agentic-promo-video)
- [OrcaRouter：What “Plan a Video” Actually Produces](https://www.orcarouter.ai/blog/claude-opus-5-5-video-plan-one-shot)
- [SlopTV：Opus 5.5 drew a 30-second Negroni explainer in HTML](https://sloptvnews.com/opus-5-5-negroni-explainer-html-motion-graphics-iteration/)
- [80aj：Claude Opus 5.5 自制动画 MV 走红](https://www.80aj.com/2026/09/25/claude-opus-animation-mv/)
- [新浪科技：实测 Opus 5.5](https://finance.sina.com.cn/tech/roll/2026-09-25/doc-inisyuqm4676290.shtml)
- [Linux.do：Opus 5.5 为歌曲逐帧画出动画 MV](https://linux.do/t/topic/2943096)
- [PDoomVideo 仓库](https://github.com/JohnHeibel/PDoomVideo)
- [Battle-of-Austerlitz-Film 仓库](https://github.com/WinterArc21/Battle-of-Austerlitz-Film)
- [riba2534/claude-opus-5-5-demo（3D 游戏，附中文提示词）](https://github.com/riba2534/claude-opus-5-5-demo)

## 🤝 贡献

欢迎提 PR 补充新案例。请附上原帖链接，只提交作者本人公开的提示词。

## 声明

所有提示词和视频作品的版权归原作者所有，本仓库只做索引和整理。原作者如不希望被收录，请开 issue，会尽快删除。

---

整理：[向阳乔木](https://github.com/joeseesun) · 2026-09-27
