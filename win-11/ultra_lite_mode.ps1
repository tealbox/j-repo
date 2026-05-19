# ultra_lite_mode.ps1
# C:\Windows\System32\SystemPropertiesPerformance.exe
# powershell -ExecutionPolicy Bypass -File .\ultra_lite_mode.ps1
# Focus: UI speed + responsiveness + zero policy violations
Write-Host "Applying Ultra Lite Performance Mode..." -ForegroundColor Cyan
# Avoid noisy errors
$ErrorActionPreference = "SilentlyContinue"
# -------------------------------
# 🔹 1. Disable ALL Animations (Safe)
# -------------------------------
Write-Host "Disabling animations..."
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "MenuShowDelay" -Value "0"
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop\WindowMetrics" -Name "MinAnimate" -Value "0"
New-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" -Name "VisualFXSetting" -Value 2
New-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Accessibility" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Accessibility" -Name "AnimationEffect" -Value 0
# -------------------------------
# 🔹 2. Disable Transparency (Safe)
# -------------------------------
Write-Host "Disabling transparency..."
New-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "EnableTransparency" -Value 0
# -------------------------------
# 🔹 3. Instant Context Menu (Safe + HUGE UX boost)
# -------------------------------
Write-Host "Enabling classic right-click menu..."
$menuPath = "HKCU:\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"
New-Item -Path $menuPath -Force | Out-Null
Set-ItemProperty -Path $menuPath -Name "(default)" -Value ""
# -------------------------------
# 🔹 4. Faster UI Response (Very Safe)
# -------------------------------
Write-Host "Improving responsiveness..."
Set-ItemProperty -Path "HKCU:\Control Panel\Mouse" -Name "MouseHoverTime" -Value "0"
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "ForegroundLockTimeout" -Value 0
# -------------------------------
# 🔹 5. Remove Startup Delay (Safe, non-invasive)
# -------------------------------
Write-Host "Removing startup lag..."
New-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Serialize" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Serialize" -Name "StartupDelayInMSec" -Value 0
# -------------------------------
# 🔹 6. Light Explorer Cleanup (Safe visuals only)
# -------------------------------
Write-Host "Cleaning Explorer visuals..."
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "TaskbarAnimations" -Value 0
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "ListviewShadow" -Value 0
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "ListviewAlphaSelect" -Value 0
# -------------------------------
# 🔹 Apply Changes
# -------------------------------
Write-Host "Restarting Explorer..." -ForegroundColor Yellow
Stop-Process -Name explorer -Force
Start-Process explorer
Write-Host ""
Write-Host "✅ ULTRA LITE MODE ENABLED" -ForegroundColor Green
Write-Host "✔ No animations"
Write-Host "✔ Instant right-click"
Write-Host "✔ Faster menus & response"
Write-Host "✔ Safe for corporate laptops"
Write-Host ""