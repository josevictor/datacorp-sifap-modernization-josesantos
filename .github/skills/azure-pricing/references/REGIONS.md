# Referência de nomes de regiões do Azure

A API Azure Retail Prices exige valores de `armRegionName` em minúsculas e sem espaços. Use esta tabela para associar nomes comuns de regiões aos valores da API.

## Mapeamento de regiões

| Nome para exibição | armRegionName |
|-------------|---------------|
| East US | `eastus` |
| East US 2 | `eastus2` |
| Central US | `centralus` |
| North Central US | `northcentralus` |
| South Central US | `southcentralus` |
| West Central US | `westcentralus` |
| West US | `westus` |
| West US 2 | `westus2` |
| West US 3 | `westus3` |
| Canada Central | `canadacentral` |
| Canada East | `canadaeast` |
| Brazil South | `brazilsouth` |
| North Europe | `northeurope` |
| West Europe | `westeurope` |
| UK South | `uksouth` |
| UK West | `ukwest` |
| France Central | `francecentral` |
| France South | `francesouth` |
| Germany West Central | `germanywestcentral` |
| Germany North | `germanynorth` |
| Switzerland North | `switzerlandnorth` |
| Switzerland West | `switzerlandwest` |
| Norway East | `norwayeast` |
| Norway West | `norwaywest` |
| Sweden Central | `swedencentral` |
| Italy North | `italynorth` |
| Poland Central | `polandcentral` |
| Spain Central | `spaincentral` |
| East Asia | `eastasia` |
| Southeast Asia | `southeastasia` |
| Japan East | `japaneast` |
| Japan West | `japanwest` |
| Australia East | `australiaeast` |
| Australia Southeast | `australiasoutheast` |
| Australia Central | `australiacentral` |
| Korea Central | `koreacentral` |
| Korea South | `koreasouth` |
| Central India | `centralindia` |
| South India | `southindia` |
| West India | `westindia` |
| UAE North | `uaenorth` |
| UAE Central | `uaecentral` |
| South Africa North | `southafricanorth` |
| South Africa West | `southafricawest` |
| Qatar Central | `qatarcentral` |

## Regras de conversão

1. Remova todos os espaços.
2. Converta para minúsculas.
3. Exemplos:
   - "East US" → `eastus`
   - "West Europe" → `westeurope`
   - "Southeast Asia" → `southeastasia`
   - "South Central US" → `southcentralus`

## Aliases comuns

As pessoas podem se referir às regiões de modo informal. Associe esses nomes ao `armRegionName` correto:

| A pessoa diz | Mapear para |
|-----------|---------|
| "US East", "Virginia" | `eastus` |
| "US West", "California" | `westus` |
| "Europe", "EU" | `westeurope` (padrão) |
| "UK", "London" | `uksouth` |
| "Asia", "Singapore" | `southeastasia` |
| "Japan", "Tokyo" | `japaneast` |
| "Australia", "Sydney" | `australiaeast` |
| "India", "Mumbai" | `centralindia` |
| "Korea", "Seoul" | `koreacentral` |
| "Brazil", "São Paulo" | `brazilsouth` |
| "Canada", "Toronto" | `canadacentral` |
| "Germany", "Frankfurt" | `germanywestcentral` |
| "France", "Paris" | `francecentral` |
| "Sweden", "Stockholm" | `swedencentral` |
