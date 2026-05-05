# Shader Conversion Tool
 
This is a simple PowerShell script to convert GLSL shaders from how they're written in ShaderToy to regular GLSL shaders. This process can also be done in reverse. I've been working on implementing shaders in Balatro modding, so I have also implemented some conversion tools between that format and the others.

The script can be ran by running this command in the downloaded folder:
```powershell
./shader-conversion-tool.ps1
```
Along with the corresponding flags for your conversion. Please note that -edition is required for any conversion that involves Balatro.

|flag|function|
|--|--|
| source | defines source file|
| output | defines output file |
| edition | defines Balatro edition name |
| GtS | GLSL to Shadertoy |
| StG | Shadertoy to GLSL |
| BtG | Balatro to GLSL |
| BtS | Balatro to ShaderToy |

# Examples
## GLSL to ShaderToy
To convert from GLSL to ShaderToy, open Windows Powershell in this directory and run the command
```powershell
./shader-conversion-tool.ps1 -source test.glsl -output test.txt -StG
```
This will convert the GLSL code in "test.glsl" into ShaderToy code that will be outputted to "test.txt".

## ShaderToy to GLSL
Open Windows Powershell in this directory and run the command
```powershell
./shader-conversion-tool.ps1 -source test.txt -output test.glsl -GtS
```
This will convert the ShaderToy code in "test.txt" into GLSL code that will be outputted to "test.glsl".

## Balatro to GLSL
To convert from Balatro to GLSL, open Windows Powershell in this directory and run the command
```powershell
./shader-conversion-tool.ps1 -source test.txt -output test.glsl -BtG -edition [insert edition name]
```
This will convert the Balatro code in "test.txt" into GLSL code that will be outputted to "test.glsl". For the Balatro code, please use the main function of your shader and any functions used within it. Edition should be the name used for the edition variable, such as foil.

## Balatro to Shadertoy
To convert from Balatro to ShaderToy, open Windows Powershell in this directory and run the command
```powershell
./shader-conversion-tool.ps1 -source test.glsl -output test.txt -BtS -edition [insert edition name]
```
This will convert the Balatro code in "test.glsl" into ShaderToy code that will be outputted to "test.txt". For the Balatro code, please use the main function of your shader and any functions used within it. Edition should be the name used for the edition variable, such as foil.

## GLSL to Balatro
To convert from GLSL to Balatro, open Windows Powershell in this directory and run the command
```powershell
./shader-conversion-tool.ps1 -source test.glsl -output test.txt -GtB -edition [insert edition name]
```
This will convert the GLSL code in "test.glsl" into Balatro code that will be outputted to "test.txt". Edition should be the name used for the edition variable, such as foil.