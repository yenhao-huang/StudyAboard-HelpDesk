# **高解析度 GIF 轉換 (最佳化版)**

## **方法：兩步驟 (建議)**

### **步驟 1 — 生成高品質調色盤**

```bash
ffmpeg -i metadata/rag_chabot.mp4 -vf "fps=20,scale=1280:-1:flags=lanczos,palettegen" palette.png
```

**參數解釋：**

* `fps=20` → 增加幀率，GIF 更流暢。
* `scale=1280:-1` → **寬度 1280px**，解析度提高。
* `flags=lanczos` → 使用高品質縮放演算法。
* `palettegen` → 建立專屬調色盤，保持顏色準確。

---

### **步驟 2 — 使用調色盤生成高解析度 GIF**

```bash
ffmpeg -i metadata/rag_chabot.mp4 -i palette.png \
-filter_complex "fps=20,scale=1280:-1:flags=lanczos[x];[x][1:v]paletteuse" demo_hd.gif
```
