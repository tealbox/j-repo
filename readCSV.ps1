# Define the root directory
$rootDir = "C:\Path\To\Root\Directory"

# Get all CSV files in the root directory and its subdirectories
$csvFiles = Get-ChildItem -Path $rootDir -Filter *.csv -Recurse

# Loop through each CSV file
foreach ($file in $csvFiles) {
    # Print the file path
    Write-Host "Processing file: $($file.FullName)"

    # Import the CSV file and print its contents
    Import-Csv -Path $file.FullName | Format-Table -AutoSize
}
