# Sample Tariff Documents

This folder contains representative examples of tariff documents used in costing analysis.

## Purpose
- Train agents on real PDF structures
- Validate extraction logic
- Document variety of formats encountered

## Examples Included Pipeline Tariffs and Rail Tariffs

## Full Tariff Library

**Local Path:** `C:\Users\jalex\supply-chain\tariff_library\`

Complete collection organized by:
- `pipelines\` - Pipeline operator tariffs
- `railroads\` - Class I railroad rates  
- `terminals\` - Terminal throughput and facilities charges

**Backup:** Regularly copy to external drive or OneDrive

## Using These Examples

When building tariff extraction agents:
1. Test on these sample PDFs first
2. Verify extraction accuracy
3. Handle edge cases
4. Then apply to full library at local path above

## File Organization
```
tariff_library/
├── pipelines/
│   ├── Colonial/
│   │   ├── Colonial_278_2023.pdf
│   │   └── Colonial_278_2024.pdf
│   └── BP_WHD/
├── railroads/
│   └── Union_Pacific/
└── terminals/
    └── Buckeye/
```