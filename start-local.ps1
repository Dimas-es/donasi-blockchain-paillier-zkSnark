# Script PowerShell untuk menjalankan sistem lokal (Tanpa Docker)
Write-Host "=== TrustGive - Local Setup Runner (Windows PowerShell) ===" -ForegroundColor Cyan

# 1. Cek PostgreSQL Service
$pgService = Get-Service -Name "postgresql-x64-18" -ErrorAction SilentlyContinue
if ($pgService -and $pgService.Status -ne "Running") {
    Write-Host "Menjalankan PostgreSQL service..." -ForegroundColor Yellow
    Start-Service "postgresql-x64-18"
}

Write-Host "`nUntuk menjalankan sistem lokal, buka 3 tab / terminal PowerShell:`n" -ForegroundColor Green

Write-Host "Terminal 1 (Blockchain Hardhat):" -ForegroundColor Yellow
Write-Host "cd blockchain"
Write-Host "npx hardhat node`n"

Write-Host "Terminal 2 (Backend Go API):" -ForegroundColor Yellow
Write-Host "cd backend"
Write-Host "go run ./cmd/server`n"

Write-Host "Terminal 3 (Frontend React):" -ForegroundColor Yellow
Write-Host "cd frontend"
Write-Host "npm run dev`n"

Write-Host "Akses Web UI di: http://localhost:5173" -ForegroundColor Cyan
Write-Host "Akun Demo Sidang:" -ForegroundColor Cyan
Write-Host " - Pengelola: pengelola@demo.local (password: demo12345)"
Write-Host " - Donatur:   donatur@demo.local   (password: demo12345)"
Write-Host " - Admin:     admin@demo.local     (password: demo12345)"
