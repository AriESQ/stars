# SurfaceLevel 2.0
 An image converter primarily for video-game development and general image resampling/conversion.

* The only tool that supports `VK_FORMAT_R64_SFLOAT`, `VK_FORMAT_R64G64_SFLOAT`, `VK_FORMAT_R64G64B64_SFLOAT`, and `VK_FORMAT_R64G64B64A64_SFLOAT`. An entirely 64-bit double pipeline is used!
* The only resampler to allow different filters for width, height, and depth, and for color channels and the alpha channel.  Use an exclusive custom filter for a sharp color down-sample, but use bilinear filtering for the alpha channel!
* Provides the mostest fastest texture-compression routines.  Other tools may take 40 minutes to convert a 4K texture to BC7, while SurfaceLevel 2.0 takes only 20 seconds while producing a better result!
* The supported colorspaces, resampling filters, and texture-addressing modes is exhaustive.  37 built-in colorspaces, 29 resampling filters, and 6 texture-addressing modes.
* Almost all texture formats for Vulkan, Metal, OpenGL, and Direct3D 12 are supported.  Literally hundreds of formats, and more to come!
* Normal-map generation, swizzling, channel swapping, image flipping, pre-multiplying alpha, and more!
* Handles 1-D, 2-D, and 3-D textures, multiple faces, texture arrays, and mipmaps.
* Currently exports to **PNG**, **BMP**, **TGA**, **JPG**, **J2K**, **JP2**, **EXR**, **DDS**, **KTX**, **PVR**, and **YUV** (and variants).
<h2>Commands</h2>

<h3>File</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>-file</td>
    <td>&lt;file path&gt;</td>
    <td>A path to an image file to load and convert. The <em>-file</em>, <em>-yuv_file</em>, and <em>-outfile</em> commands can be used multiple times to load and save multiple files.</td>
  </tr>
  <tr>
    <td>-yuv_file</td>
    <td>&lt;file path&gt;<br>&lt;width&gt; &lt;height&gt;</td>
    <td>
      Path to a YUV file to load. If the extension does not indicate the YUV encoding, then <em>yuv_input_format</em> must be called to specify the YUV encoding.<br>
      Recognized file extensions:<br>
      yuv444p16<br>
      yuv444p12le<br>
      yuv444p10le<br>
      yuv444p<br>
      yuv444y16<br>
      yuv444y12le<br>
      yuv444y10le<br>
      yuv444y<br>
      yuv422p16<br>
      yuv422p12le<br>
      yuv422p10le<br>
      yuv422p<br>
      yuv422y16<br>
      yuv422y12le<br>
      yuv422y10le<br>
      yuv422y<br>
      yuv420p16<br>
      yuv420p12le<br>
      yuv420p10le<br>
      yuv420p<br>
      yuv420y16<br>
      yuv420y12le<br>
      yuv420y10le<br>
      yuv420y<br>
      yuva12le<br>
      yuva10le<br>
      uyvy16<br>
      uyvy12le<br>
      uyvy10le<br>
      uyvy<br>
      y210<br>
      yuy2<br>
      yuy12<br>
      yv12<br>
      p016<br>
      p012<br>
      p010<br>
      nv12<br>
      nv21<br>
      y416<br>
      y410<br>
      avuv<br>
      Extensions other than these will require the format to be explicitly set.
    </td>
  </tr>
  <tr>
    <td rowspan="1">-from_clipboard<br>-from_cb<br>-clipboard_in<br>-cb_in</td>
    <td></td>
    <td>The image is loaded from the system clipboard.</td>
  </tr>
  <tr>
    <td>-outfile</td>
    <td>&lt;file path&gt;</td>
    <td>The path to which to save the file supplied with the last <em>-file</em> command. The destination file format is determined by the file extension.<br>Currently supported formats:<br>PNG<br>BMP<br>TGA<br>JPG<br>J2K<br>JP2<br>EXR<br>DDS<br>KTX<br>PVR<br>YUV (and variants)</td>
  </tr>
  <tr>
    <td rowspan="1">-to_clipboard<br>-to_cb<br>-clipboard_out<br>-cb_out</td>
    <td></td>
    <td>The output file is stored into the system clipboard.</td>
  </tr>
</table>

<h3>Gamma/Colorspaces</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td rowspan="1">-gamma<br>-g</td>
    <td>&lt;gamma&gt;</td>
    <td>Sets the input gamma power. Defaults to <strong>-2.2</strong> (precise sRGB).</td>
  </tr>
  <tr>
    <td>-targetgamma</td>
    <td>&lt;gamma&gt;</td>
    <td>Sets the output gamma power.<br>Defaults to <strong>-2.2</strong> (precise sRGB).</td>
  </tr>
  <tr>
    <td>-rgbe<br>-linear</td>
    <td></td>
    <td>Sets the source and output gamma to 0.0.</td>
  </tr>
  <tr>
    <td>-srgb</td>
    <td></td>
    <td>Sets the source gamma to -2.2 (precise sRGB).</td>
  </tr>
  <tr>
    <td>-target_srgb</td>
    <td></td>
    <td>Sets the output gamma to -2.2 (precise sRGB).</td>
  </tr>
  <tr>
    <td rowspan="36">-input_colorspace</td>
    <td>sRGB<br>sRGB_precise</td>
    <td>Sets the source colorspace profile to an accurate no-gap sRGB.</td>
  </tr>
  <tr>
    <td>sRGB_std<br>sRGB_standard</td>
    <td>Sets the source colorspace profile to the standard sRGB.</td>
  </tr>
  <tr>
    <td>smpte_170<br>smpte_170m</td>
    <td>Sets the source colorspace profile to an accurate no-gap SMPTE 170M-1999.</td>
  </tr>
  <tr>
    <td>smpte_170_std<br>smpte_170m_std<br>170m_std<br>smpte_170_standard<br>smpte_170m_standard<br>170m_standard</td>
    <td>Sets the source colorspace profile to the standard SMPTE 170M-1999.</td>
  </tr>
  <tr>
    <td>rec709<br>rec.709<br>bt709<br>bt.709<br>itu_bt709<br>itu_bt.709</td>
    <td>Sets the source colorspace profile to an accurate no-gap ITU-R Recommendation BT.709-5.</td>
  </tr>
  <tr>
    <td>rec709_std<br>rec.709_std<br>bt709_std<br>bt.709_std<br>itu_bt709_std<br>itu_bt.709_std</td>
    <td>Sets the source colorspace profile to the standard ITU-R Recommendation BT.709-5.</td>
  </tr>
  <tr>
    <td>adobe<br>adobergb<br>adobe_rgb</td>
    <td>Sets the source colorspace profile to Adobe RGB (1998) Color Image Encoding Version 2005-05.</td>
  </tr>
  <tr>
    <td>bt2020<br>bt.2020<br>itu_bt2020<br>itu_bt.2020</td>
    <td>Sets the source colorspace profile to an accurate no-gap ITU-R Recommendation BT.2020.</td>
  </tr>
  <tr>
    <td>bt2020_std<br>bt.2020_std<br>itu_bt2020_std<br>itu_bt.2020_std</td>
    <td>Sets the source colorspace profile to the standard ITU-R Recommendation BT.2020.</td>
  </tr>
  <tr>
    <td>dcip3<br>dci-p3<br>dci_p3</td>
    <td>Sets the source colorspace profile to SMPTE RP 431-2:2011.</td>
  </tr>
  <tr>
    <td>smpte_240<br>smpte_240m<br>240m</td>
    <td>Sets the source colorspace profile to an accurate no-gap SMPTE 240M-1999.</td>
  </tr>
  <tr>
    <td>smpte_240_std<br>smpte_240m_std<br>240m_std<br>smpte_240_standard<br>smpte_240m_standard<br>240m_standard</td>
    <td>Sets the source colorspace profile to the standard SMPTE 240M-1999.</td>
  </tr>
  <tr>
    <td>ntsc_1953<br>ntsc1953</td>
    <td>Sets the source colorspace profile to an accurate no-gap NTSC 1953.</td>
  </tr>
  <tr>
    <td>ntsc_1953_std<br>ntsc1953_std<br>ntsc_1953_standard<br>ntsc1953_standard</td>
    <td>Sets the source colorspace profile to the standard NTSC 1953.</td>
  </tr>
  <tr>
    <td>tech_3213<br>tech3213</td>
    <td>Sets the source colorspace profile to an accurate no-gap EBU Tech. 3213.</td>
  </tr>
  <tr>
    <td>tech_3213_std<br>tech3213_std<br>tech_3213_standard<br>tech3213_standard</td>
    <td>Sets the source colorspace profile to the standard EBU Tech. 3213.</td>
  </tr>
  <tr>
    <td>displayp3<br>display-p3<br>display_p3</td>
    <td>Sets the source colorspace profile to an accurate no-gap Display P3 Color Encoding (v 1.0).</td>
  </tr>
  <tr>
    <td>displayp3_std<br>display-p3_std<br>display_p3_std<br>displayp3_standard<br>display-p3_standard<br>display_p3_standard</td>
    <td>Sets the source colorspace profile to the standard Display P3 Color Encoding (v 1.0).</td>
  </tr>
  <tr>
    <td>rec601<br>rec.601<br>bt601<br>bt.601<br>itu_bt601<br>itu_bt.601</td>
    <td>Sets the source colorspace profile to an accurate no-gap ITU-R Recommendation BT.601 (525).</td>
  </tr>
  <tr>
    <td>rec601_std<br>rec.601_std<br>bt601_std<br>bt.601_std<br>itu_bt601_std<br>itu_bt.601_std</td>
    <td>Sets the source colorspace profile to the standard ITU-R Recommendation BT.601 (525).</td>
  </tr>
  <tr>
    <td>rec601_pal<br>rec.601_pal<br>bt601_pal<br>bt.601_pal<br>itu_bt601_pal<br>itu_bt.601_pal</td>
    <td>Sets the source colorspace profile to an accurate no-gap ITU-R Recommendation BT.601 (625).</td>
  </tr>
  <tr>
    <td>rec601_pal_std<br>rec.601_pal_std<br>bt601_pal_std<br>bt.601_pal_std<br>itu_bt601_pal_std<br>itu_bt.601_pal_std</td>
    <td>Sets the source colorspace profile to the standard ITU-R Recommendation BT.601 (625).</td>
  </tr>
  <tr>
    <td>generic_film<br>film</td>
    <td>Sets the source colorspace profile to generic film.</td>
  </tr>
  <tr>
    <td>bt470_ntsc<br>bt470_m_ntsc</td>
    <td>Sets the source colorspace profile to an accurate no-gap Rec. ITU-R BT.470-6 (M/NTSC).</td>
  </tr>
  <tr>
    <td>bt470_pal<br>bt470_m_pal</td>
    <td>Sets the source colorspace profile to an accurate no-gap Rec. ITU-R BT.470-6 (M/PAL).</td>
  </tr>
  <tr>
    <td>bt470_b<br>bt470_b1<br>bt470_d<br>bt470_d1<br>bt470_g<br>bt470_h<br>bt470_k<br>bt470_k1<br>bt470_l<br>bt470_n_pal<br>bt470_secam<br>bt470_l_secam</td>
    <td>Sets the source colorspace profile to an accurate no-gap Rec. ITU-R BT.470-6 (B, B1, D, D1, G, H, K, N/PAL, K1, L/SECAM).</td>
  </tr>
  <tr>
    <td>ntsc_1987<br>smpte_c</td>
    <td>Sets the source colorspace profile to SMPTE C with a pow(2.2) curve.</td>
  </tr>
  <tr>
    <td>ntsc_1987_std<br>smpte_c_std</td>
    <td>Sets the source colorspace profile to the standard SMPTE C.</td>
  </tr>
  <tr>
    <td>romm_rgb<br>rommrgb</td>
    <td>Sets the source colorspace profile to Reference Output Medium Metric RGB (ROMM RGB).</td>
  </tr>
  <tr>
    <td>rimm_rgb<br>rimmrgb</td>
    <td>Sets the source colorspace profile to Reference Input Medium Metric RGB (RIMM RGB).</td>
  </tr>
  <tr>
    <td>erimm_rgb<br>erimmrgb</td>
    <td>Sets the source colorspace profile to Extended Reference Input Medium Metric RGB (ERIMM RGB).</td>
  </tr>
  <tr>
    <td>plasa<br>plasa_ansi</td>
    <td>Sets the source colorspace profile to PLASA ANSI E1.54.</td>
  </tr>
  <tr>
    <td>protune<br>gopro</td>
    <td>Sets the source colorspace profile to Protune Native (GoPro).</td>
  </tr>
  <tr>
    <td>s-gamut<br>sgamut<br>s_gamut</td>
    <td>Sets the source colorspace profile to S-Gamut.</td>
  </tr>
  <tr>
    <td>s-gamut3<br>sgamut3<br>s_gamut3</td>
    <td>Sets the source colorspace profile to S-Gamut3.</td>
  </tr>
  <tr>
    <td>s-gamut3cine<br>sgamut3cine<br>s_gamut3cine<br>s-gamut3_cine<br>sgamut3_cine<br>s_gamut3_cine</td>
    <td>Sets the source colorspace profile to S-Gamut3.Cine.</td>
  </tr>
  <tr>
    <td>-target_colorspace</td>
    <td>Same as for<br><em>-input_colorspace</em></td>
    <td>Sets the output colorspace profile.</td>
  </tr>
  <tr>
    <td>-input_colorspace_file</td>
    <td>&lt;file path&gt;</td>
    <td>Sets the input colorspace profile. Loads .ICC and .ICM files.</td>
  </tr>
  <tr>
    <td>-target_colorspace_file</td>
    <td>&lt;file path&gt;</td>
    <td>Sets the output colorspace profile. Loads .ICC and .ICM files.</td>
  </tr>
  <tr>
    <td>-dont_embed_icc</td>
    <td></td>
    <td>No colorspace profile will be embedded into files with colorspace-profile support.</td>
  </tr>
  <tr>
    <td>-embed_icc</td>
    <td></td>
    <td>Any specified output colorspace profiles will be embedded into files with colorspace-profile support. This is the default.</td>
  </tr>
  <tr>
    <td>-ignore_input_colorspace_gamma</td>
    <td></td>
    <td>The gamma in any supplied or embedded input colorspace profile will be ignored.</td>
  </tr>
  <tr>
    <td rowspan="4">-rendering_intent<br>-render_intent</td>
    <td>perceptual</td>
    <td>All colors are scaled to fit into the target colorspace. Useful for converting from wide colorspaces to more narrow ones.</td>
  </tr>
  <tr>
    <td>relative_colorimetric</td>
    <td>Colors that are not in-gamut for the target colorspace are clipped to the nearest color in-gamut.<br>This is the default.</td>
  </tr>
  <tr>
    <td>saturation</td>
    <td>Colors are preserved in relative luminance and hue, but not necessarily saturation, resulting in higher overall saturation for in-gamut colors.</td>
  </tr>
  <tr>
    <td>absolute_colorimetric</td>
    <td>Not intended for color conversion, but rather typically for digital inkjet proofing.</td>
  </tr>
</table>

<h3>Resampling</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td rowspan="29">-filter</td>
    <td>box<br>point</td>
    <td>Applies the selected filter to all non-mipmap filters.</td>
  </tr>
  <tr>
    <td>tent<br>linear</td>
    <td>The default alpha filter.</td>
  </tr>
  <tr>
    <td>quadraticsharp<br>quadratic_sharp</td>
    <td></td>
  </tr>
  <tr>
    <td>quadratic</td>
    <td></td>
  </tr>
  <tr>
    <td>quadraticapprox<br>quadraticapproximate<br>quadratic_approximate</td>
    <td></td>
  </tr>
  <tr>
    <td>quadraticmix<br>quadratic_mix</td>
    <td></td>
  </tr>
  <tr>
    <td>kaiser</td>
    <td></td>
  </tr>
  <tr>
    <td>lanczos2</td>
    <td></td>
  </tr>
  <tr>
    <td>lanczos3</td>
    <td></td>
  </tr>
  <tr>
    <td>lanczos4</td>
    <td></td>
  </tr>
  <tr>
    <td>lanczos6</td>
    <td></td>
  </tr>
  <tr>
    <td>lanczos8</td>
    <td></td>
  </tr>
  <tr>
    <td>lanczos12</td>
    <td></td>
  </tr>
  <tr>
    <td>lanczos64</td>
    <td></td>
  </tr>
  <tr>
    <td>mitchell</td>
    <td>One of the best choices for upscaling.</td>
  </tr>
  <tr>
    <td>robidoux</td>
    <td>One of the best choices for upscaling.</td>
  </tr>
  <tr>
    <td>robidouxsharp</td>
    <td>The default color filter.</td>
  </tr>
  <tr>
    <td>robidouxsoft</td>
    <td></td>
  </tr>
  <tr>
    <td>catmul<br>catmulrom<br>catmul-rom</td>
    <td></td>
  </tr>
  <tr>
    <td>bspline<br>b-spline<br>b_spline</td>
    <td></td>
  </tr>
  <tr>
    <td>adobebicubic<br>adobebc</td>
    <td></td>
  </tr>
  <tr>
    <td>cardinal<br>card<br>cardinaluniform<br>cardinal_uniform<br>adobebicubicsharp<br>adobebcsharp</td>
    <td></td>
  </tr>
  <tr>
    <td>hermite</td>
    <td></td>
  </tr>
  <tr>
    <td>hamming</td>
    <td></td>
  </tr>
  <tr>
    <td>hanning</td>
    <td></td>
  </tr>
  <tr>
    <td>blackman</td>
    <td></td>
  </tr>
  <tr>
    <td>gaussiansharp<br>gaussian_sharp</td>
    <td></td>
  </tr>
  <tr>
    <td>gaussian</td>
    <td></td>
  </tr>
  <tr>
    <td>bell</td>
    <td></td>
  </tr> 
  <tr>
    <td>-filterw</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the non-mipmap color and alpha <strong>width</strong> filter.</td>
  </tr>
  <tr>
    <td>-filterh</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the non-mipmap color and alpha <strong>height</strong> filter.</td>
  </tr>
  <tr>
    <td>-filterd</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the non-mipmap color and alpha <strong>depth</strong> filter.</td>
  </tr>
  <tr>
    <td>-filterw_color</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the non-mipmap color <strong>width</strong> filter.</td>
  </tr>
  <tr>
    <td>-filterh_color</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the non-mipmap color <strong>height</strong> filter.</td>
  </tr>
  <tr>
    <td>-filterd_color</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the non-mipmap color <strong>depth</strong> filter.</td>
  </tr>
  <tr>
    <td>-filterw_alpha</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the non-mipmap alpha <strong>width</strong> filter.</td>
  </tr>
  <tr>
    <td>-filterh_alpha</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the non-mipmap alpha <strong>height</strong> filter.</td>
  </tr>
  <tr>
    <td>-filterd_alpha</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the non-mipmap alpha <strong>depth</strong> filter.</td>
  </tr>
  <tr>
    <td>-prescale</td>
    <td>&lt;new width&gt; &lt;new height&gt;</td>
    <td>Resamples the image to the given width/height using the selected non-mipmap filters.</td>
  </tr>
  <tr>
    <td>-prescale3</td>
    <td>&lt;new width&gt; &lt;new height&gt; &lt;new depth&gt;</td>
    <td>Resamples the image to the given width/height/depth using the selected non-mipmap filters.</td>
  </tr>
  <tr>
    <td rowspan="3">-resample_to</td>
    <td>nearest</td>
    <td>Resamples to the nearest power of 2 in each dimension.</td>
  </tr>
  <tr>
    <td>lo</td>
    <td>Resamples to the next power-of-2 down.</td>
  </tr>
  <tr>
    <td>hi</td>
    <td>Resamples to the next power-of-2 up.</td>
  </tr>
  <tr>
    <td>-rel_scale</td>
    <td>&lt;width multiplier&gt; &lt;height multiplier&gt;</td>
    <td>Resamples by the given width and height multipliers.</td>
  </tr>
  <tr>
    <td>-rel_scale3</td>
    <td>&lt;width multiplier&gt; &lt;height multiplier&gt; &lt;depth multiplier&gt;</td>
    <td>Resamples by the given width, height, and depth multipliers.</td>
  </tr>
  <tr>
    <td>-clamp2</td>
    <td>&lt;width&gt; &lt;height&gt;</td>
    <td>Clamps the image to the given width and height.</td>
  </tr>
  <tr>
    <td>-clamp3</td>
    <td>&lt;width&gt; &lt;height&gt; &lt;depth&gt;</td>
    <td>Clamps the image to the given width, height, and depth.</td>
  </tr>
</table>

<h3>Texture Addressing</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td rowspan="6">-textureaddressing<br>-ta</td>
    <td>clamp</td>
    <td>U, V, and W coordinates are clamped to the edge of the texture.<br>Equal to <code>D3D12_TEXTURE_ADDRESS_MODE_CLAMP</code>.</td>
  </tr>
  <tr>
    <td>repeat<br>wrap</td>
    <td>U, V, and W coordinates repeat beyond the 0..1 range.<br>Equal to <code>D3D12_TEXTURE_ADDRESS_MODE_WRAP</code>.</td>
  </tr>
  <tr>
    <td>mirror<br>reflect</td>
    <td>U, V, and W are mirrored beyond the 0..1 range.<br>Equal to <code>D3D12_TEXTURE_ADDRESS_MODE_MIRROR</code>.</td>
  </tr>
  <tr>
    <td>mirroronce<br>mirror_once</td>
    <td>U, V, and W are mirrored 1 time beyond the 0..1 range, after which clamping is used.<br>Equal to <code>D3D12_TEXTURE_ADDRESS_MODE_MIRROR_ONCE</code>.</td>
  </tr>
  <tr>
    <td>border<br>bordercolor<br>border_color</td>
    <td>The border color is used when U, V, and W go outside of 0..1.<br>Equal to <code>D3D12_TEXTURE_ADDRESS_MODE_BORDER</code>.</td>
  </tr>
  <tr>
    <td>no_border<br>null_border</td>
    <td>Nothing is considered to exist beyond the U, V, and W texture edges. This is the default.</td>
  </tr>
  <tr>
    <td>-textureaddressingw<br>-taw</td>
    <td>Same as <em>-ta.</em></td>
    <td>Applies only to the U coordinate.</td>
  </tr>
  <tr>
    <td>-textureaddressingh<br>-tah</td>
    <td>Same as <em>-ta.</em></td>
    <td>Applies only to the V coordinate.</td>
  </tr>
  <tr>
    <td>-textureaddressingd<br>-tad</td>
    <td>Same as <em>-ta.</em></td>
    <td>Applies only to the W coordinate.</td>
  </tr>
  <tr>
    <td>-textureaddressingw_color<br>-taw_color</td>
    <td>Same as <em>-ta.</em></td>
    <td>Applies only to the U coordinate and to color channels.</td>
  </tr>
  <tr>
    <td>-textureaddressingh_color<br>-tah_color</td>
    <td>Same as <em>-ta.</em></td>
    <td>Applies only to the V coordinate and to color channels.</td>
  </tr>
  <tr>
    <td>-textureaddressingd_color<br>-tad_color</td>
    <td>Same as <em>-ta.</em></td>
    <td>Applies only to the W coordinate and to color channels.</td>
  </tr>
  <tr>
    <td>-textureaddressingw_alpha<br>-taw_alpha</td>
    <td>Same as <em>-ta.</em></td>
    <td>Applies only to the U coordinate and to the alpha channel.</td>
  </tr>
  <tr>
    <td>-textureaddressingh_alpha<br>-tah_alpha</td>
    <td>Same as <em>-ta.</em></td>
    <td>Applies only to the V coordinate and to the alpha channel.</td>
  </tr>
  <tr>
    <td>-textureaddressingd_alpha<br>-tad_alpha</td>
    <td>Same as <em>-ta.</em></td>
    <td>Applies only to the W coordinate and to the alpha channel.</td>
  </tr>
  <tr>
    <td>-border_color</td>
    <td>&lt;r&gt; &lt;g&gt; &lt;b&gt; &lt;a&gt;</em></td>
    <td>Sets the border color for the U, V, and W coordinates.<br>Defaults to <strong>0.0 0.0 0.0 1.0</strong></td>
  </tr>
</table>

<h3>YUV Options</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td rowspan="15">-yuv_input_format</td>
    <td>&lt;any Vulkan, DXGI, or Metal YUV format&gt;</td>
    <td>Sets the format (encoding) of the YUV file being loaded.</td>
  </tr>
  <tr>
    <td>nv12</td>
    <td>DXGI_FORMAT_NV12/ VK_FORMAT_G8_B8R8_2PLANE_420_UNORM</td>
  </tr>
  <tr>
    <td>nv21</td>
    <td>DXGI_FORMAT_NV21/ VK_FORMAT_NV21</td>
  </tr>
  <tr>
    <td>yv12</td>
    <td>DXGI_FORMAT_YV12</td>
  </tr>
  <tr>
    <td>yuy2</td>
    <td>DXGI_FORMAT_G8R8_G8B8_UNORM/ VK_FORMAT_G8B8G8R8_422_UNORM/ MTLPixelFormatGBGR422/ DXGI_FORMAT_YUY2</td>
  </tr>
  <tr>
    <td>uyvy</td>
    <td>DXGI_FORMAT_R8G8_B8G8_UNORM/ VK_FORMAT_B8G8R8G8_422_UNORM/ MTLPixelFormatBGRG422</td>
  </tr>
  <tr>
    <td>p010</td>
    <td>DXGI_FORMAT_P010/ VK_FORMAT_G10X6_B10X6R10X6_2PLANE_420_UNORM_3PACK16</td>
  </tr>
  <tr>
    <td>p016</td>
    <td>DXGI_FORMAT_P016/ VK_FORMAT_G16_B16R16_2PLANE_420_UNORM</td>
  </tr>
  <tr>
    <td>p210</td>
    <td>DXGI_FORMAT_P210/ VK_FORMAT_G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16</td>
  </tr>
  <tr>
    <td>p216</td>
    <td>DXGI_FORMAT_P216/ VK_FORMAT_G16_B16R16_2PLANE_422_UNORM</td>
  </tr>
  <tr>
    <td>y210</td>
    <td>DXGI_FORMAT_Y210/ VK_FORMAT_G10X6_B10X6R10X6R10X6_422_UNORM_4PACK16</td>
  </tr>
  <tr>
    <td>y216</td>
    <td>DXGI_FORMAT_Y216/ VK_FORMAT_G16B16G16R16_422_UNORM</td>
  </tr>
  <tr>
    <td>y410</td>
    <td>DXGI_FORMAT_Y410</td>
  </tr>
  <tr>
    <td>y416</td>
    <td>DXGI_FORMAT_Y416</td>
  </tr>
  <tr>
    <td>ayuv</td>
    <td>DXGI_FORMAT_AYUV</td>
  </tr>
  <tr>
    <td>-yuv_format</td>
    <td>Same as <em>-yuv_input_format</em></td>
    <td>Sets the encoding when saving to a YUV format.</td>
  </tr>
  <tr>
    <td>-yuv_input_use_approx</td>
    <td></td>
    <td>Uses a common approximate YUV -> RGB conversion when loading a YUV file. By default the full YUV -> RGB algorithm is used.</td>
  </tr>
  <tr>
    <td>-yuv_use_approx</td>
    <td></td>
    <td>Uses a common approximate RGB -> YUV conversion when writing to a YUV file. By default the full RGB -> YUV algorithm is used.</td>
  </tr>
  <tr>
    <td rowspan="7">-yuv_input_kr_kb</td>
    <td>REC_709<br>REC709</td>
    <td>
      Sets the Kr and Kb factors according to the ITU-R Recommendation BT.709-5 standard.<br>
      <strong>0.212639005871510</strong> and <strong>0.072192315360734</strong>.<br>
      This is the default.
    </td>
  </tr>
  <tr>
    <td>REC_2020<br>REC2020</td>
    <td>
      Sets the Kr and Kb factors according to the ITU-R Recommendation BT.2020 standard.<br>
      0.2627 and 0.0593.
    </td>
  </tr>
  <tr>
    <td>SMPTC</td>
    <td>Sets the Kr and Kb factors according to the SMPTE C standard.<br>0.2124 and 0.0866.</td>
  </tr>
  <tr>
    <td>REC_601<br>REC601</td>
    <td>
      Sets the Kr and Kb factors according to the ITU-R Recommendation BT.601 standard.<br>
      0.2988390 and 0.1143500.
    </td>
  </tr>
  <tr>
    <td>CIE_1931<br>CIE1931</td>
    <td>
      Sets the Kr and Kb factors according to the CIE 1931 standard.<br>
      0.3086 and 0.0820.
    </td>
  </tr>
  <tr>
    <td>NTSC_1953<br>NTSC1953</td>
    <td>Sets the Kr and Kb factors according to the NTSC 1953 standard.<br>0.3 and 0.11.</td>
  </tr>
  <tr>
    <td>EBU_TECH_3213<br>EBUTECH3213</td>
    <td>
      Sets the Kr and Kb factors according to the EBU Tech. 3213 standard.<br>
      0.2988390 and 0.1143500.
    </td>
  </tr>
  <tr>
    <td>-yuv_kr_kb</td>
    <td>Same as <em>-yuv_input_kr_kb</em></td>
    <td>Sets the output Kr and Kb factors when saving to a YUV file.</td>
  </tr>
  <tr>
    <td>-yuv_input_set_kr_kb</td>
    <td>&lt;kr&gt; &lt;kb&gt;</td>
    <td>Manually specifies the Kr and Kb factors for loading a YUV file.</td>
  </tr>
  <tr>
    <td>-yuv_set_kr_kb</td>
    <td>&lt;kr&gt; &lt;kb&gt;</td>
    <td>Manually specifies the Kr and Kb factors for saving to a YUV file.</td>
  </tr>
  <tr>
    <td>-yuv_input_set_z<br>-yuv_input_set_black</td>
    <td>&lt;black level&gt;</td>
    <td>Sets the black level (0..1) for loading a YUV file. Defaults to <strong>0.0</strong>.</td>
  </tr>
  <tr>
    <td>-yuv_set_z<br>-yuv_set_black</td>
    <td>&lt;black level&gt;</td>
    <td>Sets the black level (0..1) for saving to a YUV file. Defaults to <strong>0.0</strong>.</td>
  </tr>
  <tr>
    <td>-yuv_input_set_s<br>-yuv_input_set_scale</td>
    <td>&lt;scale&gt;</td>
    <td>Sets the scaler (0..1) for loading a YUV file. Defaults to <strong>1.0</strong>.</td>
  </tr>
  <tr>
    <td>-yuv_set_s<br>-yuv_set_scale</td>
    <td>&lt;scale&gt;</td>
    <td>Sets the scaler (0..1) for saving to a YUV file. Defaults to <strong>1.0</strong>.</td>
  </tr>
  <tr>
    <td>-yuv_input_pc</td>
    <td></td>
    <td>
      Sets the black level to 0.0, scale to 1.0, Kr and Kb to the ITU-R Recommendation BT.709-5 standard, and enables the full non-approximate conversion routine for loading YUV files.
    </td>
  </tr>
  <tr>
    <td>-yuv_pc</td>
    <td></td>
    <td>
      Sets the black level to 0.0, scale to 1.0, Kr and Kb to the ITU-R Recommendation BT.709-5 standard, and enables the full non-approximate conversion routine for saving to a YUV file.
    </td>
  </tr>
  <tr>
    <td>-yuv_input_studio</td>
    <td></td>
    <td>
      Sets the black level to (16.0 / 255.0), scale to (219.0 / 255.0), Kr and Kb to the ITU-R Recommendation BT.709-5 standard, and enables the full non-approximate conversion routine for loading YUV files.
    </td>
  </tr>
  <tr>
    <td>-yuv_studio</td>
    <td></td>
    <td>
      Sets the black level to (16.0 / 255.0), scale to (219.0 / 255.0), Kr and Kb to the ITU-R Recommendation BT.709-5 standard, and enables the full non-approximate conversion routine for saving to a YUV file.
    </td>
  </tr>
</table>

<h3>Mipmaps</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>-nomips<br>-nomipmaps<br>-no_mips<br>-no_mipmaps</td>
    <td></td>
    <td>No mipmaps are generated and existing mipmaps are discarded.</td>
  </tr>
  <tr>
    <td>-nmips</td>
    <td>&lt;total mipmaps&gt;</td>
    <td>
      Sets the total number of mipmaps desired. Set to 0 to generate (or keep) a full mipmap chain.<br>
      Defaults to <strong>0</strong>.
    </td>
  </tr>
  <tr>
    <td>-keepmips<br>-keepmipmaps<br>-keep_mips<br>-keep_mipmaps</td>
    <td></td>
    <td>
      By default, new mipmaps will be generated as specified by <em>-nmips</em> (which defaults to 0, so a full chain is generated).<br>
      This command allows existing mipmaps to be retained instead of overwritten. Existing mipmaps beyond the <em>-nmips</em> specification will be truncated, and if <em>-nmips</em> extends beyond the number of existing mipmaps, then new mipmaps will be generated to fill the gap.
    </td>
  </tr>
    <tr>
    <td>-mip_filter</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Applies the selected filter to all mipmap filters.</td>
  </tr>
  <tr>
    <td>-mip_filterw</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the mipmap color and alpha <strong>width</strong> filter.</td>
  </tr>
  <tr>
    <td>-mip_filterh</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the mipmap color and alpha <strong>height</strong> filter.</td>
  </tr>
  <tr>
    <td>-mip_filterd</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the mipmap color and alpha <strong>depth</strong> filter.</td>
  </tr>
  <tr>
    <td>-mip_filterw_color</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the mipmap color <strong>width</strong> filter.</td>
  </tr>
  <tr>
    <td>-mip_filterh_color</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the mipmap color <strong>height</strong> filter.</td>
  </tr>
  <tr>
    <td>-mip_filterd_color</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the mipmap color <strong>depth</strong> filter.</td>
  </tr>
  <tr>
    <td>-mip_filterw_alpha</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the mipmap alpha <strong>width</strong> filter.</td>
  </tr>
  <tr>
    <td>-mip_filterh_alpha</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the mipmap alpha <strong>height</strong> filter.</td>
  </tr>
  <tr>
    <td>-mip_filterd_alpha</td>
    <td>Same as for <em>-filter</em>.</td>
    <td>Sets the mipmap alpha <strong>depth</strong> filter.</td>
  </tr>
</table>

<h3>Normal Maps</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td rowspan="7">-nm_channel</td>
    <td>r<br>red</td>
    <td>The normal map will be generated using the R channel.</td>
  </tr>
  <tr>
    <td>g<br>green</td>
    <td>The normal map will be generated using the G channel.</td>
  </tr>
  <tr>
    <td>b<br>blue</td>
    <td>The normal map will be generated using the B channel.</td>
  </tr>
  <tr>
    <td>a<br>alpha</td>
    <td>The normal map will be generated using the A channel.</td>
  </tr>
  <tr>
    <td>max</td>
    <td>The normal map will be generated using the max value between the RGBA channels. This is the default.</td>
  </tr>
  <tr>
    <td>rgb</td>
    <td>The normal map will be generated using the average value between the RGB channels.</td>
  </tr>
  <tr>
    <td>colorspace</td>
    <td>The normal map will be generated using the weighted average value between the RGB channels. Use <em>-luma</em> to select from predefined weights or <em>-weight</em> to manually specify weights.</td>
  </tr>
  <tr>
    <td>-norm<br>-normalize</td>
    <td></td>
    <td>Indicates that the normal maps should be normalized.</td>
  </tr>
  <tr>
    <td>-opengl<br>-unity<br>-blender<br>-maya</td>
    <td></td>
    <td>Specifies that the normal map should be compatible with OpenGL.</td>
  </tr>
  <tr>
    <td>-directx<br>-ue4<br>-unreal<br>-unrealengine<br>-ue<br>-dsmax</td>
    <td></td>
    <td>Specifies that the normal map should be compatible with DirectX.</td>
  </tr>
  <tr>
    <td>-n3x3</td>
    <td></td>
    <td>Normal maps will be generated with a 3×3 kernel.</td>
  </tr>
  <tr>
    <td>-n5x5</td>
    <td></td>
    <td>Normal maps will be generated with a 5×5 kernel.</td>
  </tr>
  <tr>
    <td>-n7x7</td>
    <td></td>
    <td>Normal maps will be generated with a 7×7 kernel.</td>
  </tr>
  <tr>
    <td>-n9x9</td>
    <td></td>
    <td>Normal maps will be generated with a 9×9 kernel.</td>
  </tr>
  <tr>
    <td>-scale<br>-nm_z</td>
    <td></td>
    <td>Specifies the normal map’s Z influence.</td>
  </tr>
</table>

<h3>Transforms</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>-format</td>
    <td>&lt;any Vulkan, DXGI, or Metal format&gt;</td>
    <td>Converts the loaded image to the given texture format.</td>
  </tr>
  <tr>
    <td>-ogl_format</td>
    <td>&lt;internal format&gt; &lt;type&gt; &lt;base internal format&gt;</td>
    <td>Converts the loaded image to the given OpenGL texture format.</td>
  </tr>
  <tr>
    <td>-ignore_alpha</td>
    <td></td>
    <td>Any alpha channel is set to all 1’s.</td>
  </tr>
  <tr>
    <td>-alpha_threshold</td>
    <td>&lt;cutoff&gt;</td>
    <td>Sets the alpha cutoff (0..255) for conversions to formats with binary alpha. Defaults to <strong>128</strong>.</td>
  </tr>
  <tr>
    <td>-premultiply_alpha<br>-premult_alpha</td>
    <td></td>
    <td>Specifies that alpha should be pre-multiplied. If an image is already pre-multiplied it is not pre-multiplied again.</td>
  </tr>
  <tr>
    <td>-swizzle</td>
    <td>&lt;swizzle&gt;</td>
    <td>
      Specifies a swizzle to apply. Valid swizzle characters: rgbaxyzw01. Must be 4 characters long and is not case-sensitive.
    </td>
  </tr>
  <tr>
    <td>-swap</td>
    <td></td>
    <td>Swaps the R and B channels.</td>
  </tr>
</table>

<h3>Quality Settings</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>-quality_highest<br>-very_slow</td>
    <td></td>
    <td>The highest quality setting for compressing textures in BC*, EAC, ETC*, PVR, and ASTC formats.</td>
  </tr>
  <tr>
    <td>-quality_production<br>-slow</td>
    <td></td>
    <td>The 2<sup>nd</sup>-highest quality setting for compressing textures in BC*, EAC, ETC*, PVR, and ASTC formats.</td>
  </tr>
  <tr>
    <td>-quality_normal<br>-basic</td>
    <td></td>
    <td>The normal quality setting for compressing textures in BC*, EAC, ETC*, PVR, and ASTC formats.</td>
  </tr>
  <tr>
    <td>-fast</td>
    <td></td>
    <td>A fast but somewhat low-quality setting for compressing textures in BC*, EAC, ETC*, PVR, and ASTC formats.</td>
  </tr>
  <tr>
    <td>-quick<br>-veryfast</td>
    <td></td>
    <td>A faster but lower-quality setting for compressing textures in BC*, EAC, ETC*, PVR, and ASTC formats.</td>
  </tr>
  <tr>
    <td>-ultrafast</td>
    <td></td>
    <td>The fastest but lowest-quality setting for compressing textures in BC*, EAC, ETC*, PVR, and ASTC formats.</td>
  </tr>
</table>

<h3>Misc.</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>-weight<br>-weights</td>
    <td>&lt;red weight&gt; &lt;green weight&gt; &lt;blue weight&gt;</td>
    <td>Sets the luminance weight factors manually.</td>
  </tr>
  <tr>
    <td rowspan="7">-luma</td>
    <td>REC_709<br>REC709</td>
    <td>
      Sets the luminance weight factors according to the ITU-R Recommendation BT.709-5 standard.<br>
      0.212639005871510, 0.715168678767756, and 0.072192315360734.<br>
      This is the default.
    </td>
  </tr>
  <tr>
    <td>REC_2020<br>REC2020</td>
    <td>
      Sets the luminance weight factors according to the ITU-R Recommendation BT.2020 standard.<br>
      0.2627, 0.678, and 0.0593.
    </td>
  </tr>
  <tr>
    <td>SMPTC</td>
    <td>
      Sets the luminance weight factors according to the SMPTE C standard.<br>
      0.2124, 0.7011, and 0.0866.
    </td>
  </tr>
  <tr>
    <td>REC_601<br>REC601</td>
    <td>
      Sets the luminance weight factors according to the ITU-R Recommendation BT.601 standard.<br>
      0.2988390, 0.5868110, and 0.1143500.
    </td>
  </tr>
  <tr>
    <td>CIE_1931<br>CIE1931</td>
    <td>
      Sets the luminance weight factors according to the CIE 1931 standard.<br>
      0.3086, 0.6094, and 0.0820.
    </td>
  </tr>
  <tr>
    <td>NTSC_1953<br>NTSC1953</td>
    <td>
      Sets the luminance weight factors according to the NTSC 1953 standard.<br>
      0.3, 0.59, and 0.11.
    </td>
  </tr>
  <tr>
    <td>EBU_TECH_3213<br>EBUTECH3213</td>
    <td>
      Sets the luminance weight factors according to the EBU Tech. 3213 standard.<br>
      0.2988390, 0.5868110, and 0.1143500.
    </td>
  </tr>
  <tr>
    <td>-printformats<br>-print_formats</td>
    <td></td>
    <td>Prints all supported formats that can be supplied to <em>-format</em>.</td>
  </tr>
</table>

<h3>PNG Options</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>-png_default</td>
    <td></td>
    <td>Default PNG compression (6) will be used.</td>
  </tr>
  <tr>
    <td>-png_bestspeed</td>
    <td></td>
    <td>Fast PNG compression (1) will be used.</td>
  </tr>
  <tr>
    <td>-png_bestcompression</td>
    <td></td>
    <td>Best PNG compression (9) will be used.</td>
  </tr>
  <tr>
    <td>-png_level</td>
    <td></td>
    <td>Specifies the PNG compression level. [0..9].</td>
  </tr>
  <tr>
    <td>-png_nocompression</td>
    <td></td>
    <td>No PNG compression will be used.</td>
  </tr>
  <tr>
    <td>-png_interlaced</td>
    <td></td>
    <td>Interlacing will be used. The default is <em>no</em> interlacing.</td>
  </tr>
  <tr>
    <td rowspan="8">-png_format</td>
    <td>R8G8B8<br>RGB24<br>RGB</td>
    <td rowspan="8">Specifies the PNG format to which to save.<br>If the format is not specified, the closest format to what was specified by <em>-format</em> (or the original file’s format if <em>-format</em> is not specified) will be used.</td>
  </tr>
  <tr>
    <td>R8G8B8_SRGB<br>RGB24_SRGB<br>RGB_SRGB</td>
  </tr>
  <tr>
    <td>R8G8B8A8<br>RGBA32<br>RGBA</td>
  </tr>
  <tr>
    <td>R8G8B8A8_SRGB<br>RGBA32_SRGB<br>RGBA_SRGB</td>
  </tr>
  <tr>
    <td>R16G16B16<br>RGB16</td>
  </tr>
  <tr>
    <td>R16G16B16A16<br>RGBA16</td>
  </tr>
  <tr>
    <td>L8<br>LUMINANCE8<br>GREYSCALE8<br>GRAYSCALE8</td>
  </tr>
  <tr>
    <td>L16<br>LUMINANCE16<br>GREYSCALE16<br>GRAYSCALE16</td>
  </tr>
</table>

<h3>BMP Options</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>-bmp_rle</td>
    <td></td>
    <td>
      RLE encoding will be used to save the BMP file.<br>
      <em>This is not set by default.</em>
    </td>
  </tr>
  <tr>
    <td>-bmp_noalpha</td>
    <td></td>
    <td>
      Alpha will not be saved or will be set to 1 in the BMP file.<br>
      The default is to store alpha when available.
    </td>
  </tr>
  <tr>
    <td>-bmp_nobitmask<br>-bmp_nomask</td>
    <td></td>
    <td>
      By default, the BMP file will contain masks for the R, G, B, and A channels.<br>
      This setting causes the BMP file to be saved without the masks.<br>
    </td>
  </tr>
  <tr>
    <td rowspan="18">-bmp_format</td>
    <td>R8G8B8<br>RGB24<br>RGB</td>
    <td rowspan="18">
      Specifies the BMP format to which to save.<br>If the format is not specified, the closest format to what was specified by <em>-format</em> (or the original file’s format if <em>-format</em> is not specified) will be used.</td>
    </td>
  </tr>
  <tr>
    <td>R8G8B8_SRGB<br>RGB24_SRGB<br>RGB_SRGB</td>
  </tr>
  <tr>
    <td>R8G8B8A8<br>RGBA32<br>RGBA</td>
  </tr>
  <tr>
    <td>R8G8B8A8_SRGB<br>RGBA32_SRGB<br>RGBA_SRGB</td>
  </tr>
  <tr>
    <td>B8G8R8A8</td>
  </tr>
  <tr>
    <td>B8G8R8A8_SRGB</td>
  </tr>
  <tr>
    <td>A8B8G8R8</td>
  </tr>
  <tr>
    <td>A8B8G8R8_SRGB</td>
  </tr>
  <tr>
    <td>R4G4B4A4</td>
  </tr>
  <tr>
    <td>B4G4R4A4</td>
  </tr>
  <tr>
    <td>A4R4G4B4</td>
  </tr>
  <tr>
    <td>A4B4G4R4</td>
  </tr>
  <tr>
    <td>R5G6B5</td>
  </tr>
  <tr>
    <td>B5G6R5</td>
  </tr>
  <tr>
    <td>R5G5B5A1</td>
  </tr>
  <tr>
    <td>A1B5G5R5</td>
  </tr>
  <tr>
    <td>A4B4G4R4</td>
  </tr>
</table>

<h3>TGA Options</h3>

<table border="1" cellpadding="5">
  <tr>
    <th>Command</th>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>-tga_rle</td>
    <td></td>
    <td>The TGA file will be saved with RLE encoding.</td>
  </tr>
  <tr>
    <td rowspan="6">-tga_format</td>
    <td>R8G8B8<br>RGB24<br>RGB</td>
    <td rowspan="6">Specifies the TGA format to which to save.<br>If the format is not specified, the closest format to what was specified by <em>-format</em> (or the original file’s format if <em>-format</em> is not specified) will be used.</td>
  </tr>
  <tr>
    <td>R8G8B8_SRGB<br>RGB24_SRGB<br>RGB_SRGB</td>
  </tr>
  <tr>
    <td>R8G8B8A8<br>RGBA32<br>RGBA</td>
  </tr>
  <tr>
    <td>R8G8B8A8_SRGB<br>RGBA32_SRGB<br>RGBA_SRGB</td>
  </tr>
  <tr>
    <td>A1R5G5B5<br>A1RGB5</td>
  </tr>
  <tr>
    <td>L8<br>LUMINANCE8<br>GREYSCALE8<br>GRAYSCALE8</td>
  </tr>
</table>

<h2>Formats</h2>

These image formats supported:
 | Vulkan Formats |
 | --- |
 | VK_FORMAT_R8_UNORM |
 | VK_FORMAT_R8G8_UNORM |
 | VK_FORMAT_R8G8B8_UNORM |
 | VK_FORMAT_B8G8R8_UNORM |
 | VK_FORMAT_R8G8B8A8_UNORM |
 | VK_FORMAT_B8G8R8A8_UNORM |
 | VK_FORMAT_R8_SNORM |
 | VK_FORMAT_R8G8_SNORM |
 | VK_FORMAT_R8G8B8_SNORM |
 | VK_FORMAT_B8G8R8_SNORM |
 | VK_FORMAT_R8G8B8A8_SNORM |
 | VK_FORMAT_B8G8R8A8_SNORM |
 | VK_FORMAT_R8_UINT |
 | VK_FORMAT_R8G8_UINT |
 | VK_FORMAT_R8G8B8_UINT |
 | VK_FORMAT_B8G8R8_UINT |
 | VK_FORMAT_R8G8B8A8_UINT |
 | VK_FORMAT_B8G8R8A8_UINT |
 | VK_FORMAT_R8_SINT |
 | VK_FORMAT_R8G8_SINT |
 | VK_FORMAT_R8G8B8_SINT |
 | VK_FORMAT_B8G8R8_SINT |
 | VK_FORMAT_R8G8B8A8_SINT |
 | VK_FORMAT_B8G8R8A8_SINT |
 | VK_FORMAT_R8_SRGB |
 | VK_FORMAT_R8_SRGB |
 | VK_FORMAT_R8G8_SRGB |
 | VK_FORMAT_R8G8_SRGB |
 | VK_FORMAT_R8G8B8_SRGB |
 | VK_FORMAT_B8G8R8_SRGB |
 | VK_FORMAT_R8G8B8A8_SRGB |
 | VK_FORMAT_B8G8R8A8_SRGB |
 | VK_FORMAT_R16_UNORM |
 | VK_FORMAT_R16G16_UNORM |
 | VK_FORMAT_R16G16B16_UNORM |
 | VK_FORMAT_R16G16B16A16_UNORM |
 | VK_FORMAT_R16_SNORM |
 | VK_FORMAT_R16G16_SNORM |
 | VK_FORMAT_R16G16B16_SNORM |
 | VK_FORMAT_R16G16B16A16_SNORM |
 | VK_FORMAT_R16_UINT |
 | VK_FORMAT_R16G16_UINT |
 | VK_FORMAT_R16G16B16_UINT |
 | VK_FORMAT_R16G16B16A16_UINT |
 | VK_FORMAT_R16_SINT |
 | VK_FORMAT_R16G16_SINT |
 | VK_FORMAT_R16G16B16_SINT |
 | VK_FORMAT_R16G16B16A16_SINT |
 | VK_FORMAT_R16_SFLOAT |
 | VK_FORMAT_R16G16_SFLOAT |
 | VK_FORMAT_R16G16B16_SFLOAT |
 | VK_FORMAT_R16G16B16A16_SFLOAT |
 | VK_FORMAT_R32_UINT |
 | VK_FORMAT_R32G32_UINT |
 | VK_FORMAT_R32G32B32_UINT |
 | VK_FORMAT_R32G32B32A32_UINT |
 | VK_FORMAT_R32_SINT |
 | VK_FORMAT_R32G32_SINT |
 | VK_FORMAT_R32G32B32_SINT |
 | VK_FORMAT_R32G32B32A32_SINT |
 | VK_FORMAT_R32_SFLOAT |
 | VK_FORMAT_R32G32_SFLOAT |
 | VK_FORMAT_R32G32B32_SFLOAT |
 | VK_FORMAT_R32G32B32A32_SFLOAT |
 | VK_FORMAT_R64_UINT |
 | VK_FORMAT_R64G64_UINT |
 | VK_FORMAT_R64G64B64_UINT |
 | VK_FORMAT_R64G64B64A64_UINT |
 | VK_FORMAT_R64_SINT |
 | VK_FORMAT_R64G64_SINT |
 | VK_FORMAT_R64G64B64_SINT |
 | VK_FORMAT_R64G64B64A64_SINT |
 | VK_FORMAT_R64_SFLOAT |
 | VK_FORMAT_R64G64_SFLOAT |
 | VK_FORMAT_R64G64B64_SFLOAT |
 | VK_FORMAT_R64G64B64A64_SFLOAT |
 | VK_FORMAT_R4G4_UNORM_PACK8 |
 | VK_FORMAT_R4G4B4A4_UNORM_PACK16 |
 | VK_FORMAT_B4G4R4A4_UNORM_PACK16 |
 | VK_FORMAT_A4R4G4B4_UNORM_PACK16 |
 | VK_FORMAT_A4B4G4R4_UNORM_PACK16 |
 | VK_FORMAT_R5G6B5_UNORM_PACK16 |
 | VK_FORMAT_B5G6R5_UNORM_PACK16 |
 | VK_FORMAT_R5G5B5A1_UNORM_PACK16 |
 | VK_FORMAT_A1B5G5R5_UNORM_PACK16_KHR |
 | VK_FORMAT_A1R5G5B5_UNORM_PACK16 |
 | VK_FORMAT_A8B8G8R8_UNORM_PACK32 |
 | VK_FORMAT_A8B8G8R8_SNORM_PACK32 |
 | VK_FORMAT_A8B8G8R8_UINT_PACK32 |
 | VK_FORMAT_A8B8G8R8_SINT_PACK32 |
 | VK_FORMAT_A8B8G8R8_SRGB_PACK32 |
 | VK_FORMAT_A2R10G10B10_UNORM_PACK32 |
 | VK_FORMAT_A2B10G10R10_UNORM_PACK32 |
 | VK_FORMAT_A2R10G10B10_SNORM_PACK32 |
 | VK_FORMAT_A2B10G10R10_SNORM_PACK32 |
 | VK_FORMAT_A2R10G10B10_UINT_PACK32 |
 | VK_FORMAT_A2B10G10R10_UINT_PACK32 |
 | VK_FORMAT_A2R10G10B10_SINT_PACK32 |
 | VK_FORMAT_A2B10G10R10_SINT_PACK32 |
 | VK_FORMAT_B10G11R11_UFLOAT_PACK32 |
 | VK_FORMAT_E5B9G9R9_UFLOAT_PACK32 |
 | VK_FORMAT_A8_UNORM_KHR |
 | VK_FORMAT_BC1_RGB_UNORM_BLOCK |
 | VK_FORMAT_BC1_RGBA_UNORM_BLOCK |
 | VK_FORMAT_BC2_UNORM_BLOCK |
 | VK_FORMAT_BC3_UNORM_BLOCK |
 | VK_FORMAT_BC1_RGB_SRGB_BLOCK |
 | VK_FORMAT_BC1_RGBA_SRGB_BLOCK |
 | VK_FORMAT_BC2_SRGB_BLOCK |
 | VK_FORMAT_BC3_SRGB_BLOCK |
 | VK_FORMAT_BC4_UNORM_BLOCK |
 | VK_FORMAT_BC5_UNORM_BLOCK |
 | VK_FORMAT_BC4_SNORM_BLOCK |
 | VK_FORMAT_BC5_SNORM_BLOCK |
 | VK_FORMAT_BC6H_UFLOAT_BLOCK |
 | VK_FORMAT_BC7_UNORM_BLOCK |
 | VK_FORMAT_BC7_SRGB_BLOCK |
 | VK_FORMAT_ETC2_R8G8B8_UNORM_BLOCK |
 | VK_FORMAT_ETC2_R8G8B8A1_UNORM_BLOCK |
 | VK_FORMAT_ETC2_R8G8B8A8_UNORM_BLOCK |
 | VK_FORMAT_ETC2_R8G8B8_SRGB_BLOCK |
 | VK_FORMAT_ETC2_R8G8B8A1_SRGB_BLOCK |
 | VK_FORMAT_ETC2_R8G8B8A8_SRGB_BLOCK |
 | VK_FORMAT_EAC_R11_UNORM_BLOCK |
 | VK_FORMAT_EAC_R11G11_UNORM_BLOCK |
 | VK_FORMAT_EAC_R11_SNORM_BLOCK |
 | VK_FORMAT_EAC_R11G11_SNORM_BLOCK |
 | VK_FORMAT_PVRTC1_2BPP_UNORM_BLOCK_IMG |
 | VK_FORMAT_PVRTC1_4BPP_UNORM_BLOCK_IMG |
 | VK_FORMAT_PVRTC2_2BPP_UNORM_BLOCK_IMG |
 | VK_FORMAT_PVRTC2_4BPP_UNORM_BLOCK_IMG |
 | VK_FORMAT_PVRTC1_2BPP_SRGB_BLOCK_IMG |
 | VK_FORMAT_PVRTC1_4BPP_SRGB_BLOCK_IMG |
 | VK_FORMAT_PVRTC2_2BPP_SRGB_BLOCK_IMG |
 | VK_FORMAT_PVRTC2_4BPP_SRGB_BLOCK_IMG |
 | VK_FORMAT_ASTC_4x4_UNORM_BLOCK |
 | VK_FORMAT_ASTC_5x4_UNORM_BLOCK |
 | VK_FORMAT_ASTC_5x5_UNORM_BLOCK |
 | VK_FORMAT_ASTC_6x5_UNORM_BLOCK |
 | VK_FORMAT_ASTC_6x6_UNORM_BLOCK |
 | VK_FORMAT_ASTC_8x5_UNORM_BLOCK |
 | VK_FORMAT_ASTC_8x6_UNORM_BLOCK |
 | VK_FORMAT_ASTC_8x8_UNORM_BLOCK |
 | VK_FORMAT_ASTC_10x5_UNORM_BLOCK |
 | VK_FORMAT_ASTC_10x6_UNORM_BLOCK |
 | VK_FORMAT_ASTC_10x8_UNORM_BLOCK |
 | VK_FORMAT_ASTC_10x10_UNORM_BLOCK |
 | VK_FORMAT_ASTC_12x10_UNORM_BLOCK |
 | VK_FORMAT_ASTC_12x12_UNORM_BLOCK |
 | VK_FORMAT_ASTC_4x4_SRGB_BLOCK |
 | VK_FORMAT_ASTC_5x4_SRGB_BLOCK |
 | VK_FORMAT_ASTC_5x5_SRGB_BLOCK |
 | VK_FORMAT_ASTC_6x5_SRGB_BLOCK |
 | VK_FORMAT_ASTC_6x6_SRGB_BLOCK |
 | VK_FORMAT_ASTC_8x5_SRGB_BLOCK |
 | VK_FORMAT_ASTC_8x6_SRGB_BLOCK |
 | VK_FORMAT_ASTC_8x8_SRGB_BLOCK |
 | VK_FORMAT_ASTC_10x5_SRGB_BLOCK |
 | VK_FORMAT_ASTC_10x6_SRGB_BLOCK |
 | VK_FORMAT_ASTC_10x8_SRGB_BLOCK |
 | VK_FORMAT_ASTC_10x10_SRGB_BLOCK |
 | VK_FORMAT_ASTC_12x10_SRGB_BLOCK |
 | VK_FORMAT_ASTC_12x12_SRGB_BLOCK |
 | VK_FORMAT_ASTC_4x4_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_5x4_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_5x5_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_6x5_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_6x6_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_8x5_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_8x6_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_8x8_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_10x5_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_10x6_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_10x8_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_10x10_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_12x10_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_12x12_SFLOAT_BLOCK |
 | VK_FORMAT_ASTC_3x3x3_UNORM_BLOCK_EXT |
 | VK_FORMAT_ASTC_4x3x3_UNORM_BLOCK_EXT |
 | VK_FORMAT_ASTC_4x4x3_UNORM_BLOCK_EXT |
 | VK_FORMAT_ASTC_4x4x4_UNORM_BLOCK_EXT |
 | VK_FORMAT_ASTC_5x4x4_UNORM_BLOCK_EXT |
 | VK_FORMAT_ASTC_5x5x4_UNORM_BLOCK_EXT |
 | VK_FORMAT_ASTC_5x5x5_UNORM_BLOCK_EXT |
 | VK_FORMAT_ASTC_6x5x5_UNORM_BLOCK_EXT |
 | VK_FORMAT_ASTC_6x6x5_UNORM_BLOCK_EXT |
 | VK_FORMAT_ASTC_6x6x6_UNORM_BLOCK_EXT |
 | VK_FORMAT_ASTC_3x3x3_SRGB_BLOCK_EXT |
 | VK_FORMAT_ASTC_4x3x3_SRGB_BLOCK_EXT |
 | VK_FORMAT_ASTC_4x4x3_SRGB_BLOCK_EXT |
 | VK_FORMAT_ASTC_4x4x4_SRGB_BLOCK_EXT |
 | VK_FORMAT_ASTC_5x4x4_SRGB_BLOCK_EXT |
 | VK_FORMAT_ASTC_5x5x4_SRGB_BLOCK_EXT |
 | VK_FORMAT_ASTC_5x5x5_SRGB_BLOCK_EXT |
 | VK_FORMAT_ASTC_6x5x5_SRGB_BLOCK_EXT |
 | VK_FORMAT_ASTC_6x6x5_SRGB_BLOCK_EXT |
 | VK_FORMAT_ASTC_6x6x6_SRGB_BLOCK_EXT |
 | VK_FORMAT_ASTC_3x3x3_SFLOAT_BLOCK_EXT |
 | VK_FORMAT_ASTC_4x3x3_SFLOAT_BLOCK_EXT |
 | VK_FORMAT_ASTC_4x4x3_SFLOAT_BLOCK_EXT |
 | VK_FORMAT_ASTC_4x4x4_SFLOAT_BLOCK_EXT |
 | VK_FORMAT_ASTC_5x4x4_SFLOAT_BLOCK_EXT |
 | VK_FORMAT_ASTC_5x5x4_SFLOAT_BLOCK_EXT |
 | VK_FORMAT_ASTC_5x5x5_SFLOAT_BLOCK_EXT |
 | VK_FORMAT_ASTC_6x5x5_SFLOAT_BLOCK_EXT |
 | VK_FORMAT_ASTC_6x6x5_SFLOAT_BLOCK_EXT |
 | VK_FORMAT_ASTC_6x6x6_SFLOAT_BLOCK_EXT |
 | VK_FORMAT_D16_UNORM |
 | VK_FORMAT_D32_SFLOAT |
 | VK_FORMAT_S8_UINT |
 | VK_FORMAT_D16_UNORM_S8_UINT |
 | VK_FORMAT_D24_UNORM_S8_UINT |
 | VK_FORMAT_X8_D24_UNORM_PACK32 |
 | VK_FORMAT_D32_SFLOAT_S8_UINT |
 | VK_FORMAT_G16_B16_R16_3PLANE_444_UNORM |
 | VK_FORMAT_G12X4_B12X4_R12X4_3PLANE_444_UNORM_3PACK16 |
 | VK_FORMAT_G10X6_B10X6_R10X6_3PLANE_444_UNORM_3PACK16 |
 | VK_FORMAT_G8_B8_R8_3PLANE_444_UNORM |
 | VK_FORMAT_G16_B16R16_2PLANE_444_UNORM |
 | VK_FORMAT_G12X4_B12X4R12X4_2PLANE_444_UNORM_3PACK16 |
 | VK_FORMAT_G10X6_B10X6R10X6_2PLANE_444_UNORM_3PACK16 |
 | VK_FORMAT_G8_B8R8_2PLANE_444_UNORM |
 | VK_FORMAT_G16_B16_R16_3PLANE_422_UNORM |
 | VK_FORMAT_G12X4_B12X4_R12X4_3PLANE_422_UNORM_3PACK16 |
 | VK_FORMAT_G10X6_B10X6_R10X6_3PLANE_422_UNORM_3PACK16 |
 | VK_FORMAT_G8_B8_R8_3PLANE_422_UNORM |
 | VK_FORMAT_G16_B16R16_2PLANE_422_UNORM |
 | VK_FORMAT_G12X4_B12X4R12X4_2PLANE_422_UNORM_3PACK16 |
 | VK_FORMAT_G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16 |
 | VK_FORMAT_G8_B8R8_2PLANE_422_UNORM |
 | VK_FORMAT_G16_B16_R16_3PLANE_420_UNORM |
 | VK_FORMAT_G12X4_B12X4_R12X4_3PLANE_420_UNORM_3PACK16 |
 | VK_FORMAT_G10X6_B10X6_R10X6_3PLANE_420_UNORM_3PACK16 |
 | VK_FORMAT_G8_B8_R8_3PLANE_420_UNORM |
 | VK_FORMAT_G16_B16R16_2PLANE_420_UNORM |
 | VK_FORMAT_G12X4_B12X4R12X4_2PLANE_420_UNORM_3PACK16 |
 | VK_FORMAT_G10X6_B10X6R10X6_2PLANE_420_UNORM_3PACK16 |
 | VK_FORMAT_G8_B8R8_2PLANE_420_UNORM |
 | VK_FORMAT_G16B16G16R16_422_UNORM |
 | VK_FORMAT_G12X4B12X4G12X4R12X4_422_UNORM_4PACK16 |
 | VK_FORMAT_G10X6B10X6G10X6R10X6_422_UNORM_4PACK16 |
 | VK_FORMAT_G8B8G8R8_422_UNORM |
 | VK_FORMAT_B16G16R16G16_422_UNORM |
 | VK_FORMAT_B12X4G12X4R12X4G12X4_422_UNORM_4PACK16 |
 | VK_FORMAT_B10X6G10X6R10X6G10X6_422_UNORM_4PACK16 |
 | VK_FORMAT_B8G8R8G8_422_UNORM |
 | VK_FORMAT_R12X4G12X4B12X4A12X4_UNORM_4PACK16 |
 | VK_FORMAT_R10X6G10X6B10X6A10X6_UNORM_4PACK16 |

 | DXGI Formats |
 | --- |
 | DXGI_FORMAT_R8_UNORM |
 | DXGI_FORMAT_R8G8_UNORM |
 | DXGI_FORMAT_R8G8B8A8_UNORM |
 | DXGI_FORMAT_B8G8R8A8_UNORM |
 | DXGI_FORMAT_B8G8R8X8_UNORM |
 | DXGI_FORMAT_R8_SNORM |
 | DXGI_FORMAT_R8G8_SNORM |
 | DXGI_FORMAT_R8G8B8A8_SNORM |
 | DXGI_FORMAT_R8_UINT |
 | DXGI_FORMAT_R8G8_UINT |
 | DXGI_FORMAT_R8G8B8A8_UINT |
 | DXGI_FORMAT_R8_SINT |
 | DXGI_FORMAT_R8G8_SINT |
 | DXGI_FORMAT_R8G8B8A8_SINT |
 | DXGI_FORMAT_R8G8B8A8_UNORM_SRGB |
 | DXGI_FORMAT_B8G8R8A8_UNORM_SRGB |
 | DXGI_FORMAT_B8G8R8X8_UNORM_SRGB |
 | DXGI_FORMAT_R16_UNORM |
 | DXGI_FORMAT_R16G16_UNORM |
 | DXGI_FORMAT_R16G16B16A16_UNORM |
 | DXGI_FORMAT_R16_SNORM |
 | DXGI_FORMAT_R16G16_SNORM |
 | DXGI_FORMAT_R16G16B16A16_SNORM |
 | DXGI_FORMAT_R16_UINT |
 | DXGI_FORMAT_R16G16_UINT |
 | DXGI_FORMAT_R16G16B16A16_UINT |
 | DXGI_FORMAT_R16_SINT |
 | DXGI_FORMAT_R16G16_SINT |
 | DXGI_FORMAT_R16G16B16A16_SINT |
 | DXGI_FORMAT_R16_FLOAT |
 | DXGI_FORMAT_R16G16_FLOAT |
 | DXGI_FORMAT_R16G16B16A16_FLOAT |
 | DXGI_FORMAT_R32_UINT |
 | DXGI_FORMAT_R32G32_UINT |
 | DXGI_FORMAT_R32G32B32_UINT |
 | DXGI_FORMAT_R32G32B32A32_UINT |
 | DXGI_FORMAT_R32_SINT |
 | DXGI_FORMAT_R32G32_SINT |
 | DXGI_FORMAT_R32G32B32_SINT |
 | DXGI_FORMAT_R32G32B32A32_SINT |
 | DXGI_FORMAT_R32_FLOAT |
 | DXGI_FORMAT_R32G32_FLOAT |
 | DXGI_FORMAT_R32G32B32_FLOAT |
 | DXGI_FORMAT_R32G32B32A32_FLOAT |
 | DXGI_FORMAT_B4G4R4A4_UNORM |
 | DXGI_FORMAT_B5G6R5_UNORM |
 | DXGI_FORMAT_B5G5R5A1_UNORM |
 | DXGI_FORMAT_R10G10B10_XR_BIAS_A2_UNORM |
 | DXGI_FORMAT_R10G10B10A2_UNORM |
 | DXGI_FORMAT_R10G10B10A2_UINT |
 | DXGI_FORMAT_R11G11B10_FLOAT |
 | DXGI_FORMAT_R9G9B9E5_SHAREDEXP |
 | DXGI_FORMAT_A8_UNORM |
 | DXGI_FORMAT_BC1_UNORM |
 | DXGI_FORMAT_BC2_UNORM |
 | DXGI_FORMAT_BC3_UNORM |
 | DXGI_FORMAT_BC1_UNORM_SRGB |
 | DXGI_FORMAT_BC2_UNORM_SRGB |
 | DXGI_FORMAT_BC3_UNORM_SRGB |
 | DXGI_FORMAT_BC4_UNORM |
 | DXGI_FORMAT_BC5_UNORM |
 | DXGI_FORMAT_BC4_SNORM |
 | DXGI_FORMAT_BC5_SNORM |
 | DXGI_FORMAT_BC6H_UF16 |
 | DXGI_FORMAT_BC7_UNORM |
 | DXGI_FORMAT_BC7_UNORM_SRGB |
 | DXGI_FORMAT_D16_UNORM |
 | DXGI_FORMAT_D32_FLOAT |
 | DXGI_FORMAT_D24_UNORM_S8_UINT |
 | DXGI_FORMAT_D32_FLOAT_S8X24_UINT |
 | DXGI_FORMAT_P216 |
 | DXGI_FORMAT_P210 |
 | DXGI_FORMAT_P208 |
 | DXGI_FORMAT_420_OPAQUE |
 | DXGI_FORMAT_YV12 |
 | DXGI_FORMAT_P016 |
 | DXGI_FORMAT_P010 |
 | DXGI_FORMAT_NV12 |
 | DXGI_FORMAT_NV21 |
 | DXGI_FORMAT_Y216 |
 | DXGI_FORMAT_Y210 |
 | DXGI_FORMAT_G8R8_G8B8_UNORM |
 | DXGI_FORMAT_YUY2 |
 | DXGI_FORMAT_R8G8_B8G8_UNORM |
 | DXGI_FORMAT_Y416 |
 | DXGI_FORMAT_Y410 |
 | DXGI_FORMAT_AYUV |

 | Metal Formats |
 | --- |
 | MTLPixelFormatR8Unorm |
 | MTLPixelFormatRG8Unorm |
 | MTLPixelFormatRGBA8Unorm |
 | MTLPixelFormatBGRA8Unorm |
 | MTLPixelFormatR8Snorm |
 | MTLPixelFormatRG8Snorm |
 | MTLPixelFormatRGBA8Snorm |
 | MTLPixelFormatR8Uint |
 | MTLPixelFormatRG8Uint |
 | MTLPixelFormatRGBA8Uint |
 | MTLPixelFormatR8Sint |
 | MTLPixelFormatRG8Sint |
 | MTLPixelFormatRGBA8Sint |
 | MTLPixelFormatR8Unorm_sRGB |
 | MTLPixelFormatR8Unorm_sRGB |
 | MTLPixelFormatRG8Unorm_sRGB |
 | MTLPixelFormatRG8Unorm_sRGB |
 | MTLPixelFormatRGBA8Unorm_sRGB |
 | MTLPixelFormatBGRA8Unorm_sRGB |
 | MTLPixelFormatR16Unorm |
 | MTLPixelFormatRG16Unorm |
 | MTLPixelFormatRGBA16Unorm |
 | MTLPixelFormatR16Snorm |
 | MTLPixelFormatRG16Snorm |
 | MTLPixelFormatRGBA16Snorm |
 | MTLPixelFormatR16Uint |
 | MTLPixelFormatRG16Uint |
 | MTLPixelFormatRGBA16Uint |
 | MTLPixelFormatR16Sint |
 | MTLPixelFormatRG16Sint |
 | MTLPixelFormatRGBA16Sint |
 | MTLPixelFormatR16Float |
 | MTLPixelFormatRG16Float |
 | MTLPixelFormatRGBA16Float |
 | MTLPixelFormatR32Uint |
 | MTLPixelFormatRG32Uint |
 | MTLPixelFormatRGBA32Uint |
 | MTLPixelFormatR32Sint |
 | MTLPixelFormatRG32Sint |
 | MTLPixelFormatRGBA32Sint |
 | MTLPixelFormatR32Float |
 | MTLPixelFormatRG32Float |
 | MTLPixelFormatRGBA32Float |
 | MTLPixelFormatABGR4Unorm |
 | MTLPixelFormatB5G6R5Unorm |
 | MTLPixelFormatA1BGR5Unorm |
 | MTLPixelFormatBGR5A1Unorm |
 | MTLPixelFormatBGR10A2Unorm |
 | MTLPixelFormatRGB10A2Unorm |
 | MTLPixelFormatRGB10A2Uint |
 | MTLPixelFormatRG11B10Float |
 | MTLPixelFormatRGB9E5Float |
 | MTLPixelFormatA8Unorm |
 | MTLPixelFormatBC1_RGBA |
 | MTLPixelFormatBC2_RGBA |
 | MTLPixelFormatBC3_RGBA |
 | MTLPixelFormatBC1_RGBA_sRGB |
 | MTLPixelFormatBC2_RGBA_sRGB |
 | MTLPixelFormatBC3_RGBA_sRGB |
 | MTLPixelFormatBC4_RUnorm |
 | MTLPixelFormatBC5_RGUnorm |
 | MTLPixelFormatBC4_RSnorm |
 | MTLPixelFormatBC5_RGSnorm |
 | MTLPixelFormatBC6H_RGBUfloat |
 | MTLPixelFormatBC7_RGBAUnorm |
 | MTLPixelFormatBC7_RGBAUnorm_sRGB |
 | MTLPixelFormatETC2_RGB8 |
 | MTLPixelFormatETC2_RGB8A1 |
 | MTLPixelFormatEAC_RGBA8 |
 | MTLPixelFormatETC2_RGB8_sRGB |
 | MTLPixelFormatETC2_RGB8A1_sRGB |
 | MTLPixelFormatEAC_RGBA8_sRGB |
 | MTLPixelFormatEAC_R11Unorm |
 | MTLPixelFormatEAC_RG11Unorm |
 | MTLPixelFormatEAC_R11Snorm |
 | MTLPixelFormatEAC_RG11Snorm |
 | MTLPixelFormatPVRTC_RGB_2BPP |
 | MTLPixelFormatPVRTC_RGB_4BPP |
 | MTLPixelFormatPVRTC_RGBA_2BPP |
 | MTLPixelFormatPVRTC_RGBA_4BPP |
 | MTLPixelFormatPVRTC_RGB_2BPP_sRGB |
 | MTLPixelFormatPVRTC_RGB_4BPP_sRGB |
 | MTLPixelFormatPVRTC_RGBA_2BPP_sRGB |
 | MTLPixelFormatPVRTC_RGBA_4BPP_sRGB |
 | MTLPixelFormatASTC_4x4_LDR |
 | MTLPixelFormatASTC_5x4_LDR |
 | MTLPixelFormatASTC_5x5_LDR |
 | MTLPixelFormatASTC_6x5_LDR |
 | MTLPixelFormatASTC_6x6_LDR |
 | MTLPixelFormatASTC_8x5_LDR |
 | MTLPixelFormatASTC_8x6_LDR |
 | MTLPixelFormatASTC_8x8_LDR |
 | MTLPixelFormatASTC_10x5_LDR |
 | MTLPixelFormatASTC_10x6_LDR |
 | MTLPixelFormatASTC_10x8_LDR |
 | MTLPixelFormatASTC_10x10_LDR |
 | MTLPixelFormatASTC_12x10_LDR |
 | MTLPixelFormatASTC_12x12_LDR |
 | MTLPixelFormatASTC_4x4_sRGB |
 | MTLPixelFormatASTC_5x4_sRGB |
 | MTLPixelFormatASTC_5x5_sRGB |
 | MTLPixelFormatASTC_6x5_sRGB |
 | MTLPixelFormatASTC_6x6_sRGB |
 | MTLPixelFormatASTC_8x5_sRGB |
 | MTLPixelFormatASTC_8x6_sRGB |
 | MTLPixelFormatASTC_8x8_sRGB |
 | MTLPixelFormatASTC_10x5_sRGB |
 | MTLPixelFormatASTC_10x6_sRGB |
 | MTLPixelFormatASTC_10x8_sRGB |
 | MTLPixelFormatASTC_10x10_sRGB |
 | MTLPixelFormatASTC_12x10_sRGB |
 | MTLPixelFormatASTC_12x12_sRGB |
 | MTLPixelFormatASTC_4x4_HDR |
 | MTLPixelFormatASTC_5x4_HDR |
 | MTLPixelFormatASTC_5x5_HDR |
 | MTLPixelFormatASTC_6x5_HDR |
 | MTLPixelFormatASTC_6x6_HDR |
 | MTLPixelFormatASTC_8x5_HDR |
 | MTLPixelFormatASTC_8x6_HDR |
 | MTLPixelFormatASTC_8x8_HDR |
 | MTLPixelFormatASTC_10x5_HDR |
 | MTLPixelFormatASTC_10x6_HDR |
 | MTLPixelFormatASTC_10x8_HDR |
 | MTLPixelFormatASTC_10x10_HDR |
 | MTLPixelFormatASTC_12x10_HDR |
 | MTLPixelFormatASTC_12x12_HDR |
 | MTLPixelFormatDepth16Unorm |
 | MTLPixelFormatDepth32Float |
 | MTLPixelFormatStencil8 |
 | MTLPixelFormatDepth24Unorm_Stencil8 |
 | MTLPixelFormatDepth32Float_Stencil8 |
 | MTLPixelFormatGBGR422 |
 | MTLPixelFormatBGRG422 |

 | OpenGL Formats |
 | --- |
 | GL_R8	 GL_UNSIGNED_BYTE	 GL_RED |
 | GL_RG8	 GL_UNSIGNED_BYTE	 GL_RG |
 | GL_RGB8	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_RGB8	 GL_UNSIGNED_BYTE	 GL_BGR |
 | GL_RGBA8	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_RGBA8	 GL_UNSIGNED_BYTE	 GL_BGRA |
 | GL_R8_SNORM	 GL_BYTE	 GL_RED |
 | GL_RG8_SNORM	 GL_BYTE	 GL_RG |
 | GL_RGB8_SNORM	 GL_BYTE	 GL_RGB |
 | GL_RGB8_SNORM	 GL_BYTE	 GL_BGR |
 | GL_RGBA8_SNORM	 GL_BYTE	 GL_RGBA |
 | GL_RGBA8_SNORM	 GL_BYTE	 GL_BGRA |
 | GL_R8UI	 GL_UNSIGNED_BYTE	 GL_RED_INTEGER |
 | GL_RG8UI	 GL_UNSIGNED_BYTE	 GL_RG_INTEGER |
 | GL_RGB8UI	 GL_UNSIGNED_BYTE	 GL_RGB_INTEGER |
 | GL_RGB8UI	 GL_UNSIGNED_BYTE	 GL_BGR_INTEGER |
 | GL_RGBA8UI	 GL_UNSIGNED_BYTE	 GL_RGBA_INTEGER |
 | GL_RGBA8UI	 GL_UNSIGNED_BYTE	 GL_BGRA_INTEGER |
 | GL_R8I	 GL_BYTE	 GL_RED_INTEGER |
 | GL_RG8I	 GL_BYTE	 GL_RG_INTEGER |
 | GL_RGB8I	 GL_BYTE	 GL_RGB_INTEGER |
 | GL_RGB8I	 GL_BYTE	 GL_BGR_INTEGER |
 | GL_RGBA8I	 GL_BYTE	 GL_RGBA_INTEGER |
 | GL_RGBA8I	 GL_BYTE	 GL_BGRA_INTEGER |
 | GL_SR8	 GL_UNSIGNED_BYTE	 GL_RED |
 | GL_SR8_EXT	 GL_UNSIGNED_BYTE	 GL_RED |
 | GL_SRG8	 GL_UNSIGNED_BYTE	 GL_RG |
 | GL_SRG8_EXT	 GL_UNSIGNED_BYTE	 GL_RG |
 | GL_SRGB8	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_SRGB8	 GL_UNSIGNED_BYTE	 GL_BGR |
 | GL_SRGB8_ALPHA8	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_SRGB8_ALPHA8	 GL_UNSIGNED_BYTE	 GL_BGRA |
 | GL_R16	 GL_UNSIGNED_SHORT	 GL_RED |
 | GL_RG16	 GL_UNSIGNED_SHORT	 GL_RG |
 | GL_RGB16	 GL_UNSIGNED_SHORT	 GL_RGB |
 | GL_RGBA16	 GL_UNSIGNED_SHORT	 GL_RGBA |
 | GL_R16_SNORM	 GL_SHORT	 GL_RED |
 | GL_RG16_SNORM	 GL_SHORT	 GL_RG |
 | GL_RGB16_SNORM	 GL_SHORT	 GL_RGB |
 | GL_RGBA16_SNORM	 GL_SHORT	 GL_RGBA |
 | GL_R16UI	 GL_UNSIGNED_SHORT	 GL_RED_INTEGER |
 | GL_RG16UI	 GL_UNSIGNED_SHORT	 GL_RG_INTEGER |
 | GL_RGB16UI	 GL_UNSIGNED_SHORT	 GL_RGB_INTEGER |
 | GL_RGBA16UI	 GL_UNSIGNED_SHORT	 GL_RGBA_INTEGER |
 | GL_R16I	 GL_SHORT	 GL_RED_INTEGER |
 | GL_RG16I	 GL_SHORT	 GL_RG_INTEGER |
 | GL_RGB16I	 GL_SHORT	 GL_RGB_INTEGER |
 | GL_RGBA16I	 GL_SHORT	 GL_RGBA_INTEGER |
 | GL_R16F	 GL_HALF_FLOAT	 GL_RED |
 | GL_RG16F	 GL_HALF_FLOAT	 GL_RG |
 | GL_RGB16F	 GL_HALF_FLOAT	 GL_RGB |
 | GL_RGBA16F	 GL_HALF_FLOAT	 GL_RGBA |
 | GL_R32UI	 GL_UNSIGNED_INT	 GL_RED_INTEGER |
 | GL_RG32UI	 GL_UNSIGNED_INT	 GL_RG_INTEGER |
 | GL_RGB32UI	 GL_UNSIGNED_INT	 GL_RGB_INTEGER |
 | GL_RGBA32UI	 GL_UNSIGNED_INT	 GL_RGBA_INTEGER |
 | GL_R32I	 GL_INT	 GL_RED_INTEGER |
 | GL_RG32I	 GL_INT	 GL_RG_INTEGER |
 | GL_RGB32I	 GL_INT	 GL_RGB_INTEGER |
 | GL_RGBA32I	 GL_INT	 GL_RGBA_INTEGER |
 | GL_R32F	 GL_FLOAT	 GL_RED |
 | GL_RG32F	 GL_FLOAT	 GL_RG |
 | GL_RGB32F	 GL_FLOAT	 GL_RGB |
 | GL_RGBA32F	 GL_FLOAT	 GL_RGBA |
 | GL_R3_G3_B2	 GL_UNSIGNED_BYTE_2_3_3_REV	 GL_RGB |
 | GL_RGB4	 GL_UNSIGNED_SHORT_4_4_4_4	 GL_RGB |
 | GL_RGB4	 GL_UNSIGNED_SHORT_4_4_4_4_REV	 GL_RGB |
 | GL_RGBA4	 GL_UNSIGNED_SHORT_4_4_4_4	 GL_RGBA |
 | GL_RGBA4	 GL_UNSIGNED_SHORT_4_4_4_4	 GL_BGRA |
 | GL_RGBA4	 GL_UNSIGNED_SHORT_4_4_4_4_REV	 GL_BGRA |
 | GL_RGBA4	 GL_UNSIGNED_SHORT_4_4_4_4_REV	 GL_RGBA |
 | GL_RGB5	 GL_UNSIGNED_SHORT_1_5_5_5_REV	 GL_RGB |
 | GL_RGB565	 GL_UNSIGNED_SHORT_5_6_5	 GL_RGB |
 | GL_RGB565	 GL_UNSIGNED_SHORT_5_6_5_REV	 GL_RGB |
 | GL_RGB10	 GL_UNSIGNED_SHORT	 GL_RGB |
 | GL_RGB12	 GL_UNSIGNED_SHORT	 GL_RGB |
 | GL_RGBA2	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_RGBA12	 GL_UNSIGNED_SHORT	 GL_RGBA |
 | GL_RGB5_A1	 GL_UNSIGNED_SHORT_5_5_5_1	 GL_RGBA |
 | GL_RGB5_A1	 GL_UNSIGNED_SHORT_5_5_5_1	 GL_BGRA |
 | GL_RGB5_A1	 GL_UNSIGNED_SHORT_1_5_5_5_REV	 GL_RGBA |
 | GL_RGB5_A1	 GL_UNSIGNED_SHORT_1_5_5_5_REV	 GL_BGRA |
 | GL_RGBA8	 GL_UNSIGNED_BYTE_3_3_2	 GL_BGRA |
 | GL_RGB10_A2	 GL_UNSIGNED_INT_2_10_10_10_REV	 GL_BGRA |
 | GL_RGB10_A2	 GL_UNSIGNED_INT_2_10_10_10_REV	 GL_RGBA |
 | GL_RGB10_A2UI	 GL_UNSIGNED_INT_2_10_10_10_REV	 GL_BGRA_INTEGER |
 | GL_RGB10_A2UI	 GL_UNSIGNED_INT_2_10_10_10_REV	 GL_RGBA_INTEGER |
 | GL_R11F_G11F_B10F	 GL_UNSIGNED_INT_10F_11F_11F_REV	 GL_RGB |
 | GL_RGB9_E5	 GL_UNSIGNED_INT_5_9_9_9_REV	 GL_RGB |
 | GL_ALPHA4	 GL_UNSIGNED_BYTE	 GL_ALPHA |
 | GL_ALPHA8	 GL_UNSIGNED_BYTE	 GL_ALPHA |
 | GL_ALPHA8_SNORM	 GL_BYTE	 GL_ALPHA |
 | GL_ALPHA8UI_EXT	 GL_UNSIGNED_BYTE	 GL_ALPHA_INTEGER |
 | GL_ALPHA8I_EXT	 GL_BYTE	 GL_ALPHA_INTEGER |
 | GL_ALPHA12	 GL_UNSIGNED_SHORT	 GL_ALPHA |
 | GL_ALPHA16	 GL_UNSIGNED_SHORT	 GL_ALPHA |
 | GL_ALPHA16_SNORM	 GL_SHORT	 GL_ALPHA |
 | GL_ALPHA16UI_EXT	 GL_UNSIGNED_SHORT	 GL_ALPHA_INTEGER |
 | GL_ALPHA16I_EXT	 GL_SHORT	 GL_ALPHA_INTEGER |
 | GL_ALPHA16F_ARB	 GL_HALF_FLOAT	 GL_ALPHA |
 | GL_ALPHA32UI_EXT	 GL_UNSIGNED_INT	 GL_ALPHA_INTEGER |
 | GL_ALPHA32I_EXT	 GL_INT	 GL_ALPHA_INTEGER |
 | GL_ALPHA32F_ARB	 GL_FLOAT	 GL_ALPHA |
 | GL_LUMINANCE4	 GL_UNSIGNED_BYTE	 GL_LUMINANCE |
 | GL_LUMINANCE8	 GL_UNSIGNED_BYTE	 GL_LUMINANCE |
 | GL_LUMINANCE8_SNORM	 GL_BYTE	 GL_LUMINANCE |
 | GL_SLUMINANCE8	 GL_UNSIGNED_BYTE	 GL_LUMINANCE |
 | GL_LUMINANCE8UI_EXT	 GL_UNSIGNED_BYTE	 GL_LUMINANCE_INTEGER |
 | GL_LUMINANCE8I_EXT	 GL_BYTE	 GL_LUMINANCE_INTEGER |
 | GL_LUMINANCE12	 GL_UNSIGNED_SHORT	 GL_LUMINANCE |
 | GL_LUMINANCE16	 GL_UNSIGNED_SHORT	 GL_LUMINANCE |
 | GL_LUMINANCE16_SNORM	 GL_SHORT	 GL_LUMINANCE |
 | GL_LUMINANCE16UI_EXT	 GL_UNSIGNED_SHORT	 GL_LUMINANCE_INTEGER |
 | GL_LUMINANCE16I_EXT	 GL_SHORT	 GL_LUMINANCE_INTEGER |
 | GL_LUMINANCE16F_ARB	 GL_HALF_FLOAT	 GL_LUMINANCE |
 | GL_LUMINANCE32UI_EXT	 GL_UNSIGNED_INT	 GL_LUMINANCE_INTEGER |
 | GL_LUMINANCE32I_EXT	 GL_INT	 GL_LUMINANCE_INTEGER |
 | GL_LUMINANCE32F_ARB	 GL_FLOAT	 GL_LUMINANCE |
 | GL_LUMINANCE4_ALPHA4	 GL_UNSIGNED_BYTE	 GL_LUMINANCE_ALPHA |
 | GL_LUMINANCE6_ALPHA2	 GL_UNSIGNED_BYTE	 GL_LUMINANCE_ALPHA |
 | GL_LUMINANCE8_ALPHA8	 GL_UNSIGNED_BYTE	 GL_LUMINANCE_ALPHA |
 | GL_LUMINANCE8_ALPHA8_SNORM	 GL_BYTE	 GL_LUMINANCE_ALPHA |
 | GL_SLUMINANCE8_ALPHA8	 GL_UNSIGNED_BYTE	 GL_LUMINANCE_ALPHA |
 | GL_LUMINANCE_ALPHA8UI_EXT	 GL_UNSIGNED_BYTE	 GL_LUMINANCE_ALPHA_INTEGER |
 | GL_LUMINANCE_ALPHA8I_EXT	 GL_BYTE	 GL_LUMINANCE_ALPHA_INTEGER |
 | GL_LUMINANCE12_ALPHA4	 GL_UNSIGNED_SHORT	 GL_LUMINANCE_ALPHA |
 | GL_LUMINANCE12_ALPHA12	 GL_UNSIGNED_SHORT	 GL_LUMINANCE_ALPHA |
 | GL_LUMINANCE16_ALPHA16	 GL_UNSIGNED_SHORT	 GL_LUMINANCE_ALPHA |
 | GL_LUMINANCE16_ALPHA16_SNORM	 GL_SHORT	 GL_LUMINANCE_ALPHA |
 | GL_LUMINANCE_ALPHA16UI_EXT	 GL_UNSIGNED_SHORT	 GL_LUMINANCE_ALPHA_INTEGER |
 | GL_LUMINANCE_ALPHA16I_EXT	 GL_SHORT	 GL_LUMINANCE_ALPHA_INTEGER |
 | GL_LUMINANCE_ALPHA16F_ARB	 GL_HALF_FLOAT	 GL_LUMINANCE_ALPHA |
 | GL_LUMINANCE_ALPHA32UI_EXT	 GL_UNSIGNED_INT	 GL_LUMINANCE_ALPHA_INTEGER |
 | GL_LUMINANCE_ALPHA32I_EXT	 GL_INT	 GL_LUMINANCE_ALPHA_INTEGER |
 | GL_LUMINANCE_ALPHA32F_ARB	 GL_FLOAT	 GL_LUMINANCE_ALPHA |
 | GL_INTENSITY4	 GL_UNSIGNED_BYTE	 GL_LUMINANCE |
 | GL_INTENSITY8	 GL_UNSIGNED_BYTE	 GL_LUMINANCE |
 | GL_INTENSITY8_SNORM	 GL_BYTE	 GL_LUMINANCE |
 | GL_INTENSITY8UI_EXT	 GL_UNSIGNED_BYTE	 GL_LUMINANCE_INTEGER |
 | GL_INTENSITY8I_EXT	 GL_BYTE	 GL_LUMINANCE_INTEGER |
 | GL_INTENSITY12	 GL_UNSIGNED_SHORT	 GL_LUMINANCE |
 | GL_INTENSITY16	 GL_UNSIGNED_SHORT	 GL_LUMINANCE |
 | GL_INTENSITY16_SNORM	 GL_SHORT	 GL_LUMINANCE |
 | GL_INTENSITY16UI_EXT	 GL_UNSIGNED_SHORT	 GL_LUMINANCE_INTEGER |
 | GL_INTENSITY16I_EXT	 GL_SHORT	 GL_LUMINANCE_INTEGER |
 | GL_INTENSITY16F_ARB	 GL_HALF_FLOAT	 GL_LUMINANCE |
 | GL_INTENSITY32UI_EXT	 GL_UNSIGNED_INT	 GL_LUMINANCE_INTEGER |
 | GL_INTENSITY32I_EXT	 GL_INT	 GL_LUMINANCE_INTEGER |
 | GL_INTENSITY32F_ARB	 GL_FLOAT	 GL_LUMINANCE |
 | GL_COMPRESSED_RED	 GL_UNSIGNED_BYTE	 GL_RED |
 | GL_COMPRESSED_ALPHA	 GL_UNSIGNED_BYTE	 GL_ALPHA |
 | GL_COMPRESSED_LUMINANCE	 GL_UNSIGNED_BYTE	 GL_LUMINANCE |
 | GL_COMPRESSED_SLUMINANCE	 GL_UNSIGNED_BYTE	 GL_LUMINANCE |
 | GL_COMPRESSED_LUMINANCE_ALPHA	 GL_UNSIGNED_BYTE	 GL_LUMINANCE_ALPHA |
 | GL_COMPRESSED_SLUMINANCE_ALPHA	 GL_UNSIGNED_BYTE	 GL_LUMINANCE_ALPHA |
 | GL_COMPRESSED_INTENSITY	 GL_UNSIGNED_BYTE	 GL_LUMINANCE |
 | GL_COMPRESSED_RG	 GL_UNSIGNED_BYTE	 GL_RG |
 | GL_COMPRESSED_RGB	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_COMPRESSED_RGBA	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_COMPRESSED_SRGB_ALPHA	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGB_S3TC_DXT1_EXT	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_COMPRESSED_RGBA_S3TC_DXT1_EXT	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_S3TC_DXT3_EXT	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_S3TC_DXT5_EXT	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB_S3TC_DXT1_EXT	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_LUMINANCE_LATC1_EXT	 GL_UNSIGNED_BYTE	 GL_RED |
 | GL_COMPRESSED_LUMINANCE_ALPHA_LATC2_EXT	 GL_UNSIGNED_BYTE	 GL_RG |
 | GL_COMPRESSED_SIGNED_LUMINANCE_LATC1_EXT	 GL_UNSIGNED_BYTE	 GL_RED |
 | GL_COMPRESSED_SIGNED_LUMINANCE_ALPHA_LATC2_EXT	 GL_UNSIGNED_BYTE	 GL_RG |
 | GL_COMPRESSED_RED_RGTC1	 GL_UNSIGNED_BYTE	 GL_RED |
 | GL_COMPRESSED_RG_RGTC2	 GL_UNSIGNED_BYTE	 GL_RG |
 | GL_COMPRESSED_SIGNED_RED_RGTC1	 GL_UNSIGNED_BYTE	 GL_RED |
 | GL_COMPRESSED_SIGNED_RG_RGTC2	 GL_UNSIGNED_BYTE	 GL_RG |
 | GL_COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT	 GL_FLOAT	 GL_RGB |
 | GL_COMPRESSED_RGBA_BPTC_UNORM	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB_ALPHA_BPTC_UNORM	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_ETC1_RGB8_OES	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_COMPRESSED_RGB8_ETC2	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_COMPRESSED_RGB8_PUNCHTHROUGH_ALPHA1_ETC2	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA8_ETC2_EAC	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ETC2	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_COMPRESSED_SRGB8_PUNCHTHROUGH_ALPHA1_ETC2	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ETC2_EAC	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_R11_EAC	 GL_UNSIGNED_BYTE	 GL_RED |
 | GL_COMPRESSED_RG11_EAC	 GL_UNSIGNED_BYTE	 GL_RG |
 | GL_COMPRESSED_SIGNED_R11_EAC	 GL_UNSIGNED_BYTE	 GL_RED |
 | GL_COMPRESSED_SIGNED_RG11_EAC	 GL_UNSIGNED_BYTE	 GL_RG |
 | GL_COMPRESSED_RGB_PVRTC_2BPPV1_IMG	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_COMPRESSED_RGB_PVRTC_4BPPV1_IMG	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_COMPRESSED_RGBA_PVRTC_2BPPV1_IMG	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_PVRTC_4BPPV1_IMG	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_PVRTC_2BPPV2_IMG	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_PVRTC_4BPPV2_IMG	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB_PVRTC_2BPPV1_EXT	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_COMPRESSED_SRGB_PVRTC_4BPPV1_EXT	 GL_UNSIGNED_BYTE	 GL_RGB |
 | GL_COMPRESSED_SRGB_ALPHA_PVRTC_2BPPV1_EXT	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB_ALPHA_PVRTC_4BPPV1_EXT	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB_ALPHA_PVRTC_2BPPV2_IMG	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB_ALPHA_PVRTC_4BPPV2_IMG	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_4x4_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_5x4_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_5x5_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_6x5_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_6x6_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_8x5_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_8x6_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_8x8_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_10x5_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_10x6_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_10x8_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_10x10_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_12x10_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_12x12_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_3x3x3_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_4x3x3_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_4x4x3_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_4x4x4_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_5x4x4_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_5x5x4_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_5x5x5_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_6x5x5_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_6x6x5_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_RGBA_ASTC_6x6x6_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_3x3x3_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x3x3_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x4x3_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x4x4_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x4x4_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x5x4_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x5x5_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x5x5_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x6x5_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x6x6_OES	 GL_UNSIGNED_BYTE	 GL_RGBA |
 | GL_COLOR_INDEX1_EXT	 GL_UNSIGNED_BYTE	 GL_COLOR_INDEX |
 | GL_COLOR_INDEX2_EXT	 GL_UNSIGNED_BYTE	 GL_COLOR_INDEX |
 | GL_COLOR_INDEX4_EXT	 GL_UNSIGNED_BYTE	 GL_COLOR_INDEX |
 | GL_COLOR_INDEX8_EXT	 GL_UNSIGNED_BYTE	 GL_COLOR_INDEX |
 | GL_COLOR_INDEX12_EXT	 GL_UNSIGNED_SHORT	 GL_COLOR_INDEX |
 | GL_COLOR_INDEX16_EXT	 GL_UNSIGNED_SHORT	 GL_COLOR_INDEX |
 | GL_DEPTH_COMPONENT16	 GL_UNSIGNED_SHORT	 GL_DEPTH_COMPONENT |
 | GL_DEPTH_COMPONENT24	 GL_UNSIGNED_INT	 GL_DEPTH_COMPONENT |
 | GL_DEPTH_COMPONENT32	 GL_UNSIGNED_INT	 GL_DEPTH_COMPONENT |
 | GL_DEPTH_COMPONENT32F	 GL_FLOAT	 GL_DEPTH_COMPONENT |
 | GL_DEPTH_COMPONENT32F_NV	 GL_FLOAT	 GL_DEPTH_COMPONENT |
 | GL_STENCIL_INDEX1	 GL_UNSIGNED_BYTE	 GL_STENCIL_INDEX |
 | GL_STENCIL_INDEX4	 GL_UNSIGNED_BYTE	 GL_STENCIL_INDEX |
 | GL_STENCIL_INDEX8	 GL_UNSIGNED_BYTE	 GL_STENCIL_INDEX |
 | GL_STENCIL_INDEX16	 GL_UNSIGNED_BYTE	 GL_STENCIL_INDEX |
 | GL_DEPTH24_STENCIL8	 GL_UNSIGNED_INT_24_8	 GL_DEPTH_STENCIL |
 | GL_DEPTH32F_STENCIL8	 GL_FLOAT_32_UNSIGNED_INT_24_8_REV	 GL_DEPTH_STENCIL |
 | GL_DEPTH32F_STENCIL8_NV	 GL_FLOAT_32_UNSIGNED_INT_24_8_REV	 GL_DEPTH_STENCIL |

…and more!
As well as a proper help file/documentation.
Wow!
