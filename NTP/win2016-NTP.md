## Crating NTP server for VCF 9.x using Windows 2016 server.

================================
Windows PowerShell
Copyright (C) 2016 Microsoft Corporation. All rights reserved.

# confirm current setting (follows are default settings)
PS C:\Users\Administrator> Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\w32time\TimeProviders\NtpServer" 

InputProvider                    : 0
AllowNonstandardModeCombinations : 1
EventLogFlags                    : 0
ChainEntryTimeout                : 16
ChainMaxEntries                  : 128
ChainMaxHostEntries              : 4
ChainDisable                     : 0
ChainLoggingRate                 : 30
RequireSecureTimeSyncRequests    : 0
DllName                          : C:\Windows\SYSTEM32\w32time.DLL
Enabled                          : 0
PSPath                           : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Serv
                                   ices\w32time\TimeProviders\NtpServer
PSParentPath                     : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Serv
                                   ices\w32time\TimeProviders
PSChildName                      : NtpServer
PSDrive                          : HKLM
PSProvider                       : Microsoft.PowerShell.Core\Registry

# enable NTP Server feature
PS C:\Users\Administrator> Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\w32time\TimeProviders\NtpServer" -Name "Enabled" -Value 1 

# set [AnnounceFlags] to 5
# number means
# 0x00 : Not a time server
# 0x01 : Always time server
# 0x02 : Automatic time server
# 0x04 : Always reliable time server
# 0x08 : Automatic reliable time server
PS C:\Users\Administrator> Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\services\W32Time\Config" -Name "AnnounceFlags" -Value 5 

# restart Windows Time service
PS C:\Users\Administrator> Restart-Service w32Time 

# if Windows Firewall is running, allow NTP port
PS C:\Users\Administrator> New-NetFirewallRule `
-Name "NTP Server Port" `
-DisplayName "NTP Server Port" `
-Description 'Allow NTP Server Port' `
-Profile Any `
-Direction Inbound `
-Action Allow `
-Protocol UDP `
-Program Any `
-LocalAddress Any `
-LocalPort 123 


