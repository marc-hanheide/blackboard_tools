
# Install first:  Install-Module -Name MicrosoftTeams
# TRY THIE FIRST: Connect-MicrosoftTeams

# Parameters
$CSVPath = "students.csv"
$TeamName = "CMP3103/CMP9050 - Autonomous Mobile Robotics"

# Connect to Microsoft Teams
Connect-MicrosoftTeams

# Get the Team ID
$Team = Get-Team -DisplayName $TeamName

$TeamID = $Team.GroupId
Write-Host "Team ID:" $TeamID

# overwrite TeamID (hack if there are multiple with same name)
# $TeamID="b898dfe2-a0a2-48f8-b6ef-95bb5b19bb6e"

if ($TeamID) {
    # Import CSV and add users
    Import-Csv $CSVPath | ForEach-Object {
        try {
            Add-TeamUser -GroupId $TeamID -User $_.Email -Role $_.Role
            Write-Host "Added user: $($_.Email)" -ForegroundColor Green
        }
        catch {
            Write-Host "Failed to add user: $($_.Email)" -ForegroundColor Red
            Write-Host $_.Exception.Message
        }
    }
}
else {
    Write-Host "Team '$TeamName' not found!" -ForegroundColor Red
}

# Disconnect when done
Disconnect-MicrosoftTeams