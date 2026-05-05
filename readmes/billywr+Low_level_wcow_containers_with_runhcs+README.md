
# Create a Windows Container (WCOW) Using `runhcs` and `wclayer`

This guide walks you through launching a Windows container manually using `runhcs` and `wclayer`, without Docker or containerd. It uses PowerShell variables and produces clean JSON with properly escaped backslashes.

---

## Prerequisites

You’ll need:

- Windows 10/11 Pro or Windows Server with Containers feature enabled
- PowerShell running as Administrator
- Docker CLI to pull the base image
- Golang should be preinstalled
- `runhcs.exe` and `wclayer.exe` from [Microsoft/hcsshim](https://github.com/microsoft/hcsshim)

---

- Install working versions of wclayer and runhcs

```go
go install github.com/Microsoft/hcsshim/cmd/wclayer@v0.8.9
go install github.com/Microsoft/hcsshim/cmd/runhcs@v0.8.9
```

## Step 1: Pull a Base Image, can pull nanoserver or servercore

```powershell
docker pull mcr.microsoft.com/windows/nanoserver:ltsc2022
docker pull mcr.microsoft.com/windows/servercore:ltsc2022
```

---

## Step 2: Get the Base Layer Path from Image [at this stage you can proceed with nanoserer or use servercore in 2.1]

```powershell
$BaseLayer = (docker image inspect mcr.microsoft.com/windows/nanoserver:ltsc2022 | ConvertFrom-Json)[0].GraphDriver.Data.dir
```

#### 2.1 Getting Baselayer from `servercore base image`, its usually the last layer in the layerchain.json, after this just proceed with step 3
 ```pswh
 $TopLayer = (docker image inspect mcr.microsoft.com/windows/servercore:ltsc2022 | ConvertFrom-Json)[0].GraphDriver.Data.dir
 $BaseLayers = Get-Content "$TopLayer\layerchain.json" | ConvertFrom-Json
 $BaseLayer = @($BaseLayers)[-1]
 ```

---

## Step 3: Create the Writable Scratch Layer

```powershell
$ScratchLayer = "C:\ProgramData\Docker\windowsfilter\myscratch"
New-Item -ItemType Directory -Path $ScratchLayer -Force

wclayer create --layer $BaseLayer $ScratchLayer
```

---

## Step 4: Create the Container Bundle and Config File

```powershell
$BaseLayerEscaped = $BaseLayer -replace '\\', '\\'
$ScratchLayerEscaped = $ScratchLayer -replace '\\', '\\'
$Bundle = "C:\scratch-container"
New-Item -ItemType Directory -Path $Bundle -Force

$Config = @"
{
  "ociVersion": "1.0.2",
  "process": {
    "cwd": "C:\\",
    "args": [
      "C:\\Windows\\System32\\cmd.exe",
      "/c",
      "ping -t 127.0.0.1 > nul"
    ],
    "user": {
      "username": "ContainerUser"
    }
  },
  "windows": {
    "layerFolders": [
      "$BaseLayerEscaped",
      "$ScratchLayerEscaped"
    ]
  }
}
"@

$Config | Out-File -Encoding ASCII -FilePath "$Bundle\config.json"
```

---

## Step 5: Create and Start the Container

```powershell
runhcs create -b $Bundle test-container
runhcs start test-container
```
#### 5.1 To create and start the container simultaneously:
```pwsh
runhcs run -b $Bundle test-container
```

---

## Step 6: Exec into the Container (Optional)

```powershell
runhcs exec test-container powershell.exe
```

---

## Step 7: Stop and Delete the Container

```powershell
runhcs kill test-container
runhcs delete test-container
```

If above commands fail to kill or/and delete use 
```pwsh
runhcs delete test-container --force
```

---

## Notes
- `myscratch` and `test-container` should not be pre-existing
- One scratch layer = one container
- If `wclayer` fails, verify your base layer path
- The ping command keeps the container alive for inspection
- Stop Docker if you see `0x20` errors about files in use
- Sometimes, after deleting a container, you may need to dismount the scratch layer before running it again. Use the following PowerShell command
  ```pwsh
   Dismount-DiskImage -ImagePath "path_to_your_scratch_layer\sandbox.vhdx"
  ```

---

This method gives you full control over how Windows containers are constructed and executed using low-level tools.
