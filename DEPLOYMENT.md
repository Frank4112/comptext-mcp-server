# 🚀 Render.com Deployment Anleitung

## ✅ Repository ist bereit!

Alle erforderlichen Dateien sind bereits im Repository:
- ✅ `requirements.txt` - Python Dependencies
- ✅ `mcp_server.py` - MCP Server Implementation
- ✅ `render.yaml` - Render Deployment Config

## 📋 Deployment Schritte

### Option A: Blueprint Deploy (Empfohlen)

1. **Gehe zu Render.com**
   - Öffne: https://render.com/deploy

2. **Repository verbinden**
   - Repository: `ProfRandom92/comptext-mcp-server`
   - Render erkennt automatisch `render.yaml`

3. **Deploy starten**
   - Klicke auf "Apply"
   - Warte ~2-3 Minuten
   - ✅ Fertig!

### Option B: Manuelles Setup

1. **Account erstellen**
   - Gehe zu https://render.com
   - Erstelle einen Account (falls noch nicht vorhanden)

2. **Neuen Web Service erstellen**
   - Dashboard → "New" → "Web Service"
   - Repository verbinden: `comptext-mcp-server`

3. **Einstellungen konfigurieren**
   ```
   Name: comptext-mcp
   Environment: Python 3
   Region: Frankfurt (EU)
   Plan: Free
   Build Command: pip install -r requirements.txt
   Start Command: python mcp_server.py
   ```

4. **Umgebungsvariablen**
   ```
   PORT = 10000
   PYTHON_VERSION = 3.11.0
   ```

5. **Deploy starten**
   - Klicke "Create Web Service"
   - Warte auf den Build (~2-3 Min)

## 🌐 Nach dem Deployment

Du erhältst eine URL wie:
```
https://comptext-mcp-XXXXX.onrender.com
```

### Testen der Endpoints

```bash
# Health Check
curl https://YOUR-URL.onrender.com/health

# Server Status
curl https://YOUR-URL.onrender.com/
```

## 🔧 MCP Client Konfiguration

Trage in deinem MCP Client ein:

| Feld | Wert |
|------|------|
| **Name** | CompText MCP Server |
| **URL** | `https://comptext-mcp-XXXXX.onrender.com` |
| **Auth** | None |

## ⚡ Performance Hinweise

**Free Tier Cold Start:**
- Der Server schläft nach 15 Min Inaktivität
- Erste Anfrage nach Pause: ~30 Sekunden
- Nachfolgende Anfragen: schnell

**Lösung:**
- Upgrade auf Paid Plan ($7/Monat)
- Oder: Keep-Alive Cron Job einrichten

## 🔐 Optional: Authentication hinzufügen

Falls du API-Key Authentication möchtest:

1. In Render Dashboard:
   - Settings → Environment → Add
   - Key: `MCP_API_KEY`
   - Value: `dein-sicherer-token`

2. Im MCP Client:
   - Auth Type: Bearer Token
   - Token: `dein-sicherer-token`

## 📊 Monitoring

**Live Logs anzeigen:**
- Render Dashboard → Logs → Tail

**Fehlersuche:**
```bash
# Events anzeigen
curl https://YOUR-URL.onrender.com/

# Health Check
curl https://YOUR-URL.onrender.com/health
```

## 🎯 Next Steps

- [ ] Auf Render.com deployen
- [ ] URL testen
- [ ] In MCP Client eintragen
- [ ] Ersten Test durchführen

## 📚 Weitere Ressourcen

- [Render.com Dokumentation](https://render.com/docs)
- [MCP Protocol Specs](https://modelcontextprotocol.io)
- [Repository](https://github.com/ProfRandom92/comptext-mcp-server)

## ❓ Hilfe benötigt?

Bei Problemen:
1. Prüfe die Render Logs
2. Teste die Health Endpoint
3. Erstelle ein GitHub Issue

---

**Viel Erfolg mit deinem CompText MCP Server! 🚀**
