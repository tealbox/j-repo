# speedup.ps1
# Right‑click Start -> Terminal -> run
# powershell -ExecutionPolicy Bypass -File .\speedup.ps1
# Disable animations and improve performance (no admin required)
# C:\Windows\System32\SystemPropertiesPerformance.exe
Write-Host "Applying performance tweaks..."
# Ensure registry paths exist
New-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Accessibility" -Force | Out-Null
# Disable menu delay
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "MenuShowDelay" -Value "0"
# Disable window animations
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop\WindowMetrics" -Name "MinAnimate" -Value "0"
# Visual effects: best performance
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" -Name "VisualFXSetting" -Value 2
# Disable taskbar animations
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "TaskbarAnimations" -Value 0
# Disable transparency
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "EnableTransparency" -Value 0
# Disable animations (accessibility)
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Accessibility" -Name "AnimationEffect" -Value 0
Write-Host "Enabling classic right-click menu..."
$path = "HKCU:\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"
# Create required keys
New-Item -Path $path -Force | Out-Null
# Set default value to empty
Set-ItemProperty -Path $path -Name "(default)" -Value "" -Force
# Restart Explorer
Write-Host "Restarting Explorer..."
Stop-Process -Name explorer -Force
Start-Process explorer
Write-Host "Done! Full right-click menu enabled (no 'Show more options')."


# ----------------------------
# Revert (restore default Windows 11 menu)
# Remove-Item -Path "HKCU:\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}" -Recurse -Force
# Stop-Process -Name explorer -Force
# Start-Process explorer
# ----------------------------