# Witrn K2 PD Analyzer

**Witrn K2 PD Analyzer** is a desktop Power Delivery (PD) packet analysis software designed for the **WITRN K2 USB power tester**.  
It supports real-time monitoring, decoding, and visualization of PD communication data.  
Ideal for USB PD debugging, adapter identification, and protocol research.

---

## 🖼️ Interface Overview

![Witrn K2 PD Analyzer Screenshot](./2ea1cdcb-faac-4916-aa3e-3c7ce7ba7659.png)

The interface displays:

- Real-time voltage, current, DP/DM voltage, and CC voltage  
- PD message direction, type, raw data, and parsed contents  
- Apple vendor-defined VDM decoding results  
- Device status and connection logs  
- One-click filtering, sorting, and PD message statistics  

---

## ⚙️ Features

- ✅ **Real-time PD packet decoding**  
- ✅ **Live display of electrical parameters**  
- ✅ **Log output with filtering and search functions**  
- ✅ **PD message counting and statistics**  
- ✅ **Apple PD adapter information decoding**  
- ✅ **Clean and intuitive graphical interface**  
- 🔘 **More features coming soon...**

---

## 💡 How to Use

1. Connect the **WITRN K2** device to your computer  
2. Open this software, click **Refresh**, and select your device (e.g., `WITRN.K2 (SN: 20230727)`)  
3. Click **Open** to establish the connection  
4. When the message `Device opened successfully. Starting read loop...` appears, the connection is successful  
5. PD communication logs will appear in the **PD Messages** window; select any entry to view detailed information in the **Message Details** panel  

---

## 🔧 Extended Features (as of V1.2)

- **Data Filtering:** Right-click the **SOP / Message Type / Direction** column headers to filter data for easier analysis  
- **Color Settings:** Configure text and background colors for message entries in **Color Settings** at the bottom right  
- **Apple Adapter Capture:** When connected to an Apple USB-C PD adapter, the analyzer can capture and decode PD packets exchanged with the power adapter  

---

## ⚠️ Notes

- This software requires the **WITRN K2** hardware device to function  
- Displayed PD packets and electrical data are for debugging and analysis only — not for precision measurement  
- If you encounter connection issues or incorrect data, ensure the device firmware is version **3.9 or above**, and that **PD Online Mode** is enabled in settings  
- Some PD messages may be misidentified; please verify results carefully  

---

## 🧩 Compatibility

| Platform              | Status   |
| --------------------- | -------- |
| macOS (Apple Silicon) | ✅ Tested |
| Windows 10 / 11       | ✅ Tested |

---

## 📦 Download

Visit the [Releases](../../releases) page to download the latest executable version.

---

## 📜 License

This software and all accompanying files are the proprietary property of the author.  
**Not open source.**  
For personal or internal use only.  
Modification, decompilation, or redistribution is strictly prohibited.  
See [LICENSE.txt](./LICENSE.txt) and [LICENSE_zh.txt](./LICENSE_zh.txt) for details.

---

## ✉️ Contact

**Niboe Kaiwet**  
For commercial licensing or technical inquiries, please contact via **GitHub Issues**.

---

© 2025 Niboe Kaiwet – All rights reserved