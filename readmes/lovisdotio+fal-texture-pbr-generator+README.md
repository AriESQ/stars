# PATINA — AI PBR Texture Generator

Generate production-ready PBR texture maps from images or text descriptions. Preview materials in real-time on an interactive 3D sphere, then download maps ready for Substance Designer, Substance Painter, Blender, Unreal Engine, and Unity.

## Features

- **Text to Material** — Describe any material and get seamless, tileable PBR maps
- **Image to PBR** — Upload a photo or render to extract all PBR channels
- **Real-time 3D Preview** — Interactive WebGL sphere with full PBR material applied (auto-rotates, drag to orbit)
- **Substance Designer / Painter Ready** — Download as ZIP with standard naming convention (`BaseColor`, `Normal`, `Roughness`, `Metallic`, `Height`)
- **Individual Downloads** — Download any map individually as PNG
- **Bring Your Own Key** — Enter your fal.ai API key directly in the browser (never stored server-side)

## Generated Maps

| Map | Description | Use in Substance |
|-----|-------------|-----------------|
| **Base Color** | Albedo / Diffuse color | BaseColor channel |
| **Normal** | Surface detail normals | Normal channel |
| **Roughness** | Surface roughness | Roughness channel |
| **Metallic** | Metallic regions | Metallic channel |
| **Height** | Displacement / bump | Height channel |

## Getting Started

### Prerequisites

- Node.js 18+
- A fal.ai API key — [get one free here](https://fal.ai/dashboard/keys)

### Local Development

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/fal-texture-pbr-generator.git
cd fal-texture-pbr-generator

# Install dependencies
npm install

# (Optional) Set a default API key
cp .env.local.example .env.local
# Edit .env.local and add your FAL_KEY

# Start the dev server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) and enter your fal.ai API key to start generating.

### Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/fal-texture-pbr-generator&env=FAL_KEY&envDescription=Optional%20default%20fal.ai%20API%20key.%20Users%20can%20also%20enter%20their%20own%20key%20in%20the%20UI.&envLink=https://fal.ai/dashboard/keys)

1. Click the deploy button
2. Optionally add a `FAL_KEY` environment variable (users can also enter their own key in the UI)
3. Deploy!

## Tech Stack

- **[Next.js](https://nextjs.org)** — App Router, API Routes
- **[Three.js](https://threejs.org)** / **[React Three Fiber](https://r3f.docs.pmnd.rs)** — WebGL 3D preview
- **[Tailwind CSS](https://tailwindcss.com)** — Styling
- **[JSZip](https://stuk.github.io/jszip/)** — Client-side ZIP creation
- **[fal.ai](https://fal.ai)** — PATINA model API

## API Endpoints

### `POST /api/generate`

Generates PBR texture maps.

**Headers:**
- `x-fal-key` — Your fal.ai API key

**Body (FormData):**
- `mode` — `"text"` or `"image"`
- `prompt` — Material description (text mode)
- `image` — Image file (image mode)

## Credits

- **PATINA Model** by [Benjamin](https://x.com/MLPBenjamin)
- **Website** by [Lovis Odin](https://x.com/OdinLovis)
- **Infrastructure** by [fal.ai](https://fal.ai)

## License

MIT
