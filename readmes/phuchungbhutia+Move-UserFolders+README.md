# Move-UserFolders.ps1
[![GitHub stars](https://img.shields.io/github/stars/phuchungbhutia/Move-UserFolders)](https://github.com/phuchungbhutia/Move-UserFolders/stargazers) [![License](https://img.shields.io/github/license/phuchungbhutia/Move-UserFolders)](https://github.com/phuchungbhutia/Move-UserFolders/blob/main/LICENSE) [![Workflow Status](https://img.shields.io/github/workflow/status/phuchungbhutia/Move-UserFolders/Update%20Prompt%20Indexes)](https://github.com/phuchungbhutia/Move-UserFolders/actions) [![Contributors](https://img.shields.io/github/contributors/phuchungbhutia/Move-UserFolders)](https://github.com/phuchungbhutia/Move-UserFolders/graphs/contributors) [![Last Updated](https://img.shields.io/github/last-commit/phuchungbhutia/Move-UserFolders/main?label=Last%20Updated)](https://github.com/phuchungbhutia/Move-UserFolders/commits/main)

A PowerShell script to automatically move default user folders (like Desktop, Documents, Downloads, etc.) from `C:\Users\<username>` to `D:\Users\<username>` in Windows 11. The script also updates the Windows Registry so the system uses the new locations as defaults.

## Repository Stats

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=phuchungbhutia&show_icons=true&theme=radical)
## ⚙️ Features

- Automatically detects the currently logged-in user
- Moves contents of:
  - Desktop
  - Documents
  - Downloads
  - Music
  - Pictures
  - Videos
- Updates registry paths accordingly
- Restarts File Explorer to apply changes

## 🧪 Tested On

- Windows 11 (22H2 and 23H2)
- PowerShell 5.1+

---

## 🚀 How to Use

### ✅ Step 1: Download the Script

You can clone the repo or download just the script file:

```bash
git clone https://github.com/phuchungbhutia/Move-UserFolders.git
```

Or download the `Move-UserFolders.ps1` file directly.

### ✅ Step 2: Open PowerShell as Administrator

- Press `Start`
- Search for **PowerShell**
- Right-click and choose **Run as Administrator**

### ✅ Step 3: Set Execution Policy (if needed)

If script execution is restricted, run:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope Process
```

### ✅ Step 4: Run the Script

Navigate to the folder where the script is located and run it:

```powershell
cd "C:\Path\To\Move-UserFolders"
.\Move-UserFolders.ps1
```

That’s it! The script will:

- Move your folders from `C:\Users\YourName` to `D:\Users\YourName`
- Update registry entries
- Restart Explorer so the changes take effect

---

## 📁 Folder Paths Affected

| Folder     | Old Path                  | New Path                  |
|------------|---------------------------|---------------------------|
| Desktop    | C:\Users\YourName\Desktop | D:\Users\YourName\Desktop |
| Documents  | C:\Users\YourName\Documents | D:\Users\YourName\Documents |
| Downloads  | C:\Users\YourName\Downloads | D:\Users\YourName\Downloads |
| Music      | C:\Users\YourName\Music   | D:\Users\YourName\Music   |
| Pictures   | C:\Users\YourName\Pictures | D:\Users\YourName\Pictures |
| Videos     | C:\Users\YourName\Videos  | D:\Users\YourName\Videos  |

---

## ⚠️ Warnings

- **Backup your files** before running the script.
- This assumes a `D:` drive is available and accessible.
- For single-user systems only — not tested in enterprise environments.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

Made with ❤️ to help you free up space on your C: drive.
