# Artifact Relay - Quick Reference Guide

## For Agent/LLM Use

### When User Asks: "Give me the file" or "Show me the image"

Use the enhanced endpoint for best results:

```http
GET /api/artifacts/{chat_id}/{file_path}/enhanced?inline=true
```

**Response Decision Tree:**

```
if response.can_inline and response.inline_base64:
    → Display inline: ![Image](response.inline_base64)
    
elif response.has_public_url:
    → Share cloud URL: "Download: {response.public_url}"
    
else:
    → Share local URL: "Available at: {response.local_url}"
    → Warn: "Note: This link only works on the local network"
```

### Examples

#### Example 1: Small Image (Should Inline)

```bash
GET /api/artifacts/chat123/chart.png/enhanced
```

Response:
```json
{
  "inline_base64": "data:image/png;base64,iVBORw0KG...",
  "method": "inline",
  "can_inline": true
}
```

→ **Action:** Display with markdown: `![Chart](data:image/png;base64,...)`

#### Example 2: Large File (Need Cloud)

```bash
GET /api/artifacts/chat123/report.pdf/enhanced?use_cloud=true
```

Response:
```json
{
  "public_url": "https://transfer.sh/abc123/report.pdf",
  "local_url": "http://10.73.184.61:8000/api/artifacts/chat123/report.pdf",
  "method": "cloud",
  "has_public_url": true
}
```

→ **Action:** Return both URLs with context

#### Example 3: List All Artifacts

```bash
GET /api/artifacts/chat123/list-enhanced?inline=true
```

Response:
```json
{
  "artifacts": [
    {
      "name": "output.png",
      "inline_base64": "data:image/png;base64,...",
      "method": "inline"
    },
    {
      "name": "data.csv", 
      "local_url": "http://10.73.184.61:8000/api/artifacts/chat123/data.csv",
      "method": "local"
    }
  ],
  "count": 2,
  "relay_base_url": "http://10.73.184.61:8000"
}
```

### Response Format

```typescript
interface ArtifactResponse {
  // URLs (at least one will be present)
  local_url: string;          // Always present
  public_url?: string;        // Only if use_cloud=true
  inline_base64?: string;     // Only for small images/text
  
  // Metadata
  method: 'local' | 'cloud' | 'inline' | 'cloud+inline';
  size: number;               // Bytes
  size_human: string;         // "1.2 MB"
  mime_type: string;          // "image/png"
  
  // Capabilities
  can_inline: boolean;        // Can be base64 encoded?
  has_public_url: boolean;    // Cloud URL available?
}
```

### Common Patterns

#### Pattern 1: Display Generated Images

```python
# After generating a chart
response = get("/api/artifacts/{chat_id}/chart.png/enhanced?inline=true")

if response['can_inline']:
    return f"Here's the chart:\n\n![Chart]({response['inline_base64']})"
else:
    return f"Chart generated: {response['local_url']}"
```

#### Pattern 2: Share Files Externally

```python
# When user needs to download from outside network
response = get("/api/artifacts/{chat_id}/report.pdf/enhanced?use_cloud=true")

if response['has_public_url']:
    return f"Download link (expires in 7 days):\n{response['public_url']}"
else:
    return f"File too large for cloud relay. Local access: {response['local_url']}"
```

#### Pattern 3: List Downloadable Artifacts

```python
# Show user what files are available
response = get("/api/artifacts/{chat_id}/list-enhanced")

files = []
for artifact in response['artifacts']:
    if artifact['can_inline'] and artifact['mime_type'].startswith('image/'):
        files.append(f"- 📷 {artifact['name']} (can display inline)")
    else:
        files.append(f"- 📄 {artifact['name']} ({artifact['size_human']})")

return "Available files:\n" + "\n".join(files)
```

## Limitations to Communicate

### Inline Encoding
- ✅ Works for: Images < 500 KB, text files < 500 KB
- ❌ Won't work for: Large files, videos, binaries

### Cloud Relay
- ✅ Works for: Files < 100 MB
- ❌ Won't work for: Files > 100 MB
- ⏰ Expiration: 7 days

### Local URLs
- ✅ Works from: Same network as agent (10.73.184.0/24)
- ❌ Won't work from: External networks without VPN

## Error Handling

```python
try:
    response = get(f"/api/artifacts/{chat_id}/{file}/enhanced")
    # Success - use response
except 404:
    return "File not found. Did you create it in this conversation?"
except 403:
    return "Access denied. Security restriction."
except 500 as e:
    return f"Error accessing file: {e}"
```

## Best Practices

1. **Always try inline first for images**
   ```python
   ?inline=true  # Default, but explicit is better
   ```

2. **Use cloud relay sparingly**
   ```python
   ?use_cloud=true  # Only when user needs external access
   ```

3. **Provide context with URLs**
   ```python
   # Good
   "Here's your chart: ![Chart](...)"
   
   # Better
   "I've generated a pressure vs time chart showing the trend over 24 hours: ![Chart](...)"
   ```

4. **Warn about limitations**
   ```python
   if not response['can_inline'] and not response['has_public_url']:
       return f"File available at {response['local_url']} (local network only)"
   ```

## Testing Commands

```bash
# Test inline encoding
curl "http://10.73.184.61:8000/api/artifacts/test/file.png/enhanced?inline=true" | jq .

# Test cloud relay
curl "http://10.73.184.61:8000/api/artifacts/test/file.pdf/enhanced?use_cloud=true" | jq .

# Test listing
curl "http://10.73.184.61:8000/api/artifacts/test/list-enhanced" | jq .
```

---

**Quick Reminder:**
- Small images → `inline=true` → Display directly
- Large files → `use_cloud=true` → Share download link
- Local network → Use local_url as fallback
