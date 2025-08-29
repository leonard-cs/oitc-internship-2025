# 🛠️ SQL Server Setup Guide

## Table of Contents
- [SQL Authentication](#enable-sql-authentication--create-a-login)
- [SQL Server Network Port](#configure-sql-server-network-port)
- [Windows Defender Firewall](#allow-sql-server-port-in-windows-defender-firewall)

## Enable SQL Authentication & Create a Login
1. In SSMS → right-click the server → Properties → Security:
    - Select SQL Server and Windows Authentication mode → OK.
    - Restart SQL Server service (via SQL Server Configuration Manager or services.msc).

2. Create a SQL Auth login:
    ```sql
    CREATE LOGIN northwind_user 
    WITH PASSWORD = 'StrongPassword123!';
    GO

    USE Northwind;
    CREATE USER northwind_user FOR LOGIN northwind_user;
    EXEC sp_addrolemember 'db_owner', 'northwind_user';
    GO
    ```
    ✅ Now northwind_user can log in with SQL authentication.

## Configure SQL Server Network Port
1. Open SQL Server Configuration Manager.

2. Navigate to:
    - SQL Server Network Configuration → Protocols for MSSQLSERVER.
    - Enable TCP/IP (right-click → Enable).

3. Right-click TCP/IP → Properties:
    - Go to the IP Addresses tab.
    - Scroll down to IPAll:
        - Set TCP Port = 1433 (default SQL port).
        - Clear TCP Dynamic Ports (leave blank).
    - Click OK.

4. Restart SQL Server service.

## Allow SQL Server Port in Windows Defender Firewall
1. Open Windows Defender Firewall with Advanced Security.

2. Go to Inbound Rules → New Rule.
    - Rule Type: Port.
    - Protocol: TCP, Specific local ports: 1433.
    - Action: Allow the connection.
    - Profile: Domain, Private, Public (choose what applies).
    - Name: SQL Server 1433.

3. Click Finish.

## Reference
- [Setup SQL Server Auth (Chinese)](https://ithelp.ithome.com.tw/articles/10214386)
- [Window Defender Firewall for SQL Server (Chinese)](https://i-freelancer.net/WebHelp/Qboss/ACC40_WebHelp/SQLServerAw1.html)
- [Error: Adapve Server is unavalible (Chinese)](https://blog.csdn.net/vbwhere/article/details/103690794)
