# ⚗️ Gnomalab: Digital Alchemy Suite

**Shaders ISF para VDMX**

¡Bienvenido a la Digital Alchemy Suite! Esta es una colección personal de shaders en formato ISF (Interactive Shader Format), creados específicamente para la manipulación de señal, la estética glitch y procesos binarios aplicados al vídeo en tiempo real.

---

## 🚀 Sobre el Desarrollo e Inspiración

Este proyecto nace de las ganas de llevar conceptos estéticos y procesos de postproducción tradicional (que normalmente requieren render) directamente al flujo de trabajo en vivo.

Muchos de estos efectos están inspirados en plugins comerciales clásicos de After Effects y otras plataformas de composición, pero "hackeados" y portados a ISF para que el píxel sea modelado en el momento, bajo el calor del directo. Encontrarás desde distorsiones matemáticas puras hasta homenajes a la arqueología mediática, como el procesamiento de barrido analógico de los Vasulka y su mítico sintetizador Rutt-Etra.

**Nota sobre la autoría:** Yo no soy programador. Esta suite es el resultado de una colaboración creativa con Gemini (Google AI). Ella ha actuado como el puente técnico para materializar las ideas, estructuras y lógicas que yo tenía en mente pero no sabía cómo escribir en código. Este flujo de trabajo es una prueba de cómo la IA puede empoderar a los artistas para que podamos fabricar nuestras propias herramientas.

---

## 🛠️ Compatibilidad y Rendimiento

- **Testado en:** VDMX6 Plus.
- **Compatibilidad:** Debería funcionar perfectamente en VDMX6, VDMX5 y cualquier software que soporte el estándar ISF (aunque no han sido probados fuera de VDMX).
- **Rendimiento:** ¡Ojo! Algunos shaders son computacionalmente pesados, especialmente los que tienen procesos encadenados (multi-pass) o feedback persistente. El rendimiento dependerá directamente de la potencia de tu GPU.
- **Interfaz (UI):** Como son herramientas de uso personal original, algunos parámetros están en español. Siéntete libre de editarlos o renombrarlos si te resulta más cómodo.

---

## 📥 Cómo Instalar en VDMX

### Instalación Automática (Recomendada)

1. Clona o descarga este repositorio:
   ```bash
   git clone https://github.com/Gnomalab/VDMX-ISF-Effects-Suite.git
   ```

2. Copia toda la carpeta `ISF` a la ubicación de shaders de VDMX:
   ```bash
   cp -r ISF/* ~/Library/Graphics/ISF/
   ```

3. Reinicia VDMX y los shaders aparecerán en tu biblioteca de FX.

### Instalación Manual

1. Descarga el repositorio como ZIP desde GitHub.
2. Ve a `~/Library/Graphics/ISF/` en tu Mac (puedes usar `Cmd+Shift+G` en Finder).
3. Arrastra las carpetas individuales de shaders desde `ISF/` a esa ubicación.
4. Reinicia VDMX.

**💡 Tip:** Cada shader incluye su propio README con descripción técnica completa en inglés y español.

---


## 📂 El Laboratorio (Catálogo de Efectos)

He dividido la suite en estas categorías principales para que te sea fácil navegar por ellas dentro de VDMX:

### 1. Pixel Sorting & Vector Flow 🌊
- **Gn PixSort S3:** Mi versión más avanzada. Olvídate de las líneas rectas; aquí hay espirales, vórtices y campos magnéticos.
- **Gn PixSort Flow Mapper:** El movimiento lo dicta una segunda imagen. Control total del flujo.
- **Gn PixelSort Clean:** Para cuando necesitas ordenación pero quieres mantener el fondo intacto.

### 2. Glitch & Vandalismo Digital 👾
- **Gn Vandalizer:** Destrucción selectiva. Slices, Melt y TV Warp focalizados por máscaras de precisión.
- **Gn XOR Smear:** Corrupción bitwise pura. Texturas que parecen nacer del propio error del dato.
- **Gn Glitch Control:** La "navaja suiza" para desplazamientos RGB, estiramientos y copias.

### 3. Síntesis de Vídeo y Señal 📺
- **Gn Vasulka Synth:** Un viaje al Rutt-Etra. Transforma el vídeo en una escultura topográfica 3D vibrante.
- **Gn Modulation Pro:** Trata el vídeo como voltaje. Modulación analógica con espacios de color CMYK y HSV.
- **Gn Triple Alchemy:** Una matriz de ruteo para aplicar distintos procesos a negros, medios y blancos de forma independiente.

### 4. Deformación Temporal y Feedback 🌀
- **Gn Slit-Scan Master:** Escaneo de rendija con deformación por mapas. El tiempo ya no es lineal.
- **Gn Pixel Melt:** Derretido viscoso con gravedad 360°.
- **Gn Topo Lines:** Generador de curvas de nivel rítmicas inspiradas en la cartografía técnica.

## 👤 Créditos

- **Concepto y Dirección Artística:** Gnomalab
- **Puente Técnico & Thought Partner:** Gemini AI
- **Web:** [www.gnomalab.es](http://www.gnomalab.es/)
- **Instagram:** [@gnomalab](https://www.instagram.com/gnomalab)
- **Youtube:** [Gnomalab](https://www.youtube.com/@gnomalab)

---

2026 Gnomalab. Hecho por un artista, para artistas.  
**Licencia MIT** — Úsalo, modifícalo, compártelo. Si te ayuda en tu arte, considera invitarme a una birra 🍺
