#!/usr/bin/env python3
"""
Gerador de diagramas interativos de arquitetura do Azure v3.
Gera diagramas HTML interativos com ícones oficiais do Azure (Base64 embutido).
"""

import json
from datetime import datetime

from icons import get_icon_data_uri

_HAS_OFFICIAL_ICONS = True
# Ícones de serviços do Azure: SVG, cores e mapeamento da chave do ícone oficial
# icon: caminho SVG com viewBox 48x48 (alternativa)
# azure_icon_key: chave em icons.py (ícone oficial do Azure)
SERVICE_ICONS = {
    "openai": {
        "icon_svg": '<circle cx="24" cy="24" r="18" fill="#0078D4"/><text x="24" y="30" text-anchor="middle" font-size="18" fill="white" font-weight="700">AI</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "AI",
        "azure_icon_key": "azure_openai"
    },
    "ai_foundry": {
        "icon_svg": '<rect x="6" y="10" width="36" height="28" rx="4" fill="#0078D4"/><rect x="12" y="16" width="10" height="8" rx="2" fill="white" opacity="0.9"/><rect x="26" y="16" width="10" height="8" rx="2" fill="white" opacity="0.9"/><rect x="12" y="27" width="24" height="5" rx="2" fill="white" opacity="0.6"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "AI",
        "azure_icon_key": "ai_foundry"
    },
    "ai_hub": {
        "icon_svg": '<rect x="6" y="10" width="36" height="28" rx="4" fill="#0078D4"/><circle cx="24" cy="24" r="8" fill="white" opacity="0.9"/><circle cx="24" cy="24" r="4" fill="#0078D4"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "AI",
        "azure_icon_key": "machine_learning"
    },
    "search": {
        "icon_svg": '<circle cx="20" cy="20" r="12" fill="none" stroke="#0078D4" stroke-width="3.5"/><line x1="29" y1="29" x2="40" y2="40" stroke="#0078D4" stroke-width="3.5" stroke-linecap="round"/><circle cx="20" cy="20" r="5" fill="#0078D4" opacity="0.3"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "AI",
        "azure_icon_key": "cognitive_search"
    },
    "ai_search": {
        "icon_svg": '<circle cx="20" cy="20" r="12" fill="none" stroke="#0078D4" stroke-width="3.5"/><line x1="29" y1="29" x2="40" y2="40" stroke="#0078D4" stroke-width="3.5" stroke-linecap="round"/><circle cx="20" cy="20" r="5" fill="#0078D4" opacity="0.3"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "AI",
        "azure_icon_key": "cognitive_search"
    },
    "aml": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><path d="M14 32 L20 18 L26 26 L32 14" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "AI",
        "azure_icon_key": "machine_learning"
    },
    "storage": {
        "icon_svg": '<rect x="8" y="8" width="32" height="8" rx="3" fill="#0078D4"/><rect x="8" y="20" width="32" height="8" rx="3" fill="#0078D4" opacity="0.7"/><rect x="8" y="32" width="32" height="8" rx="3" fill="#0078D4" opacity="0.4"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "storage_accounts"
    },
    "adls": {
        "icon_svg": '<rect x="8" y="8" width="32" height="8" rx="3" fill="#0078D4"/><rect x="8" y="20" width="32" height="8" rx="3" fill="#0078D4" opacity="0.7"/><rect x="8" y="32" width="32" height="8" rx="3" fill="#0078D4" opacity="0.4"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "data_lake_storage_gen1"
    },
    "fabric": {
        "icon_svg": '<polygon points="24,6 42,18 42,34 24,46 6,34 6,18" fill="#E8740C" opacity="0.9"/><text x="24" y="30" text-anchor="middle" font-size="14" fill="white" font-weight="700">F</text>',
        "color": "#E8740C", "bg": "#FEF3E8", "category": "Data",
        "azure_icon_key": "microsoft_fabric"
    },
    "synapse": {
        "icon_svg": '<circle cx="24" cy="24" r="18" fill="#0078D4"/><path d="M15 24 L24 15 L33 24 L24 33 Z" fill="white" opacity="0.9"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "azure_synapse_analytics"
    },
    "adf": {
        "icon_svg": '<rect x="6" y="12" width="36" height="24" rx="4" fill="#0078D4"/><path d="M16 24 L28 24 M24 18 L30 24 L24 30" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "data_factory"
    },
    "data_factory": {
        "icon_svg": '<rect x="6" y="12" width="36" height="24" rx="4" fill="#0078D4"/><path d="M16 24 L28 24 M24 18 L30 24 L24 30" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "data_factory"
    },
    "keyvault": {
        "icon_svg": '<rect x="10" y="6" width="28" height="36" rx="4" fill="#E8A000"/><circle cx="24" cy="22" r="6" fill="white"/><rect x="22" y="26" width="4" height="10" rx="1" fill="white"/>',
        "color": "#E8A000", "bg": "#FEF7E0", "category": "Security",
        "azure_icon_key": "key_vaults"
    },
    "kv": {
        "icon_svg": '<rect x="10" y="6" width="28" height="36" rx="4" fill="#E8A000"/><circle cx="24" cy="22" r="6" fill="white"/><rect x="22" y="26" width="4" height="10" rx="1" fill="white"/>',
        "color": "#E8A000", "bg": "#FEF7E0", "category": "Security",
        "azure_icon_key": "key_vaults"
    },
    "vnet": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="none" stroke="#5C2D91" stroke-width="2.5"/><circle cx="16" cy="18" r="4" fill="#5C2D91"/><circle cx="32" cy="18" r="4" fill="#5C2D91"/><circle cx="24" cy="32" r="4" fill="#5C2D91"/><line x1="16" y1="18" x2="32" y2="18" stroke="#5C2D91" stroke-width="1.5"/><line x1="16" y1="18" x2="24" y2="32" stroke="#5C2D91" stroke-width="1.5"/><line x1="32" y1="18" x2="24" y2="32" stroke="#5C2D91" stroke-width="1.5"/>',
        "color": "#5C2D91", "bg": "#F3EEF9", "category": "Network",
        "azure_icon_key": "virtual_networks"
    },
    "pe": {
        "icon_svg": '<circle cx="24" cy="24" r="14" fill="none" stroke="#5C2D91" stroke-width="2"/><circle cx="24" cy="24" r="6" fill="#5C2D91"/><line x1="24" y1="10" x2="24" y2="4" stroke="#5C2D91" stroke-width="2"/><line x1="24" y1="38" x2="24" y2="44" stroke="#5C2D91" stroke-width="2"/>',
        "color": "#5C2D91", "bg": "#F3EEF9", "category": "Network",
        "azure_icon_key": "private_endpoints"
    },
    "nsg": {
        "icon_svg": '<rect x="8" y="8" width="32" height="32" rx="4" fill="#5C2D91"/><path d="M18 20 L24 14 L30 20 M18 28 L24 34 L30 28" stroke="white" stroke-width="2" fill="none"/>',
        "color": "#5C2D91", "bg": "#F3EEF9", "category": "Network",
        "azure_icon_key": "network_security_groups"
    },
    "acr": {
        "icon_svg": '<rect x="8" y="10" width="32" height="28" rx="4" fill="#0078D4"/><rect x="14" y="16" width="20" height="16" rx="2" fill="white" opacity="0.3"/><text x="24" y="30" text-anchor="middle" font-size="12" fill="white" font-weight="600">ACR</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Compute"
    },
    "aks": {
        "icon_svg": '<circle cx="24" cy="24" r="18" fill="#326CE5"/><text x="24" y="30" text-anchor="middle" font-size="16" fill="white" font-weight="700">K</text>',
        "color": "#326CE5", "bg": "#EBF0FC", "category": "Compute",
        "azure_icon_key": "kubernetes_services"
    },
    "appservice": {
        "icon_svg": '<rect x="8" y="8" width="32" height="32" rx="6" fill="#0078D4"/><polygon points="24,14 34,34 14,34" fill="white" opacity="0.9"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Compute",
        "azure_icon_key": "app_services"
    },
    "appinsights": {
        "icon_svg": '<circle cx="24" cy="24" r="16" fill="#773ADC"/><path d="M16 28 L20 20 L24 24 L28 16 L32 22" stroke="white" stroke-width="2" fill="none" stroke-linecap="round"/>',
        "color": "#773ADC", "bg": "#F0EAFA", "category": "Monitor",
        "azure_icon_key": "application_insights"
    },
    "monitor": {
        "icon_svg": '<rect x="6" y="10" width="36" height="24" rx="4" fill="#773ADC"/><path d="M14 28 L20 20 L26 24 L34 16" stroke="white" stroke-width="2" fill="none" stroke-linecap="round"/><rect x="14" y="36" width="20" height="3" rx="1" fill="#773ADC" opacity="0.5"/>',
        "color": "#773ADC", "bg": "#F0EAFA", "category": "Monitor",
        "azure_icon_key": "monitor"
    },
    "vm": {
        "icon_svg": '<rect x="6" y="8" width="36" height="26" rx="3" fill="#0078D4"/><rect x="10" y="12" width="28" height="18" rx="1" fill="white" opacity="0.2"/><rect x="16" y="36" width="16" height="4" rx="1" fill="#0078D4"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Compute",
        "azure_icon_key": "virtual_machine"
    },
    "bastion": {
        "icon_svg": '<rect x="8" y="6" width="32" height="36" rx="4" fill="#5C2D91"/><rect x="14" y="12" width="20" height="14" rx="2" fill="white" opacity="0.3"/><circle cx="24" cy="34" r="4" fill="white" opacity="0.7"/>',
        "color": "#5C2D91", "bg": "#F3EEF9", "category": "Network",
        "azure_icon_key": "bastions"
    },
    "jumpbox": {
        "icon_svg": '<rect x="8" y="8" width="32" height="32" rx="4" fill="#5C2D91"/><text x="24" y="30" text-anchor="middle" font-size="14" fill="white" font-weight="600">JB</text>',
        "color": "#5C2D91", "bg": "#F3EEF9", "category": "Network",
        "azure_icon_key": "virtual_machine"
    },
    "vpn": {
        "icon_svg": '<rect x="6" y="12" width="36" height="24" rx="4" fill="#5C2D91"/><path d="M16 24 L24 16 L32 24 L24 32 Z" fill="white" opacity="0.8"/>',
        "color": "#5C2D91", "bg": "#F3EEF9", "category": "Network",
        "azure_icon_key": "virtual_network_gateways"
    },
    "user": {
        "icon_svg": '<circle cx="24" cy="16" r="8" fill="#0078D4"/><path d="M10 42 Q10 30 24 30 Q38 30 38 42" fill="#0078D4"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "External"
    },
    "app": {
        "icon_svg": '<rect x="8" y="6" width="32" height="36" rx="6" fill="#666"/><rect x="14" y="12" width="20" height="20" rx="2" fill="white" opacity="0.3"/><circle cx="24" cy="40" r="2" fill="white" opacity="0.7"/>',
        "color": "#666666", "bg": "#F5F5F5", "category": "External"
    },
    "default": {
        "icon_svg": '<circle cx="24" cy="24" r="16" fill="#0078D4"/><text x="24" y="30" text-anchor="middle" font-size="14" fill="white" font-weight="600">?</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Azure"
    },
    "cdn": {
        "icon_svg": '<circle cx="24" cy="24" r="18" fill="#0078D4"/><text x="24" y="28" text-anchor="middle" font-size="10" fill="white" font-weight="700">CDN</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Network",
        "azure_icon_key": "cdn_profiles"
    },
    "event_hub": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#0078D4"/><text x="24" y="22" text-anchor="middle" font-size="8" fill="white" font-weight="700">Event</text><text x="24" y="33" text-anchor="middle" font-size="8" fill="white">Hub</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Integration",
        "azure_icon_key": "event_hubs"
    },
    "redis": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#D83B01"/><text x="24" y="28" text-anchor="middle" font-size="10" fill="white" font-weight="700">Redis</text>',
        "color": "#D83B01", "bg": "#FEF0E8", "category": "Data",
        "azure_icon_key": "cache_redis"
    },
    "devops": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#0078D4"/><text x="24" y="22" text-anchor="middle" font-size="8" fill="white" font-weight="700">Dev</text><text x="24" y="33" text-anchor="middle" font-size="8" fill="white">Ops</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "DevOps",
        "azure_icon_key": "azure_devops"
    },
    "acr": {
        "icon_svg": '<rect x="8" y="10" width="32" height="28" rx="4" fill="#0078D4"/><text x="24" y="28" text-anchor="middle" font-size="10" fill="white" font-weight="700">ACR</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Compute",
        "azure_icon_key": "container_registries"
    },
    "container_registry": {
        "icon_svg": '<rect x="8" y="10" width="32" height="28" rx="4" fill="#0078D4"/><text x="24" y="28" text-anchor="middle" font-size="10" fill="white" font-weight="700">ACR</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Compute",
        "azure_icon_key": "container_registries"
    },
    "app_gateway": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#0078D4"/><text x="24" y="22" text-anchor="middle" font-size="8" fill="white" font-weight="700">App</text><text x="24" y="33" text-anchor="middle" font-size="8" fill="white">GW</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Network",
        "azure_icon_key": "application_gateways"
    },
    "iot_hub": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#0078D4"/><text x="24" y="22" text-anchor="middle" font-size="8" fill="white" font-weight="700">IoT</text><text x="24" y="33" text-anchor="middle" font-size="8" fill="white">Hub</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "IoT",
        "azure_icon_key": "iot_hub"
    },
    "stream_analytics": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#0078D4"/><text x="24" y="22" text-anchor="middle" font-size="7" fill="white" font-weight="700">Stream</text><text x="24" y="33" text-anchor="middle" font-size="7" fill="white">Analytics</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "stream_analytics_jobs"
    },
    "vpn_gateway": {
        "icon_svg": '<rect x="6" y="12" width="36" height="24" rx="4" fill="#5C2D91"/><path d="M16 24 L24 16 L32 24 L24 32 Z" fill="white" opacity="0.8"/>',
        "color": "#5C2D91", "bg": "#F3EEF9", "category": "Network",
        "azure_icon_key": "virtual_network_gateways"
    },
    "front_door": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#0078D4"/><text x="24" y="22" text-anchor="middle" font-size="7" fill="white" font-weight="700">Front</text><text x="24" y="33" text-anchor="middle" font-size="7" fill="white">Door</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Network",
        "azure_icon_key": "front_door_and_cdn_profiles"
    },
    "ai_hub": {
        "icon_svg": '<rect x="6" y="10" width="36" height="28" rx="4" fill="#0078D4"/><circle cx="24" cy="24" r="8" fill="white" opacity="0.9"/><circle cx="24" cy="24" r="4" fill="#0078D4"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "AI",
        "azure_icon_key": "ai_studio"
    },
    "firewall": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#E8A000"/><text x="24" y="22" text-anchor="middle" font-size="7" fill="white" font-weight="700">Fire</text><text x="24" y="33" text-anchor="middle" font-size="7" fill="white">wall</text>',
        "color": "#E8A000", "bg": "#FFF8E1", "category": "Network",
        "azure_icon_key": "firewalls"
    },
    "document_intelligence": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#0078D4"/><text x="24" y="22" text-anchor="middle" font-size="9" fill="white" font-weight="700">Doc</text><text x="24" y="33" text-anchor="middle" font-size="9" fill="white">Intel</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "AI",
        "azure_icon_key": "form_recognizer"
    },
    "form_recognizer": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#0078D4"/><text x="24" y="22" text-anchor="middle" font-size="9" fill="white" font-weight="700">Doc</text><text x="24" y="33" text-anchor="middle" font-size="9" fill="white">Intel</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "AI",
        "azure_icon_key": "form_recognizer"
    },
    "databricks": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="6" fill="#FF3621"/><text x="24" y="30" text-anchor="middle" font-size="16" fill="white" font-weight="700">DB</text>',
        "color": "#FF3621", "bg": "#FFF0EE", "category": "Data",
        "azure_icon_key": "azure_databricks"
    },
    "sql_server": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#0078D4"/><text x="24" y="22" text-anchor="middle" font-size="11" fill="white" font-weight="700">SQL</text><rect x="12" y="28" width="24" height="8" rx="2" fill="white" opacity="0.3"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "sql_server"
    },
    "sql_database": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#0078D4"/><text x="24" y="22" text-anchor="middle" font-size="11" fill="white" font-weight="700">SQL</text><rect x="12" y="28" width="24" height="8" rx="2" fill="white" opacity="0.3"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "sql_database"
    },
    "cosmos_db": {
        "icon_svg": '<circle cx="24" cy="24" r="18" fill="#0078D4"/><text x="24" y="22" text-anchor="middle" font-size="9" fill="white" font-weight="700">Cosmos</text><text x="24" y="33" text-anchor="middle" font-size="9" fill="white">DB</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "azure_cosmos_db"
    },
    "app_service": {
        "icon_svg": '<rect x="6" y="10" width="36" height="28" rx="6" fill="#0078D4"/><text x="24" y="28" text-anchor="middle" font-size="11" fill="white" font-weight="700">App</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Compute",
        "azure_icon_key": "app_services"
    },
    "aks": {
        "icon_svg": '<polygon points="24,4 44,20 38,44 10,44 4,20" fill="#326CE5" stroke="#fff" stroke-width="1"/><text x="24" y="30" text-anchor="middle" font-size="11" fill="white" font-weight="700">K8s</text>',
        "color": "#326CE5", "bg": "#EBF0FA", "category": "Compute",
        "azure_icon_key": "kubernetes_services"
    },
    "function_app": {
        "icon_svg": '<polygon points="24,6 42,42 6,42" fill="#F0AD4E"/><text x="24" y="36" text-anchor="middle" font-size="14" fill="white" font-weight="700">ƒ</text>',
        "color": "#F0AD4E", "bg": "#FFF8ED", "category": "Compute",
        "azure_icon_key": "function_apps"
    },
    "synapse": {
        "icon_svg": '<circle cx="24" cy="24" r="18" fill="#0078D4"/><text x="24" y="22" text-anchor="middle" font-size="8" fill="white" font-weight="700">Syn</text><text x="24" y="32" text-anchor="middle" font-size="8" fill="white">apse</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "azure_synapse_analytics"
    },
    "log_analytics": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#5C2D91"/><text x="24" y="28" text-anchor="middle" font-size="10" fill="white" font-weight="700">Log</text>',
        "color": "#5C2D91", "bg": "#F3EDF7", "category": "Monitoring",
        "azure_icon_key": "log_analytics_workspaces"
    },
    "app_insights": {
        "icon_svg": '<circle cx="24" cy="24" r="18" fill="#5C2D91"/><text x="24" y="28" text-anchor="middle" font-size="10" fill="white" font-weight="700">AI</text>',
        "color": "#5C2D91", "bg": "#F3EDF7", "category": "Monitoring",
        "azure_icon_key": "application_insights"
    },
    "nsg": {
        "icon_svg": '<rect x="6" y="6" width="36" height="36" rx="4" fill="#E8A000"/><text x="24" y="28" text-anchor="middle" font-size="10" fill="white" font-weight="700">NSG</text>',
        "color": "#E8A000", "bg": "#FFF8E1", "category": "Network",
        "azure_icon_key": "network_security_groups"
    },
    "apim": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><path d="M16 20 L32 20 M16 28 L32 28 M24 14 L24 34" stroke="white" stroke-width="2" fill="none" stroke-linecap="round"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Integration",
        "azure_icon_key": "api_management_services"
    },
    "api_management": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><path d="M16 20 L32 20 M16 28 L32 28 M24 14 L24 34" stroke="white" stroke-width="2" fill="none" stroke-linecap="round"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Integration",
        "azure_icon_key": "api_management_services"
    },
    "service_bus": {
        "icon_svg": '<rect x="6" y="10" width="36" height="28" rx="4" fill="#0078D4"/><path d="M14 24 L22 24 M26 24 L34 24" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round"/><circle cx="24" cy="24" r="4" fill="white"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Integration",
        "azure_icon_key": "azure_service_bus"
    },
    "logic_apps": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><path d="M14 18 L24 28 L34 18" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Integration",
        "azure_icon_key": "logic_apps"
    },
    "logic_app": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><path d="M14 18 L24 28 L34 18" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Integration",
        "azure_icon_key": "logic_apps"
    },
    "event_grid": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><circle cx="16" cy="18" r="3" fill="white"/><circle cx="32" cy="18" r="3" fill="white"/><circle cx="16" cy="30" r="3" fill="white"/><circle cx="32" cy="30" r="3" fill="white"/><line x1="16" y1="18" x2="32" y2="30" stroke="white" stroke-width="1.5"/><line x1="32" y1="18" x2="16" y2="30" stroke="white" stroke-width="1.5"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Integration",
        "azure_icon_key": "event_grid_topics"
    },
    "container_apps": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><rect x="12" y="14" width="10" height="10" rx="2" fill="white" opacity="0.9"/><rect x="26" y="14" width="10" height="10" rx="2" fill="white" opacity="0.9"/><rect x="12" y="28" width="24" height="6" rx="2" fill="white" opacity="0.6"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Compute",
        "azure_icon_key": "container_apps_environments"
    },
    "container_app": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><rect x="12" y="14" width="10" height="10" rx="2" fill="white" opacity="0.9"/><rect x="26" y="14" width="10" height="10" rx="2" fill="white" opacity="0.9"/><rect x="12" y="28" width="24" height="6" rx="2" fill="white" opacity="0.6"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Compute",
        "azure_icon_key": "container_apps_environments"
    },
    "postgresql": {
        "icon_svg": '<rect x="8" y="8" width="32" height="32" rx="4" fill="#0078D4"/><text x="24" y="28" text-anchor="middle" font-size="10" fill="white" font-weight="700">PG</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "azure_database_postgresql_server"
    },
    "mysql": {
        "icon_svg": '<rect x="8" y="8" width="32" height="32" rx="4" fill="#0078D4"/><text x="24" y="28" text-anchor="middle" font-size="10" fill="white" font-weight="700">My</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "azure_database_mysql_server"
    },
    "load_balancer": {
        "icon_svg": '<circle cx="24" cy="24" r="18" fill="#5C2D91"/><path d="M16 18 L32 18 M16 24 L32 24 M16 30 L32 30" stroke="white" stroke-width="2" fill="none" stroke-linecap="round"/>',
        "color": "#5C2D91", "bg": "#F3EEF9", "category": "Network",
        "azure_icon_key": "load_balancers"
    },
    "nat_gateway": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#5C2D91"/><text x="24" y="28" text-anchor="middle" font-size="10" fill="white" font-weight="700">NAT</text>',
        "color": "#5C2D91", "bg": "#F3EEF9", "category": "Network",
        "azure_icon_key": "nat"
    },
    "expressroute": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#5C2D91"/><path d="M14 24 L34 24" stroke="white" stroke-width="3" fill="none" stroke-linecap="round"/><circle cx="14" cy="24" r="4" fill="white"/><circle cx="34" cy="24" r="4" fill="white"/>',
        "color": "#5C2D91", "bg": "#F3EEF9", "category": "Network",
        "azure_icon_key": "expressroute_circuits"
    },
    "sentinel": {
        "icon_svg": '<circle cx="24" cy="24" r="18" fill="#0078D4"/><path d="M24 12 L24 24 L32 28" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="24" cy="24" r="3" fill="white"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Security",
        "azure_icon_key": "azure_sentinel"
    },
    "data_explorer": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><path d="M14 30 L20 18 L26 26 L34 14" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "azure_data_explorer_clusters"
    },
    "kusto": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><path d="M14 30 L20 18 L26 26 L34 14" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Data",
        "azure_icon_key": "azure_data_explorer_clusters"
    },
    "signalr": {
        "icon_svg": '<circle cx="24" cy="24" r="18" fill="#0078D4"/><path d="M16 20 Q24 12 32 20 M16 28 Q24 36 32 28" stroke="white" stroke-width="2" fill="none" stroke-linecap="round"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Integration",
        "azure_icon_key": "signalr"
    },
    "notification_hub": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><path d="M18 16 L24 12 L30 16 L30 28 L18 28 Z" stroke="white" stroke-width="2" fill="white" opacity="0.9"/><circle cx="24" cy="32" r="3" fill="white"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Integration",
        "azure_icon_key": "notification_hubs"
    },
    "spring_apps": {
        "icon_svg": '<circle cx="24" cy="24" r="18" fill="#6DB33F"/><text x="24" y="28" text-anchor="middle" font-size="10" fill="white" font-weight="700">🌱</text>',
        "color": "#6DB33F", "bg": "#EFF8E8", "category": "Compute",
        "azure_icon_key": "azure_spring_apps"
    },
    "static_web_app": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><text x="24" y="28" text-anchor="middle" font-size="10" fill="white" font-weight="700">SWA</text>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Compute",
        "azure_icon_key": "static_apps"
    },
    "digital_twins": {
        "icon_svg": '<rect x="6" y="8" width="36" height="32" rx="4" fill="#0078D4"/><circle cx="18" cy="20" r="5" fill="white" opacity="0.9"/><circle cx="30" cy="20" r="5" fill="white" opacity="0.9"/><line x1="18" y1="25" x2="18" y2="34" stroke="white" stroke-width="2"/><line x1="30" y1="25" x2="30" y2="34" stroke="white" stroke-width="2"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "IoT",
        "azure_icon_key": "digital_twins"
    },
    "backup": {
        "icon_svg": '<rect x="8" y="8" width="32" height="32" rx="4" fill="#0078D4"/><path d="M16 28 L24 16 L32 28 Z" stroke="white" stroke-width="2" fill="white" opacity="0.8"/>',
        "color": "#0078D4", "bg": "#E8F4FD", "category": "Management",
        "azure_icon_key": "backup_vault"
    },
}

CONNECTION_STYLES = {
    "api":      {"color": "#0078D4", "dash": "0"},
    "data":     {"color": "#0F9D58", "dash": "0"},
    "security": {"color": "#E8A000", "dash": "5,5"},
    "private":  {"color": "#5C2D91", "dash": "3,3"},
    "network":  {"color": "#5C2D91", "dash": "5,5"},
    "default":  {"color": "#999999", "dash": "0"},
}


_TYPE_ALIASES = {
    # Nomes de recursos ARM do Azure → tipo canônico do diagrama
    # Rede
    "private_endpoints": "pe", "private_endpoint": "pe",
    "virtual_networks": "vnet", "virtual_network": "vnet",
    "network_security_groups": "nsg", "network_security_group": "nsg",
    "bastion_hosts": "bastion", "bastion_host": "bastion",
    "application_gateways": "app_gateway", "application_gateway": "app_gateway",
    "front_doors": "front_door", "front_door_and_cdn_profiles": "front_door",
    "virtual_network_gateways": "vpn", "vpn_gateways": "vpn",
    "load_balancers": "load_balancer",
    "nat_gateways": "nat_gateway",
    "expressroute_circuits": "expressroute",
    "firewalls": "firewall",
    "cdn_profiles": "cdn",
    # Dados
    "data_factories": "adf", "data_factory": "adf",
    "storage_accounts": "storage", "storage_account": "storage",
    "data_lake": "adls", "adls_gen2": "adls", "data_lake_storage": "adls",
    "fabric_capacities": "fabric", "fabric_capacity": "fabric", "microsoft_fabric": "fabric",
    "synapse_workspaces": "synapse", "synapse_workspace": "synapse", "synapse_analytics": "synapse",
    "cosmos": "cosmos_db", "cosmosdb": "cosmos_db", "documentdb": "cosmos_db",
    "sql_databases": "sql_database", "sql_db": "sql_database",
    "sql_servers": "sql_server",
    "redis_caches": "redis", "redis_cache": "redis", "cache_redis": "redis",
    "stream_analytics_jobs": "stream_analytics",
    "databricks_workspaces": "databricks",
    "data_explorer_clusters": "data_explorer", "azure_data_explorer": "data_explorer",
    "postgresql_server": "postgresql", "postgresql_servers": "postgresql",
    "mysql_server": "mysql", "mysql_servers": "mysql",
    # IA
    "cognitive_services": "ai_foundry", "ai_services": "ai_foundry", "foundry": "ai_foundry",
    "azure_openai": "openai",
    "cognitive_search": "search", "search_services": "search", "search_service": "search",
    "machine_learning": "aml", "ml": "aml", "machine_learning_workspaces": "aml",
    "form_recognizers": "document_intelligence",
    "ai_studio": "ai_hub", "foundry_project": "ai_hub",
    # Segurança
    "key_vault": "keyvault", "key_vaults": "keyvault",
    "sentinel": "sentinel", "azure_sentinel": "sentinel",
    # Computação
    "virtual_machines": "vm", "virtual_machine": "vm",
    "app_services": "appservice", "web_apps": "appservice", "web_app": "appservice",
    "function_apps": "function_app", "functions": "function_app",
    "kubernetes_services": "aks", "managed_clusters": "aks", "kubernetes": "aks",
    "container_registries": "acr",
    "container_apps_environments": "container_apps",
    "spring_apps": "spring_apps", "azure_spring_apps": "spring_apps",
    "static_apps": "static_web_app", "static_web_apps": "static_web_app",
    # Integração
    "event_hubs": "event_hub",
    "event_grid_topics": "event_grid", "event_grid_domains": "event_grid",
    "api_management_services": "apim",
    "service_bus_namespaces": "service_bus",
    "logic_app": "logic_apps",
    "notification_hubs": "notification_hub",
    # Monitoramento
    "log_analytics_workspaces": "log_analytics",
    "application_insights": "appinsights", "app_insight": "appinsights",
    # IoT
    "iot_hubs": "iot_hub",
    # Gerenciamento
    "backup_vaults": "backup", "backup_vault": "backup",
}

def get_service_info(svc_type: str) -> dict:
    t = svc_type.lower().replace("-", "_").replace(" ", "_")
    t = _TYPE_ALIASES.get(t, t)
    info = SERVICE_ICONS.get(t, SERVICE_ICONS["default"]).copy()
    # Adiciona o URI de dados do ícone oficial do Azure, se disponível
    azure_key = info.get("azure_icon_key", t)
    icon_uri = get_icon_data_uri(azure_key)
    info["icon_data_uri"] = icon_uri
    return info


def generate_html(services: list, connections: list, title: str, vnet_info: str = "", hierarchy: list = None) -> str:
    def _norm(t):
        t = t.lower().replace("-", "_").replace(" ", "_")
        return _TYPE_ALIASES.get(t, t)

    nodes_js = json.dumps([{
        "id": svc["id"],
        "name": svc["name"],
        "type": _norm(svc.get("type", "default")),
        "sku": svc.get("sku", ""),
        "private": svc.get("private", False),
        "details": svc.get("details", []),
        "subscription": svc.get("subscription", ""),
        "resourceGroup": svc.get("resourceGroup", ""),
        "icon_svg": get_service_info(svc.get("type", "default"))["icon_svg"],
        "icon_data_uri": get_service_info(svc.get("type", "default")).get("icon_data_uri", ""),
        "color": get_service_info(svc.get("type", "default"))["color"],
        "bg": get_service_info(svc.get("type", "default"))["bg"],
        "category": get_service_info(svc.get("type", "default"))["category"],
    } for svc in services], ensure_ascii=False)

    hierarchy_js = json.dumps(hierarchy or [], ensure_ascii=False)

    edges_js = json.dumps([{
        "from": conn["from"],
        "to": conn["to"],
        "label": conn.get("label", ""),
        "type": conn.get("type", "default"),
        "color": CONNECTION_STYLES.get(conn.get("type", "default"), CONNECTION_STYLES["default"])["color"],
        "dash": CONNECTION_STYLES.get(conn.get("type", "default"), CONNECTION_STYLES["default"])["dash"],
    } for conn in connections], ensure_ascii=False)

    pe_count = sum(1 for s in services if _norm(s.get("type", "default")) == "pe")
    svc_count = len(services) - pe_count
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    vnet_info_js = json.dumps(vnet_info, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif; background: #f3f2f1; color: #323130; }}

  .header {{
    background: white; border-bottom: 1px solid #edebe9;
    padding: 12px 24px; display: flex; align-items: center; gap: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }}
  .header-icon {{
    width: 32px; height: 32px; border-radius: 4px;
    background: linear-gradient(135deg, #0078D4, #00BCF2);
    display: flex; align-items: center; justify-content: center;
  }}
  .header-icon svg {{ width: 20px; height: 20px; }}
  .header h1 {{ font-size: 15px; font-weight: 600; color: #201f1e; }}
  .header .meta {{ font-size: 11px; color: #a19f9d; }}
  .header-right {{ margin-left: auto; display: flex; gap: 16px; align-items: center; }}
  .stat {{ font-size: 11px; color: #605e5c; }}
  .stat b {{ color: #323130; }}

  .container {{ display: flex; height: calc(100vh - 56px); }}

  .canvas-area {{
    flex: 1; position: relative; overflow: hidden;
    background: white;
    background-image:
      linear-gradient(#faf9f8 1px, transparent 1px),
      linear-gradient(90deg, #faf9f8 1px, transparent 1px);
    background-size: 24px 24px;
  }}
  #canvas {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}

  .toolbar {{
    position: absolute; top: 10px; left: 10px;
    display: flex; gap: 1px; z-index: 10;
    background: white; border: 1px solid #edebe9; border-radius: 6px;
    padding: 2px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }}
  .tool-btn {{
    background: transparent; border: none; border-radius: 4px;
    padding: 5px 10px; font-size: 11px; cursor: pointer; color: #605e5c;
    font-family: inherit; transition: all 0.1s;
  }}
  .tool-btn:hover {{ background: #f3f2f1; color: #323130; }}
  .tool-sep {{ width: 1px; background: #edebe9; margin: 3px 1px; }}

  .zoom-indicator {{
    position: absolute; top: 10px; right: 286px;
    background: white; border: 1px solid #edebe9; border-radius: 4px;
    padding: 3px 8px; font-size: 10px; color: #a19f9d; z-index: 10;
  }}

  /* ── Barra lateral ── */
  .sidebar {{
    width: 272px; background: #faf9f8; border-left: 1px solid #edebe9;
    overflow-y: auto; display: flex; flex-direction: column;
  }}
  .sidebar::-webkit-scrollbar {{ width: 3px; }}
  .sidebar::-webkit-scrollbar-thumb {{ background: #c8c6c4; border-radius: 3px; }}

  .sidebar-header {{
    padding: 12px 14px; border-bottom: 1px solid #edebe9;
    font-weight: 600; font-size: 12px; color: #605e5c;
    position: sticky; top: 0; background: #faf9f8; z-index: 1;
  }}
  .cat-label {{
    padding: 10px 14px 4px; font-size: 10px; color: #a19f9d;
    font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
  }}
  .service-card {{
    margin: 2px 6px; border: 1px solid #edebe9; border-radius: 6px;
    overflow: hidden; cursor: pointer; transition: all 0.1s;
    background: white;
  }}
  .service-card:hover {{ border-color: #c8c6c4; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
  .service-card.selected {{ border-color: #0078D4; box-shadow: 0 0 0 1px #0078D4; }}
  .service-card-header {{
    padding: 7px 10px; display: flex; align-items: center; gap: 8px;
  }}
  .sc-icon {{ width: 28px; height: 28px; flex-shrink: 0; }}
  .sc-icon svg {{ width: 28px; height: 28px; }}
  .service-name {{ font-size: 12px; font-weight: 600; color: #323130; }}
  .service-sku {{ font-size: 10px; color: #a19f9d; }}
  .service-card-body {{ padding: 2px 10px 6px; }}
  .service-detail {{ font-size: 10px; color: #605e5c; padding: 1px 0; }}
  .service-detail::before {{ content: "› "; color: #a19f9d; }}
  .private-badge {{
    font-size: 9px; background: #f3eef9; color: #5C2D91;
    border-radius: 3px; padding: 1px 5px; margin-left: auto;
    border: 1px solid #e0d4f5;
  }}

  .legend {{
    padding: 10px 14px; border-top: 1px solid #edebe9; margin-top: auto;
  }}
  .legend-title {{ font-size: 10px; font-weight: 600; color: #a19f9d; margin-bottom: 5px; }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; font-size: 10px; color: #605e5c; margin-bottom: 2px; }}
  .legend-line {{ width: 18px; height: 2px; border-radius: 1px; }}
  .legend-line-dash {{ width: 18px; height: 0; border-top: 2px dashed; }}

  /* ── Estilos SVG ── */
  .node {{ cursor: grab; pointer-events: all; }}
  .node:active {{ cursor: grabbing; }}
  .node .node-bg {{ pointer-events: all; }}
  .node.selected .node-bg {{ stroke: #0078D4; stroke-width: 2.5; }}
  .node.selected {{ filter: drop-shadow(0 0 6px rgba(0,120,212,0.4)); }}

  /* ── Destaque de arestas ao selecionar um nó ── */
  .edge-path {{ transition: opacity 0.2s, stroke-width 0.2s; }}
  .edge-label {{ transition: opacity 0.2s; }}
  .edge-path.highlight {{ opacity: 1 !important; stroke-width: 2.5 !important; filter: drop-shadow(0 0 4px rgba(0,120,212,0.5)); }}
  .edge-path.dimmed {{ opacity: 0.1 !important; }}
  .edge-label.highlight {{ opacity: 1 !important; font-weight: 700; }}
  .edge-label.dimmed {{ opacity: 0.15 !important; }}
  .edge-label-bg.highlight {{ stroke: #0078D4 !important; stroke-width: 1.5 !important; }}
  .edge-label-bg.dimmed {{ opacity: 0.15 !important; }}
  .node.dimmed {{ opacity: 0.25; transition: opacity 0.2s; }}

  .subnet-rect {{
    rx: 6; ry: 6;
  }}
  .subnet-label {{
    font-size: 11px; font-weight: 600; font-family: 'Segoe UI', sans-serif;
  }}

  .status-bar {{
    position: absolute; bottom: 10px; left: 10px;
    background: white; border: 1px solid #edebe9; border-radius: 4px;
    padding: 4px 10px; font-size: 10px; color: #a19f9d;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }}

  .tooltip {{
    position: absolute; background: white; color: #323130;
    border: 1px solid #edebe9; padding: 8px 12px;
    border-radius: 6px; font-size: 11px; pointer-events: none;
    white-space: nowrap; z-index: 100; display: none;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  }}
  .tooltip strong {{ color: #201f1e; }}
  .tooltip-detail {{ color: #605e5c; margin-top: 1px; font-size: 10px; }}
</style>
</head>
<body>

<div class="header">
  <div class="header-icon">
    <svg viewBox="0 0 24 24"><path d="M12 2L2 7v10l10 5 10-5V7L12 2z" fill="white" opacity="0.9"/></svg>
  </div>
  <div>
    <h1>{title}</h1>
    <div class="meta">Arquitetura do Azure &middot; {generated_at}</div>
  </div>
  <div class="header-right">
    <div class="stat"><b>{svc_count}</b> serviços</div>
    <div class="stat"><b>{pe_count}</b> Private Endpoints</div>
    <div class="stat"><b>{len(connections)}</b> conexões</div>
  </div>
</div>

<div class="container">
  <div class="canvas-area">
    <div class="toolbar">
      <button class="tool-btn" onclick="fitToScreen()">Ajustar</button>
      <div class="tool-sep"></div>
      <button class="tool-btn" onclick="zoomIn()">+</button>
      <button class="tool-btn" onclick="zoomOut()">&minus;</button>
      <div class="tool-sep"></div>
      <button class="tool-btn" onclick="textBigger()" title="Aumentar texto" style="font-size:13px;">A+</button>
      <button class="tool-btn" onclick="textSmaller()" title="Diminuir texto" style="font-size:10px;">A&minus;</button>
      <div class="tool-sep"></div>
      <button class="tool-btn" onclick="downloadPNG()" title="Baixar PNG">&#128247; PNG</button>
    </div>
    <div class="zoom-indicator" id="zoom-level">100%</div>
    <svg id="canvas">
      <defs>
        <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke" opacity="0.7"/>
        </marker>
        <marker id="arr-data" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke" opacity="0.7"/>
        </marker>
        <marker id="arr-sec" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke" opacity="0.7"/>
        </marker>
        <marker id="arr-pe" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke" opacity="0.7"/>
        </marker>
        <filter id="shadow">
          <feDropShadow dx="0" dy="1" stdDeviation="2" flood-opacity="0.08"/>
        </filter>
      </defs>
      <g id="diagram-root"></g>
    </svg>
    <div id="tooltip" class="tooltip"></div>
    <div class="status-bar">Arraste os nós &middot; Role para ampliar &middot; Arraste o espaço vazio para mover</div>
  </div>

  <div class="sidebar">
    <div class="sidebar-header">Recursos</div>
    <div id="service-list"></div>
    <div class="legend">
      <div class="legend-title">Tipos de conexão</div>
      <div class="legend-item"><div class="legend-line" style="background:#0078D4;"></div> API</div>
      <div class="legend-item"><div class="legend-line" style="background:#0F9D58;"></div> Dados</div>
      <div class="legend-item"><div class="legend-line-dash" style="border-color:#E8A000;"></div> Segurança</div>
      <div class="legend-item"><div class="legend-line-dash" style="border-color:#5C2D91;"></div> Private Endpoint</div>
    </div>
  </div>
</div>

<script>
const NODES = {nodes_js};
const EDGES = {edges_js};
const VNET_INFO = {vnet_info_js};
const HIERARCHY = {hierarchy_js};
const CATEGORY_LABELS = {{
  'AI': 'IA', 'Data': 'Dados', 'Security': 'Segurança', 'Compute': 'Computação',
  'Integration': 'Integração', 'Network': 'Rede', 'External': 'Externo',
  'Monitor': 'Monitoramento', 'Monitoring': 'Monitoramento',
  'Management': 'Gerenciamento', 'Azure': 'Azure', 'DevOps': 'DevOps', 'IoT': 'IoT'
}};
function categoryLabel(category) {{ return CATEGORY_LABELS[category] || category; }}

// ── Dimensionamento dos nós ──
const SVC_W = 180, SVC_H = 120;  // nó de serviço (ícone acima, nome abaixo), 20% maior
const PE_W = 120, PE_H = 84;     // nó de PE (menor), 20% maior
const GAP = 40;

// ── Layout: estilo de caixa de grupo por categoria ──
// Cada categoria recebe uma caixa rotulada, com os serviços organizados em uma grade.
// Os grupos são organizados em 2D: serviços principais acima e demais grupos abaixo.
// Os nós de PE ficam em um grupo separado de sub-rede de PE.

const positions = {{}};
const useRgLayout = HIERARCHY.length > 0 && NODES.some(n => n.resourceGroup);
const peNodes = useRgLayout ? [] : NODES.filter(n => n.type === 'pe');  // Modo RG: PE incluído em mainNodes
const mainNodes = useRgLayout ? NODES : NODES.filter(n => n.type !== 'pe');

// Parâmetros de layout das caixas de grupo
const GROUP_PAD = 24;
const GROUP_TITLE_H = 28;
const GROUP_GAP = 60;
const COLS_PER_GROUP = 3;
const CELL_W = SVC_W + 100;
const CELL_H = SVC_H + 90;

function groupDimensions(nodeCount) {{
  const cols = Math.min(nodeCount, COLS_PER_GROUP);
  const rows = Math.ceil(nodeCount / COLS_PER_GROUP);
  const w = cols * CELL_W + GROUP_PAD * 2;
  const h = rows * CELL_H + GROUP_PAD + GROUP_TITLE_H;
  return {{ w, h, cols, rows }};
}}

const groupBoxes = [];

// ── Estratégia de layout: por RG (se houver HIERARCHY) ou por categoria (padrão) ──

if (useRgLayout) {{
  // ── Layout por RG: agrupa por assinatura > ResourceGroup ──
  let gx = 60, gy = 140;
  let subStartX = 60;
  const SUB_GAP = 80;
  const RG_GAP = 60;

  HIERARCHY.forEach((sub, subIdx) => {{
    let rgX = gx;
    let rgMaxH = 0;

    const subRGs = sub.resourceGroups || [];
    subRGs.forEach((rgName, rgIdx) => {{
      const rgNodes = mainNodes.filter(n => n.subscription === sub.subscription && n.resourceGroup === rgName);
      if (rgNodes.length === 0) return;

      const dim = groupDimensions(rgNodes.length);

      rgNodes.forEach((n, i) => {{
        const col = i % dim.cols;
        const row = Math.floor(i / dim.cols);
        positions[n.id] = {{
          x: rgX + GROUP_PAD + col * CELL_W + (CELL_W - SVC_W) / 2,
          y: gy + GROUP_TITLE_H + row * CELL_H + (CELL_H - SVC_H) / 2
        }};
      }});

      groupBoxes.push({{
        cat: rgName, x: rgX, y: gy, w: dim.w, h: dim.h,
        color: rgNodes[0]?.color || '#0078D4',
        isRG: true, subscription: sub.subscription
      }});

      rgX += dim.w + RG_GAP;
      rgMaxH = Math.max(rgMaxH, dim.h);
    }});

    // Próxima linha de assinatura
    if (subIdx < HIERARCHY.length - 1) {{
      gy += rgMaxH + SUB_GAP;
      gx = subStartX;
    }}
  }});

  // Coloca os nós principais sem atribuição (sem assinatura/RG) em um grupo genérico
  const unassigned = mainNodes.filter(n => !positions[n.id]);
  if (unassigned.length > 0) {{
    const allY = Object.values(positions).map(p => p.y);
    const bottomY = allY.length > 0 ? Math.max(...allY) + SVC_H + GROUP_GAP : 140;
    const dim = groupDimensions(unassigned.length);
    unassigned.forEach((n, i) => {{
      const col = i % dim.cols;
      const row = Math.floor(i / dim.cols);
      positions[n.id] = {{
        x: 60 + GROUP_PAD + col * CELL_W + (CELL_W - SVC_W) / 2,
        y: bottomY + GROUP_TITLE_H + row * CELL_H + (CELL_H - SVC_H) / 2
      }};
    }});
    groupBoxes.push({{
      cat: 'Outros', x: 60, y: bottomY, w: dim.w, h: dim.h,
      color: '#666'
    }});
  }}

}} else {{
  // ── Layout por categoria (original) ──
  const bottomCategories = ['Network', 'External', 'Monitor', 'Monitoring'];
  const catOrder = ['AI', 'Data', 'Security', 'Compute', 'Integration', 'DevOps', 'IoT', 'Azure'];

  const catGroups = {{}};
  mainNodes.forEach(n => {{
    const cat = n.category || 'Azure';
    if (!catGroups[cat]) catGroups[cat] = [];
    catGroups[cat].push(n);
  }});

// Inclui dinamicamente categorias que não estejam em catOrder nem em bottomCategories
const extraCats = Object.keys(catGroups).filter(cat => !catOrder.includes(cat) && !bottomCategories.includes(cat));
const fullCatOrder = [...catOrder, ...extraCats];

// ── Posiciona os grupos de serviços principais em uma grade fluida ──
const serviceGroups = fullCatOrder.filter(cat => catGroups[cat] && catGroups[cat].length > 0
  && !bottomCategories.includes(cat));

let gx = 60, gy = 140;
let rowMaxH = 0;
let rowStartX = 60;
const MAX_ROW_W = Math.max(1600, serviceGroups.length * 400);

serviceGroups.forEach(cat => {{
  const nodes = catGroups[cat];
  const dim = groupDimensions(nodes.length);

  // Quebra para a próxima linha se ficar muito largo
  if (gx + dim.w > rowStartX + MAX_ROW_W && gx > rowStartX) {{
    gx = rowStartX;
    gy += rowMaxH + GROUP_GAP;
    rowMaxH = 0;
  }}

  // Posiciona os nós na grade do grupo
  nodes.forEach((n, i) => {{
    const col = i % dim.cols;
    const row = Math.floor(i / dim.cols);
    positions[n.id] = {{
      x: gx + GROUP_PAD + col * CELL_W + (CELL_W - SVC_W) / 2,
      y: gy + GROUP_TITLE_H + row * CELL_H + (CELL_H - SVC_H) / 2
    }};
  }});

  groupBoxes.push({{
    cat, x: gx, y: gy, w: dim.w, h: dim.h,
    color: nodes[0]?.color || '#0078D4'
  }});

  gx += dim.w + GROUP_GAP;
  rowMaxH = Math.max(rowMaxH, dim.h);
}});

// ── Posiciona os grupos inferiores (Rede, Externo, Monitoramento) ──
const bottomGroupY = gy + rowMaxH + GROUP_GAP + 20;
let bgx = 60;
bottomCategories.forEach(cat => {{
  const nodes = catGroups[cat];
  if (!nodes || nodes.length === 0) return;
  const dim = groupDimensions(nodes.length);

  nodes.forEach((n, i) => {{
    const col = i % dim.cols;
    const row = Math.floor(i / dim.cols);
    positions[n.id] = {{
      x: bgx + GROUP_PAD + col * CELL_W + (CELL_W - SVC_W) / 2,
      y: bottomGroupY + GROUP_TITLE_H + row * CELL_H + (CELL_H - SVC_H) / 2
    }};
  }});

  groupBoxes.push({{
    cat, x: bgx, y: bottomGroupY, w: dim.w, h: dim.h,
    color: nodes[0]?.color || '#666',
    isBottom: true
  }});

  bgx += dim.w + GROUP_GAP;
}});

}} // fim do else (layout por categoria)

// ── Posicionamento dos nós de PE ──
if (useRgLayout) {{
  // Modo RG: os nós de PE ficam dentro das respectivas caixas de RG
  // O layout de RG já define as posições dos PEs que têm subscription/resourceGroup
  // Coloca os PEs sem atribuição de RG em um grupo separado
  const unplacedPEs = peNodes.filter(pe => !positions[pe.id]);
  if (unplacedPEs.length > 0) {{
    // Localiza a caixa de RG mais à direita
    const allGbRight = groupBoxes.length > 0 ? Math.max(...groupBoxes.map(gb => gb.x + gb.w)) : 0;
    const peStartX = allGbRight + GROUP_GAP;
    const peStartY = 140;
    const peCols = Math.min(unplacedPEs.length, 4);
    const peCellW = PE_W + 50;
    const peCellH = PE_H + 30;
    const peBoxW = peCols * peCellW + GROUP_PAD * 2;
    const peRows = Math.ceil(unplacedPEs.length / peCols);
    const peBoxH = peRows * peCellH + GROUP_PAD + GROUP_TITLE_H;

    unplacedPEs.forEach((pe, i) => {{
      const col = i % peCols;
      const row = Math.floor(i / peCols);
      positions[pe.id] = {{
        x: peStartX + GROUP_PAD + col * peCellW + (peCellW - PE_W) / 2,
        y: peStartY + GROUP_TITLE_H + row * peCellH + (peCellH - PE_H) / 2
      }};
    }});
    groupBoxes.push({{
      cat: 'Private Endpoints', x: peStartX, y: peStartY, w: peBoxW, h: peBoxH,
      color: '#5C2D91', isPE: true
    }});
  }}
}} else {{
  // Modo de categoria: nós de PE em grupo separado acima dos grupos de serviços
  const PE_Y = 40;
  if (peNodes.length > 0) {{
    const peCols = Math.min(peNodes.length, 6);
    const peRows = Math.ceil(peNodes.length / peCols);
    const peCellW = PE_W + 50;
    const peCellH = PE_H + 30;
    const peBoxW = peCols * peCellW + GROUP_PAD * 2;
    const peBoxH = peRows * peCellH + GROUP_PAD + GROUP_TITLE_H;

    peNodes.forEach((pe, i) => {{
      const col = i % peCols;
      const row = Math.floor(i / peCols);
      positions[pe.id] = {{
        x: 60 + GROUP_PAD + col * peCellW + (peCellW - PE_W) / 2,
        y: PE_Y + GROUP_TITLE_H + row * peCellH + (peCellH - PE_H) / 2
      }};
    }});

    groupBoxes.push({{
      cat: 'Private Endpoints', x: 60, y: PE_Y, w: peBoxW, h: peBoxH,
      color: '#5C2D91', isPE: true
    }});

    const peBottom = PE_Y + peBoxH + GROUP_GAP;
    if (peBottom > 140) {{
      const shift = peBottom - 140;
      NODES.forEach(n => {{
        if (n.type !== 'pe' && positions[n.id]) {{
          positions[n.id].y += shift;
        }}
      }});
      groupBoxes.forEach(gb => {{
        if (!gb.isPE) gb.y += shift;
      }});
    }}
  }}
}}

// ── Mapeamento de nó para grupo (para roteamento de arestas) ──
const nodeGroupMap = {{}};
groupBoxes.forEach((gb, idx) => {{
  NODES.forEach(n => {{
    const pos = positions[n.id];
    if (!pos) return;
    const nw = n.type === 'pe' ? PE_W : SVC_W;
    const nh = n.type === 'pe' ? PE_H : SVC_H;
    const ncx = pos.x + nw / 2;
    const ncy = pos.y + nh / 2;
    if (ncx >= gb.x && ncx <= gb.x + gb.w && ncy >= gb.y && ncy <= gb.y + gb.h) {{
      nodeGroupMap[n.id] = idx;
    }}
  }});
}});
// Margens do corredor de roteamento (fora de todas as caixas de grupo)
const _rightMarginBase = groupBoxes.length > 0 ? Math.max(...groupBoxes.map(g => g.x + g.w)) + 40 : 800;
const _leftMarginBase = groupBoxes.length > 0 ? Math.min(...groupBoxes.map(g => g.x)) - 40 : -40;

// ── Estado ──
let dragging = null, dragOffX = 0, dragOffY = 0;
let draggingGroup = null, groupDragNodes = [];  // para arrastar o RG/a caixa de grupo
let _dragStartX = 0, _dragStartY = 0, _didDrag = false;  // global para que a reconstrução do DOM por renderDiagram durante o arraste não redefina os valores
let viewTransform = {{ x: 0, y: 0, scale: 1 }};
let isPanning = false, panSX = 0, panSY = 0, panSTx = 0, panSTy = 0;
let _routeCounter = 0;

// ── Destaque bidirecional ──
let _selectedNodeId = null;

function selectNode(nodeId) {{
  const wasSelected = _selectedNodeId === nodeId;

  // Limpa todas as seleções
  clearSelection();

  // Desativa ao clicar no mesmo nó
  if (wasSelected) {{ _selectedNodeId = null; return; }}

  _selectedNodeId = nodeId;
  applySelectionHighlight();
  // Rola o cartão da barra lateral até ficar visível na seleção inicial
  const sCard = document.getElementById('card-' + nodeId);
  if (sCard) sCard.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
}}

// Reaplica as classes CSS do _selectedNodeId atual (chamado após renderDiagram reconstruir o DOM)
function applySelectionHighlight() {{
  const nodeId = _selectedNodeId;
  if (!nodeId) return;

  // Destaca o nó do diagrama
  const svgNode = document.querySelector(`.node[data-id="${{nodeId}}"]`);
  if (svgNode) svgNode.classList.add('selected');
  // Destaca o cartão da barra lateral
  const card = document.getElementById('card-' + nodeId);
  if (card) card.classList.add('selected');

  // Localiza as arestas conectadas (nas quais este nó é origem ou destino)
  const connectedNodeIds = new Set([nodeId]);
  document.querySelectorAll('.edge-path').forEach(p => {{
    const f = p.getAttribute('data-from'), t = p.getAttribute('data-to');
    if (f === nodeId || t === nodeId) {{
      p.classList.add('highlight');
      connectedNodeIds.add(f);
      connectedNodeIds.add(t);
    }} else {{
      p.classList.add('dimmed');
    }}
  }});
  document.querySelectorAll('.edge-label').forEach(g => {{
    const f = g.getAttribute('data-from'), t = g.getAttribute('data-to');
    if (f === nodeId || t === nodeId) {{
      g.classList.add('highlight');
      g.querySelector('.edge-label-bg')?.classList.add('highlight');
    }} else {{
      g.classList.add('dimmed');
      g.querySelector('.edge-label-bg')?.classList.add('dimmed');
    }}
  }});
  // Atenua os nós não conectados
  document.querySelectorAll('.node').forEach(n => {{
    const nid = n.getAttribute('data-id');
    if (!connectedNodeIds.has(nid)) n.classList.add('dimmed');
  }});
}}

function clearSelection() {{
  _selectedNodeId = null;
  document.querySelectorAll('.node').forEach(n => {{ n.classList.remove('selected', 'dimmed'); }});
  document.querySelectorAll('.service-card').forEach(c => c.classList.remove('selected'));
  document.querySelectorAll('.edge-path').forEach(p => {{ p.classList.remove('highlight', 'dimmed'); }});
  document.querySelectorAll('.edge-label').forEach(g => {{ g.classList.remove('highlight', 'dimmed'); }});
  document.querySelectorAll('.edge-label-bg').forEach(r => {{ r.classList.remove('highlight', 'dimmed'); }});
}}

function markerFor(type) {{
  if (type === 'data') return 'arr-data';
  if (type === 'security') return 'arr-sec';
  if (type === 'private') return 'arr-pe';
  return 'arr';
}}

function renderDiagram() {{
  const root = document.getElementById('diagram-root');
  root.innerHTML = '';
  _routeCounter = 0;  // redefine o contador de deslocamento a cada renderização

  // ── Limites da VNet (elevados para que avoidNodes possa mover desvios para fora da VNet) ──
  let _vnetBounds = null;
  if (!useRgLayout) {{
    const _pg = groupBoxes.filter(gb => !gb.isBottom);
    const _hasPriv = NODES.some(n => n.private && n.type !== 'pe');
    const _hasVNI = VNET_INFO && VNET_INFO.length > 0;
    const _hasPe = NODES.some(n => n.type === 'pe');
    if (_pg.length > 0 && (_hasPriv || _hasVNI || _hasPe)) {{
      const vx = Math.min(..._pg.map(g => g.x)) - 16;
      const vy = Math.min(..._pg.map(g => g.y)) - 36;
      const vR = Math.max(..._pg.map(g => g.x + g.w)) + 16;
      const vB = Math.max(..._pg.map(g => g.y + g.h)) + 16;
      _vnetBounds = {{ x: vx, y: vy, w: vR - vx, h: vB - vy }};
    }}
  }}

  // ── Desenha o limite da VNet (somente no layout por categoria, não no layout de RG) ──
  if (!useRgLayout) {{
  const privateGroups = groupBoxes.filter(gb => !gb.isBottom);
  const hasPrivateNodes = NODES.some(n => n.private && n.type !== 'pe');
  const hasVNetInfo = VNET_INFO && VNET_INFO.length > 0;
  const hasPeNodes = NODES.some(n => n.type === 'pe');
  const showVNet = hasPrivateNodes || hasVNetInfo || hasPeNodes;

  if (privateGroups.length > 0 && showVNet) {{
      const vx = Math.min(...privateGroups.map(g => g.x)) - 16;
      const vy = Math.min(...privateGroups.map(g => g.y)) - 36;
      const vRight = Math.max(...privateGroups.map(g => g.x + g.w)) + 16;
      const vBottom = Math.max(...privateGroups.map(g => g.y + g.h)) + 16;

      const vr = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      vr.setAttribute('x', vx); vr.setAttribute('y', vy);
      vr.setAttribute('width', vRight - vx); vr.setAttribute('height', vBottom - vy);
      vr.setAttribute('fill', '#f8f7ff'); vr.setAttribute('stroke', '#5C2D91');
      vr.setAttribute('stroke-width', '2'); vr.setAttribute('stroke-dasharray', '8,4');
      vr.setAttribute('rx', '12');
      root.appendChild(vr);

      const vnetLabel = VNET_INFO ? `Virtual Network (${{VNET_INFO}})` : 'Virtual Network';
      const vl = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      vl.setAttribute('class', 'vnet-boundary-label');
      vl.setAttribute('style', 'cursor: pointer;');
      vl.innerHTML = `<svg x="${{vx + 10}}" y="${{vy + 6}}" width="20" height="20" viewBox="0 0 48 48">
        <rect x="6" y="6" width="36" height="36" rx="4" fill="none" stroke="#5C2D91" stroke-width="3"/>
        <circle cx="16" cy="18" r="3" fill="#5C2D91"/><circle cx="32" cy="18" r="3" fill="#5C2D91"/><circle cx="24" cy="32" r="3" fill="#5C2D91"/>
      </svg>
      <text x="${{vx + 34}}" y="${{vy + 20}}" font-size="12" font-weight="600" fill="#5C2D91" font-family="Segoe UI, sans-serif">${{vnetLabel}}</text>`;
      root.appendChild(vl);

      // Armazena a referência do retângulo da VNet para destaque
      vr.setAttribute('id', 'vnet-rect');
      vl.addEventListener('click', () => {{ toggleVNetHighlight(); }});
      root.appendChild(vl);
  }}
  }} // fim de if(!useRgLayout) para o limite da VNet

  // ── Desenha as caixas de grupo (categoria ou RG, conforme o modo de layout) ──
  const _groupLabelElements = []; // armazena rótulos para renderizá-los novamente sobre as arestas
  groupBoxes.forEach(gb => {{
    if (gb.isPE) {{
      // Grupo de PE: sempre desenhado com estilo tracejado
      const gr = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      gr.setAttribute('x', gb.x); gr.setAttribute('y', gb.y);
      gr.setAttribute('width', gb.w); gr.setAttribute('height', gb.h);
      gr.setAttribute('rx', '8'); gr.setAttribute('fill', '#f3eef9');
      gr.setAttribute('stroke', '#c8b8e8'); gr.setAttribute('stroke-width', '1.2');
      gr.setAttribute('stroke-dasharray', '4,4');
      root.appendChild(gr);
    }} else {{
      // Grupo de serviços (categoria ou RG)
      const gr = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      gr.setAttribute('x', gb.x); gr.setAttribute('y', gb.y);
      gr.setAttribute('width', gb.w); gr.setAttribute('height', gb.h);
      gr.setAttribute('rx', '8');
      gr.setAttribute('fill', gb.isRG ? '#fafafa' : 'white');
      gr.setAttribute('stroke', gb.isRG ? gb.color : '#c8c6c4');
      gr.setAttribute('stroke-width', gb.isRG ? '1.5' : '1.2');
      if (gb.isRG) gr.setAttribute('stroke-dasharray', '6,3');
      root.appendChild(gr);
    }}

    // Barra de título
    const titleBar = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    titleBar.setAttribute('x', gb.x); titleBar.setAttribute('y', gb.y);
    titleBar.setAttribute('width', gb.w); titleBar.setAttribute('height', GROUP_TITLE_H);
    titleBar.setAttribute('rx', '8');
    titleBar.setAttribute('fill', gb.color);
    titleBar.setAttribute('opacity', '0.1');
    root.appendChild(titleBar);
    const titleFill = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    titleFill.setAttribute('x', gb.x); titleFill.setAttribute('y', gb.y + GROUP_TITLE_H - 8);
    titleFill.setAttribute('width', gb.w); titleFill.setAttribute('height', '8');
    titleFill.setAttribute('fill', gb.color); titleFill.setAttribute('opacity', '0.1');
    root.appendChild(titleFill);

    // Linha de destaque colorida
    const accent = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    accent.setAttribute('x', gb.x); accent.setAttribute('y', gb.y);
    accent.setAttribute('width', gb.w); accent.setAttribute('height', '3');
    accent.setAttribute('rx', '8'); accent.setAttribute('fill', gb.color);
    root.appendChild(accent);

    // Rótulo do grupo: RG usa 📁, PE usa "Private Endpoints" e categoria usa o nome da categoria
    const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    label.setAttribute('x', gb.x + 12); label.setAttribute('y', gb.y + 18);
    label.setAttribute('font-size', '12'); label.setAttribute('font-weight', '600');
    label.setAttribute('fill', gb.color); label.setAttribute('font-family', 'Segoe UI, sans-serif');
    label.textContent = gb.isRG ? `📁 ${{gb.cat}}` : categoryLabel(gb.cat);
    root.appendChild(label);
    _groupLabelElements.push(label);

    // Torna a barra de título arrastável e move todos os nós internos
    titleBar.style.cursor = 'grab';
    const gbIdx = groupBoxes.indexOf(gb);
    titleBar.addEventListener('mousedown', e => {{
      if (e.button !== 0) return;
      e.stopPropagation(); e.preventDefault();
      draggingGroup = gbIdx;
      const svgPt = getSVGPoint(e);
      dragOffX = svgPt.x; dragOffY = svgPt.y;
      // Localiza todos os nós dentro desta caixa de grupo
      groupDragNodes = NODES.filter(n => {{
        const pos = positions[n.id];
        if (!pos) return false;
        const nw = n.type === 'pe' ? PE_W : SVC_W;
        const nh = n.type === 'pe' ? PE_H : SVC_H;
        const cx = pos.x + nw/2, cy = pos.y + nh/2;
        return cx >= gb.x && cx <= gb.x + gb.w && cy >= gb.y && cy <= gb.y + gb.h;
      }}).map(n => n.id);
    }});
  }});

  // ── Desenha os limites das assinaturas (somente para várias assinaturas, após as caixas de grupo) ──
  if (HIERARCHY.length > 1 && useRgLayout) {{
    HIERARCHY.forEach((sub, subIdx) => {{
      // Localiza todas as caixas de RG pertencentes a esta assinatura
      const subRgBoxes = groupBoxes.filter(gb => gb.isRG && gb.subscription === sub.subscription);
      if (subRgBoxes.length === 0) return;

      const sx = Math.min(...subRgBoxes.map(gb => gb.x)) - 20;
      const sy = Math.min(...subRgBoxes.map(gb => gb.y)) - 40;
      const sRight = Math.max(...subRgBoxes.map(gb => gb.x + gb.w)) + 20;
      const sBottom = Math.max(...subRgBoxes.map(gb => gb.y + gb.h)) + 20;

      const sr = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      sr.setAttribute('x', sx); sr.setAttribute('y', sy);
      sr.setAttribute('width', sRight - sx); sr.setAttribute('height', sBottom - sy);
      sr.setAttribute('fill', 'none'); sr.setAttribute('stroke', '#0078D4');
      sr.setAttribute('stroke-width', '2.5'); sr.setAttribute('stroke-dasharray', '12,4');
      sr.setAttribute('rx', '16'); sr.setAttribute('opacity', '0.7');
      root.appendChild(sr);

      const sl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      sl.setAttribute('x', sx + 12); sl.setAttribute('y', sy + 16);
      sl.setAttribute('font-size', '12'); sl.setAttribute('font-weight', '700');
      sl.setAttribute('fill', '#0078D4'); sl.setAttribute('font-family', 'Segoe UI, sans-serif');
      sl.textContent = `📦 ${{sub.subscription}}`;
      root.appendChild(sl);
    }});
  }}

  // ── Roteamento de arestas (sem obstáculos) ──
  // Calcula os limites globais: a parte inferior absoluta de TODOS os nós
  function getGlobalBounds() {{
    let minY = Infinity, maxY = -Infinity;
    NODES.forEach(n => {{
      const pos = positions[n.id];
      if (!pos) return;
      const h = n.type === 'pe' ? PE_H : SVC_H;
      if (pos.y < minY) minY = pos.y;
      if (pos.y + h > maxY) maxY = pos.y + h;
    }});
    return {{ minY, maxY }};
  }}

  function getNodeBox(node) {{
    const pos = positions[node.id];
    if (!pos) return null;
    const w = node.type === 'pe' ? PE_W : SVC_W;
    const h = node.type === 'pe' ? PE_H : SVC_H;
    return {{ x: pos.x, y: pos.y, w, h, cx: pos.x + w/2, cy: pos.y + h/2 }};
  }}

  // Ponto da borda: saída/entrada na borda do retângulo
  function borderExit(box, side) {{
    // lado: 'top', 'bottom', 'left', 'right'
    if (side === 'top') return {{ x: box.cx, y: box.y }};
    if (side === 'bottom') return {{ x: box.cx, y: box.y + box.h }};
    if (side === 'left') return {{ x: box.x, y: box.cy }};
    if (side === 'right') return {{ x: box.x + box.w, y: box.cy }};
  }}

  // Verifica se um segmento de linha atinge alguma caixa de grupo (para rotear arestas)
  function hitsGroupBox(x1, y1, x2, y2, skipGroupIndices) {{
    for (let gi = 0; gi < groupBoxes.length; gi++) {{
      if (skipGroupIndices.includes(gi)) continue;
      const gb = groupBoxes[gi];
      const pad = 4;
      const left = gb.x - pad, right = gb.x + gb.w + pad;
      const top = gb.y - pad, bottom = gb.y + gb.h + pad;
      const dx = x2 - x1, dy = y2 - y1;
      let tmin = 0, tmax = 1;
      const edges = [[-dx, x1 - left], [dx, right - x1], [-dy, y1 - top], [dy, bottom - y1]];
      let hit = true;
      for (const [p, q] of edges) {{
        if (Math.abs(p) < 0.001) {{ if (q < 0) {{ hit = false; break; }} }}
        else {{
          const t = q / p;
          if (p < 0) {{ if (t > tmin) tmin = t; }}
          else {{ if (t < tmax) tmax = t; }}
          if (tmin > tmax) {{ hit = false; break; }}
        }}
      }}
      if (hit && tmin < tmax) return true;
    }}
    return false;
  }}

  // Localiza o espaço entre grupos adjacentes (mesma linha)
  function findGapBetween(gi1, gi2) {{
    if (gi1 < 0 || gi2 < 0) return null;
    const g1 = groupBoxes[gi1], g2 = groupBoxes[gi2];
    // Mesma linha: os intervalos de Y se sobrepõem
    const yOverlap = g1.y < g2.y + g2.h && g2.y < g1.y + g1.h;
    if (!yOverlap) return null;
    // Espaço entre eles
    if (g1.x + g1.w < g2.x) return {{ x: (g1.x + g1.w + g2.x) / 2 }};
    if (g2.x + g2.w < g1.x) return {{ x: (g2.x + g2.w + g1.x) / 2 }};
    return null;
  }}

  // Cria um caminho ortogonal com cantos arredondados
  function buildOrthoPath(pts) {{
    let d = `M ${{pts[0].x}} ${{pts[0].y}}`;
    const radius = 6;
    for (let i = 1; i < pts.length - 1; i++) {{
      const prev = pts[i-1], curr = pts[i], next = pts[i+1];
      const dx1 = curr.x - prev.x, dy1 = curr.y - prev.y;
      const dx2 = next.x - curr.x, dy2 = next.y - curr.y;
      const len1 = Math.sqrt(dx1*dx1 + dy1*dy1);
      const len2 = Math.sqrt(dx2*dx2 + dy2*dy2);
      if (len1 < 1 || len2 < 1) {{ d += ` L ${{curr.x}} ${{curr.y}}`; continue; }}
      const r = Math.min(radius, len1/2, len2/2);
      const bx = curr.x - (dx1/len1)*r, by = curr.y - (dy1/len1)*r;
      const ax = curr.x + (dx2/len2)*r, ay = curr.y + (dy2/len2)*r;
      d += ` L ${{bx}} ${{by}} Q ${{curr.x}} ${{curr.y}} ${{ax}} ${{ay}}`;
    }}
    d += ` L ${{pts[pts.length-1].x}} ${{pts[pts.length-1].y}}`;
    return d;
  }}

  // Localiza o ponto de cruzamento entre dois segmentos ortogonais (somente H cruza V)
  function findSegCrossing(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2) {{
    const aIsH = Math.abs(ay1 - ay2) < 1;
    const bIsH = Math.abs(by1 - by2) < 1;
    if (aIsH === bIsH) return null;
    let hx1, hx2, hy, vx, vy1, vy2;
    if (aIsH) {{
      hy = ay1; hx1 = Math.min(ax1, ax2); hx2 = Math.max(ax1, ax2);
      vx = bx1; vy1 = Math.min(by1, by2); vy2 = Math.max(by1, by2);
    }} else {{
      hy = by1; hx1 = Math.min(bx1, bx2); hx2 = Math.max(bx1, bx2);
      vx = ax1; vy1 = Math.min(ay1, ay2); vy2 = Math.max(ay1, ay2);
    }}
    const MM = 2;
    if (vx > hx1 + MM && vx < hx2 - MM &&
        hy > vy1 + MM && hy < vy2 - MM) {{
      return {{ x: vx, y: hy }};
    }}
    return null;
  }}

  // Cria um caminho ortogonal com cantos arredondados E arcos de ponte nos cruzamentos
  function buildPathWithBridges(pts, bridges) {{
    const CR = 6, BR = 12;
    if (pts.length <= 1) return '';

    // Indexa as pontes por segmento e ordena na direção do percurso
    const bySeg = {{}};
    (bridges || []).forEach(b => {{
      if (!bySeg[b.segIdx]) bySeg[b.segIdx] = [];
      bySeg[b.segIdx].push(b);
    }});
    for (const si in bySeg) {{
      const i = parseInt(si);
      if (i >= pts.length - 1) continue;
      const p1 = pts[i], p2 = pts[i + 1];
      const isH = Math.abs(p1.y - p2.y) < 1;
      if (isH) {{
        const dir = Math.sign(p2.x - p1.x) || 1;
        bySeg[si].sort((a, b) => (a.x - b.x) * dir);
      }} else {{
        const dir = Math.sign(p2.y - p1.y) || 1;
        bySeg[si].sort((a, b) => (a.y - b.y) * dir);
      }}
    }}

    // Auxiliar: adiciona arcos de ponte a um segmento
    function appendBridges(d, segIdx, segP1, segP2) {{
      const segB = bySeg[segIdx] || [];
      if (segB.length === 0) return d;
      const isH = Math.abs(segP1.y - segP2.y) < 1;
      segB.forEach(b => {{
        if (isH) {{
          const dir = Math.sign(segP2.x - segP1.x) || 1;
          d += ` L ${{b.x - BR * dir}} ${{segP1.y}}`;
          d += ` A ${{BR}} ${{BR}} 0 0 ${{dir > 0 ? 1 : 0}} ${{b.x + BR * dir}} ${{segP1.y}}`;
        }} else {{
          const dir = Math.sign(segP2.y - segP1.y) || 1;
          d += ` L ${{segP1.x}} ${{b.y - BR * dir}}`;
          d += ` A ${{BR}} ${{BR}} 0 0 ${{dir > 0 ? 0 : 1}} ${{segP1.x}} ${{b.y + BR * dir}}`;
        }}
      }});
      return d;
    }}

    // Caminho de dois pontos (linha reta)
    if (pts.length === 2) {{
      let d = `M ${{pts[0].x}} ${{pts[0].y}}`;
      d = appendBridges(d, 0, pts[0], pts[1]);
      d += ` L ${{pts[1].x}} ${{pts[1].y}}`;
      return d;
    }}

    // Caminho de vários pontos com cantos e pontes
    let d = `M ${{pts[0].x}} ${{pts[0].y}}`;
    for (let i = 1; i < pts.length; i++) {{
      const prev = pts[i - 1], curr = pts[i];
      const isLast = (i === pts.length - 1);

      // Calcula o recorte do canto para pontos que não sejam o último
      let target = curr, cSuffix = '';
      if (!isLast) {{
        const next = pts[i + 1];
        const dx1 = curr.x - prev.x, dy1 = curr.y - prev.y;
        const dx2 = next.x - curr.x, dy2 = next.y - curr.y;
        const len1 = Math.sqrt(dx1 * dx1 + dy1 * dy1);
        const len2 = Math.sqrt(dx2 * dx2 + dy2 * dy2);
        if (len1 >= 1 && len2 >= 1) {{
          const r = Math.min(CR, len1 / 2, len2 / 2);
          const bx = curr.x - (dx1 / len1) * r;
          const by = curr.y - (dy1 / len1) * r;
          const ax = curr.x + (dx2 / len2) * r;
          const ay = curr.y + (dy2 / len2) * r;
          target = {{ x: bx, y: by }};
          cSuffix = ` Q ${{curr.x}} ${{curr.y}} ${{ax}} ${{ay}}`;
        }}
      }}

      // Desenha pontes no segmento (i-1) → i
      d = appendBridges(d, i - 1, prev, curr);

      // Linha até o destino e curva de canto opcional
      d += ` L ${{target.x}} ${{target.y}}${{cSuffix}}`;
    }}
    return d;
  }}

  // ── Desvio de obstáculos: roteia as arestas ao redor dos nós ──
  function segHitsNode(x1, y1, x2, y2, pos, nw, nh, margin) {{
    const nx1 = pos.x - margin, ny1 = pos.y - margin;
    const nx2 = pos.x + nw + margin, ny2 = pos.y + nh + margin;
    if (Math.abs(x1 - x2) < 1) {{
      // Segmento vertical
      const x = x1;
      const minY = Math.min(y1, y2), maxY = Math.max(y1, y2);
      return x > nx1 && x < nx2 && maxY > ny1 && minY < ny2;
    }} else {{
      // Segmento horizontal
      const y = y1;
      const minX = Math.min(x1, x2), maxX = Math.max(x1, x2);
      return y > ny1 && y < ny2 && maxX > nx1 && minX < nx2;
    }}
  }}

  function avoidNodes(pts, fromId, toId) {{
    const MARGIN = 25;
    const SECTION_MARGIN = 12;
    let points = pts.map(p => ({{...p}}));
    // Salva as âncoras originais, que NUNCA podem se mover (elas se conectam aos nós)
    const startAnchor = {{...points[0]}};
    const endAnchor = {{...points[points.length - 1]}};

    // Obstáculos de seção (groupBox): groupBoxes que não contêm NENHUMA extremidade.
    // Ignora o grupo de PE, pois arestas do tipo PE podem atravessá-lo legitimamente.
    const _fromGrp = _nodeGrp[fromId];
    const _toGrp = _nodeGrp[toId];
    const sectionObstacles = [];
    for (let gi = 0; gi < groupBoxes.length; gi++) {{
      if (gi === _fromGrp || gi === _toGrp) continue;
      const gb = groupBoxes[gi];
      if (gb.isPE) continue;
      sectionObstacles.push(gb);
    }}

    // Auxiliar: se a coordenada de desvio da seção cair dentro do retângulo da VNet
    // enquanto uma das extremidades estiver fora dela, move o desvio para além da
    // borda mais próxima, evitando atravessar o interior não relacionado da VNet.
    function _clampOutsideVNet(val, axis) {{
      if (!_vnetBounds) return val;
      const inAnchor = (a) => (a.x > _vnetBounds.x && a.x < _vnetBounds.x + _vnetBounds.w
                            && a.y > _vnetBounds.y && a.y < _vnetBounds.y + _vnetBounds.h);
      const srcOut = !inAnchor(startAnchor);
      const dstOut = !inAnchor(endAnchor);
      if (!srcOut && !dstOut) return val;
      if (axis === 'x') {{
        const L = _vnetBounds.x, R = _vnetBounds.x + _vnetBounds.w;
        if (val > L && val < R) return (val - L) <= (R - val) ? L - SECTION_MARGIN : R + SECTION_MARGIN;
      }} else {{
        const T = _vnetBounds.y, B = _vnetBounds.y + _vnetBounds.h;
        if (val > T && val < B) return (val - T) <= (B - val) ? T - SECTION_MARGIN : B + SECTION_MARGIN;
      }}
      return val;
    }}

    for (let iter = 0; iter < 20; iter++) {{
      let found = false;

      for (let i = 0; i < points.length - 1 && !found; i++) {{
        const p1 = points[i], p2 = points[i+1];

        // 1) Obstáculos de seção (maiores, verificados primeiro)
        for (const gb of sectionObstacles) {{
          const pos = {{x: gb.x, y: gb.y}};
          if (!segHitsNode(p1.x, p1.y, p2.x, p2.y, pos, gb.w, gb.h, SECTION_MARGIN)) continue;

          found = true;
          const isVert = Math.abs(p1.x - p2.x) < 1;
          const isFirst = (i === 0);
          const isLast = (i + 1 === points.length - 1);

          if (points.length <= 2) {{
            if (isVert) {{
              const leftX = gb.x - SECTION_MARGIN;
              const rightX = gb.x + gb.w + SECTION_MARGIN;
              let detourX = Math.abs(p1.x - leftX) <= Math.abs(p1.x - rightX) ? leftX : rightX;
              detourX = _clampOutsideVNet(detourX, 'x');
              points = [points[0], {{x: detourX, y: p1.y}}, {{x: detourX, y: p2.y}}, points[points.length-1]];
            }} else {{
              const topY = gb.y - SECTION_MARGIN;
              const bottomY = gb.y + gb.h + SECTION_MARGIN;
              let detourY = Math.abs(p1.y - topY) <= Math.abs(p1.y - bottomY) ? topY : bottomY;
              detourY = _clampOutsideVNet(detourY, 'y');
              points = [points[0], {{x: p1.x, y: detourY}}, {{x: p2.x, y: detourY}}, points[points.length-1]];
            }}
          }} else if (isFirst) {{
            if (isVert) {{
              const leftX = gb.x - SECTION_MARGIN;
              const rightX = gb.x + gb.w + SECTION_MARGIN;
              let detourX = Math.abs(p1.x - leftX) <= Math.abs(p1.x - rightX) ? leftX : rightX;
              detourX = _clampOutsideVNet(detourX, 'x');
              points.splice(1, 0, {{x: p1.x, y: p1.y}}, {{x: detourX, y: p1.y}});
              points[3] = {{x: detourX, y: p2.y}};
            }} else {{
              const topY = gb.y - SECTION_MARGIN;
              const bottomY = gb.y + gb.h + SECTION_MARGIN;
              let detourY = Math.abs(p1.y - topY) <= Math.abs(p1.y - bottomY) ? topY : bottomY;
              detourY = _clampOutsideVNet(detourY, 'y');
              points.splice(1, 0, {{x: p1.x, y: detourY}});
              points[2] = {{x: p2.x, y: detourY}};
            }}
          }} else if (isLast) {{
            if (isVert) {{
              const leftX = gb.x - SECTION_MARGIN;
              const rightX = gb.x + gb.w + SECTION_MARGIN;
              let detourX = Math.abs(p1.x - leftX) <= Math.abs(p1.x - rightX) ? leftX : rightX;
              detourX = _clampOutsideVNet(detourX, 'x');
              points[i] = {{x: detourX, y: p1.y}};
              points.splice(i + 1, 0, {{x: detourX, y: p2.y}}, {{x: p2.x, y: p2.y}});
            }} else {{
              const topY = gb.y - SECTION_MARGIN;
              const bottomY = gb.y + gb.h + SECTION_MARGIN;
              let detourY = Math.abs(p1.y - topY) <= Math.abs(p1.y - bottomY) ? topY : bottomY;
              detourY = _clampOutsideVNet(detourY, 'y');
              points[i] = {{x: p1.x, y: detourY}};
              points.splice(i + 1, 0, {{x: p2.x, y: detourY}});
            }}
          }} else {{
            if (isVert) {{
              const leftX = gb.x - SECTION_MARGIN;
              const rightX = gb.x + gb.w + SECTION_MARGIN;
              let newX = Math.abs(p1.x - leftX) <= Math.abs(p1.x - rightX) ? leftX : rightX;
              newX = _clampOutsideVNet(newX, 'x');
              points[i] = {{ x: newX, y: p1.y }};
              points[i+1] = {{ x: newX, y: p2.y }};
            }} else {{
              const topY = gb.y - SECTION_MARGIN;
              const bottomY = gb.y + gb.h + SECTION_MARGIN;
              let newY = Math.abs(p1.y - topY) <= Math.abs(p1.y - bottomY) ? topY : bottomY;
              newY = _clampOutsideVNet(newY, 'y');
              points[i] = {{ x: p1.x, y: newY }};
              points[i+1] = {{ x: p2.x, y: newY }};
            }}
          }}
          break;
        }}
        if (found) break;

        // 2) Obstáculos de nós de serviço
        for (const node of NODES) {{
          if (node.id === fromId || node.id === toId) continue;
          const pos = positions[node.id];
          if (!pos) continue;
          const nw = node.type === 'pe' ? PE_W : SVC_W;
          const nh = (node.type === 'pe' ? PE_H : SVC_H) + 20; // inclui o texto abaixo da caixa

          if (!segHitsNode(p1.x, p1.y, p2.x, p2.y, pos, nw, nh, MARGIN)) continue;

          found = true;
          const isVert = Math.abs(p1.x - p2.x) < 1;
          const isFirst = (i === 0);
          const isLast = (i + 1 === points.length - 1);

          if (points.length <= 2) {{
            // Linha reta atingindo um nó: converte em desvio de quatro pontos (âncoras preservadas)
            if (isVert) {{
              const leftX = pos.x - MARGIN;
              const rightX = pos.x + nw + MARGIN;
              const detourX = Math.abs(p1.x - leftX) <= Math.abs(p1.x - rightX) ? leftX : rightX;
              points = [points[0], {{x: detourX, y: p1.y}}, {{x: detourX, y: p2.y}}, points[points.length-1]];
            }} else {{
              const topY = pos.y - MARGIN;
              const bottomY = pos.y + nh + MARGIN;
              const detourY = Math.abs(p1.y - topY) <= Math.abs(p1.y - bottomY) ? topY : bottomY;
              points = [points[0], {{x: p1.x, y: detourY}}, {{x: p2.x, y: detourY}}, points[points.length-1]];
            }}
          }} else if (isFirst) {{
            // O primeiro segmento colide: mantém points[0] (âncora) e insere o desvio depois
            if (isVert) {{
              const leftX = pos.x - MARGIN;
              const rightX = pos.x + nw + MARGIN;
              const detourX = Math.abs(p1.x - leftX) <= Math.abs(p1.x - rightX) ? leftX : rightX;
              points.splice(1, 0, {{x: p1.x, y: p1.y}}, {{x: detourX, y: p1.y}});
              points[3] = {{x: detourX, y: p2.y}};
            }} else {{
              const topY = pos.y - MARGIN;
              const bottomY = pos.y + nh + MARGIN;
              const detourY = Math.abs(p1.y - topY) <= Math.abs(p1.y - bottomY) ? topY : bottomY;
              points.splice(1, 0, {{x: p1.x, y: detourY}});
              points[2] = {{x: p2.x, y: detourY}};
            }}
          }} else if (isLast) {{
            // O último segmento colide: mantém o último ponto (âncora) e insere o desvio antes
            if (isVert) {{
              const leftX = pos.x - MARGIN;
              const rightX = pos.x + nw + MARGIN;
              const detourX = Math.abs(p1.x - leftX) <= Math.abs(p1.x - rightX) ? leftX : rightX;
              points[i] = {{x: detourX, y: p1.y}};
              points.splice(i + 1, 0, {{x: detourX, y: p2.y}}, {{x: p2.x, y: p2.y}});
            }} else {{
              const topY = pos.y - MARGIN;
              const bottomY = pos.y + nh + MARGIN;
              const detourY = Math.abs(p1.y - topY) <= Math.abs(p1.y - bottomY) ? topY : bottomY;
              points[i] = {{x: p1.x, y: detourY}};
              points.splice(i + 1, 0, {{x: p2.x, y: detourY}});
            }}
          }} else {{
            // Segmento intermediário: é seguro mover as duas extremidades
            if (isVert) {{
              const leftX = pos.x - MARGIN;
              const rightX = pos.x + nw + MARGIN;
              const newX = Math.abs(p1.x - leftX) <= Math.abs(p1.x - rightX) ? leftX : rightX;
              points[i] = {{ x: newX, y: p1.y }};
              points[i+1] = {{ x: newX, y: p2.y }};
            }} else {{
              const topY = pos.y - MARGIN;
              const bottomY = pos.y + nh + MARGIN;
              const newY = Math.abs(p1.y - topY) <= Math.abs(p1.y - bottomY) ? topY : bottomY;
              points[i] = {{ x: p1.x, y: newY }};
              points[i+1] = {{ x: p2.x, y: newY }};
            }}
          }}
          break;
        }}
      }}

      if (!found) break;
    }}

    // Restaura as âncoras para garantir que as linhas sempre toquem os nós de origem/destino
    points[0] = startAnchor;
    points[points.length - 1] = endAnchor;

    return points;
  }}

  // ── Arestas: renderização em três fases ──
  // Fase 0: pré-analisa os lados de saída → Fase 1: calcula caminhos com âncoras deslocadas
  // Fase 2: detecta cruzamentos → Fase 3: renderiza com arcos de ponte
  const _edgeLabels = [];

  // FASE 0: pré-análise para contar quantas arestas saem de cada lado de cada nó
  const _sideTotal = {{}};
  const _edgeSides = [];
  EDGES.forEach(edge => {{
    const fn = NODES.find(n => n.id === edge.from);
    const tn = NODES.find(n => n.id === edge.to);
    if (!fn || !tn) {{ _edgeSides.push(null); return; }}
    const fromBox = getNodeBox(fn);
    const toBox = getNodeBox(tn);
    if (!fromBox || !toBox) {{ _edgeSides.push(null); return; }}

    const isPeEdge = edge.type === 'private';
    let exitSide, entrySide;
    if (isPeEdge) {{
      exitSide = 'bottom'; entrySide = 'top';
    }} else {{
      const dx = toBox.cx - fromBox.cx;
      const dy = toBox.cy - fromBox.cy;
      if (Math.abs(dx) >= Math.abs(dy)) {{
        exitSide = dx >= 0 ? 'right' : 'left';
        entrySide = dx >= 0 ? 'left' : 'right';
      }} else {{
        exitSide = dy >= 0 ? 'bottom' : 'top';
        entrySide = dy >= 0 ? 'top' : 'bottom';
      }}
    }}
    const ek = `${{edge.from}}_${{exitSide}}`;
    const nk = `${{edge.to}}_${{entrySide}}`;
    _sideTotal[ek] = (_sideTotal[ek] || 0) + 1;
    _sideTotal[nk] = (_sideTotal[nk] || 0) + 1;
    _edgeSides.push({{ exitSide, entrySide, isPeEdge, fromBox, toBox, edge }});
  }});

  // ── ORGANIZAÇÃO DAS CONEXÕES: cria o mapa de canais para agrupar arestas entre grupos ──
  // Etapa 1: mapeia cada nó para a caixa de grupo que o contém
  const _nodeGrp = {{}};
  NODES.forEach(n => {{
    const pos = positions[n.id];
    if (!pos) return;
    const nw = n.type === 'pe' ? PE_W : SVC_W;
    const nh = n.type === 'pe' ? PE_H : SVC_H;
    const cx = pos.x + nw / 2, cy = pos.y + nh / 2;
    for (let gi = 0; gi < groupBoxes.length; gi++) {{
      const gb = groupBoxes[gi];
      if (cx >= gb.x && cx <= gb.x + gb.w && cy >= gb.y && cy <= gb.y + gb.h) {{
        _nodeGrp[n.id] = gi; break;
      }}
    }}
  }});

  // Etapa 2: identifica canais entre pares de grupos e atribui deslocamentos de posição
  const _chMap = {{}};       // chave → {{ axis:'y'|'x', value: número }}
  const _chEdges = {{}};     // chave → [edgeIdx, ...]
  _edgeSides.forEach((info, idx) => {{
    if (!info || info.isPeEdge) return;
    const sg = _nodeGrp[info.edge.from], tg = _nodeGrp[info.edge.to];
    if (sg === undefined || tg === undefined) return;

    let key;
    if (sg !== tg) {{
      key = Math.min(sg, tg) + '_' + Math.max(sg, tg);
      if (!_chEdges[key]) _chEdges[key] = [];
      _chEdges[key].push(idx);
      if (!_chMap[key]) {{
        const a = groupBoxes[sg], b = groupBoxes[tg];
        if (a.y + a.h <= b.y)      _chMap[key] = {{ axis: 'y', value: (a.y + a.h + b.y) / 2 }};
        else if (b.y + b.h <= a.y) _chMap[key] = {{ axis: 'y', value: (b.y + b.h + a.y) / 2 }};
        else if (a.x + a.w <= b.x) _chMap[key] = {{ axis: 'x', value: (a.x + a.w + b.x) / 2 }};
        else if (b.x + b.w <= a.x) _chMap[key] = {{ axis: 'x', value: (b.x + b.w + a.x) / 2 }};
      }}
    }} else {{
      // Arestas internas ao grupo: agrupa por direção para atribuir deslocamentos
      const dir = (info.exitSide === 'bottom' || info.exitSide === 'top') ? 'v' : 'h';
      key = 'i' + sg + dir;
      if (!_chEdges[key]) _chEdges[key] = [];
      _chEdges[key].push(idx);
      // Sem valor fixo de canal: cada aresta usa seu próprio ponto médio e deslocamento
    }}
  }});

  // Etapa 3: ordena as arestas em cada canal e atribui deslocamentos
  const _chOff = {{}};  // edgeIdx → deslocamento em px
  const _CH_SLOT = 18;  // espaçamento entre linhas de um agrupamento
  Object.keys(_chEdges).forEach(key => {{
    const ch = _chMap[key];
    const arr = _chEdges[key];
    const isVert = ch ? ch.axis === 'y' : key.endsWith('v');
    arr.sort((a, b) => {{
      const ia = _edgeSides[a], ib = _edgeSides[b];
      if (isVert) return (ia.fromBox.cx + ia.toBox.cx) - (ib.fromBox.cx + ib.toBox.cx);
      return (ia.fromBox.cy + ia.toBox.cy) - (ib.fromBox.cy + ib.toBox.cy);
    }});
    const n = arr.length;
    arr.forEach((ei, slot) => {{
      _chOff[ei] = n > 1 ? (slot - (n - 1) / 2) * _CH_SLOT : 0;
    }});
  }});

  // Saída deslocada da borda: distribui várias arestas uniformemente pelo lado do nó
  const _sideUsed = {{}};
  function staggeredExit(nodeId, box, side) {{
    const key = `${{nodeId}}_${{side}}`;
    const total = _sideTotal[key] || 1;
    const idx = _sideUsed[key] || 0;
    _sideUsed[key] = idx + 1;
    const isH = (side === 'top' || side === 'bottom');
    const sideLen = isH ? box.w : box.h;
    const CM = Math.max(40, sideLen * 0.3); // margem do canto: no mínimo 40 px ou 30% do lado
    const usable = Math.max(0, sideLen - 2 * CM);
    const maxSpread = Math.min(usable, total * 14);
    const step = total > 1 ? maxSpread / (total - 1) : 0;
    const offset = total > 1 ? -maxSpread / 2 + idx * step : 0;
    if (side === 'top') return {{ x: Math.max(box.x + CM, Math.min(box.x + box.w - CM, box.cx + offset)), y: box.y }};
    if (side === 'bottom') return {{ x: Math.max(box.x + CM, Math.min(box.x + box.w - CM, box.cx + offset)), y: box.y + box.h }};
    if (side === 'left') return {{ x: box.x, y: Math.max(box.y + CM, Math.min(box.y + box.h - CM, box.cy + offset)) }};
    return {{ x: box.x + box.w, y: Math.max(box.y + CM, Math.min(box.y + box.h - CM, box.cy + offset)) }};
  }}

  // FASE 1: calcula os caminhos das arestas com âncoras deslocadas
  const _allEdgePaths = [];
  _edgeSides.forEach((info, idx) => {{
    if (!info) return;
    const {{ exitSide, entrySide, isPeEdge, fromBox, toBox, edge }} = info;
    let pts;

    if (isPeEdge) {{
      const sp = staggeredExit(edge.from, fromBox, 'bottom');
      const ep = staggeredExit(edge.to, toBox, 'top');
      if (Math.abs(sp.x - ep.x) < 8) {{
        pts = [sp, ep];
      }} else {{
        let midY = (sp.y + ep.y) / 2;
        midY = Math.max(midY, fromBox.y + fromBox.h + 40);
        midY = Math.min(midY, toBox.y - 40);
        pts = [sp, {{x: sp.x, y: midY}}, {{x: ep.x, y: midY}}, ep];
      }}
      pts = avoidNodes(pts, edge.from, edge.to);
    }} else {{
      const sp = staggeredExit(edge.from, fromBox, exitSide);
      const ep = staggeredExit(edge.to, toBox, entrySide);
      const STUB = 40;

      // Consulta o canal para organizar arestas entre grupos
      const _sg = _nodeGrp[edge.from], _tg = _nodeGrp[edge.to];
      const _ck = _sg !== undefined && _tg !== undefined && _sg !== _tg
        ? Math.min(_sg, _tg) + '_' + Math.max(_sg, _tg) : null;
      const _cc = _ck ? _chMap[_ck] : null;
      const _co = _chOff[idx] || 0;

      if (exitSide === 'right' || exitSide === 'left') {{
        if (Math.abs(sp.y - ep.y) < 8) {{
          pts = [sp, ep];
        }} else {{
          let midX = (_cc && _cc.axis === 'x') ? _cc.value + _co : (sp.x + ep.x) / 2 + _co;
          if (exitSide === 'right') midX = Math.max(midX, fromBox.x + fromBox.w + STUB);
          if (exitSide === 'left') midX = Math.min(midX, fromBox.x - STUB);
          if (entrySide === 'right') midX = Math.max(midX, toBox.x + toBox.w + STUB);
          if (entrySide === 'left') midX = Math.min(midX, toBox.x - STUB);
          pts = [sp, {{x: midX, y: sp.y}}, {{x: midX, y: ep.y}}, ep];
        }}
      }} else {{
        if (Math.abs(sp.x - ep.x) < 8) {{
          pts = [sp, ep];
        }} else {{
          let midY = (_cc && _cc.axis === 'y') ? _cc.value + _co : (sp.y + ep.y) / 2 + _co;
          if (exitSide === 'bottom') midY = Math.max(midY, fromBox.y + fromBox.h + STUB);
          if (exitSide === 'top') midY = Math.min(midY, fromBox.y - STUB);
          if (entrySide === 'bottom') midY = Math.max(midY, toBox.y + toBox.h + STUB);
          if (entrySide === 'top') midY = Math.min(midY, toBox.y - STUB);
          pts = [sp, {{x: sp.x, y: midY}}, {{x: ep.x, y: midY}}, ep];
        }}
      }}

      pts = avoidNodes(pts, edge.from, edge.to);
    }}

    // APÓS O ROTEAMENTO: força um segmento perpendicular nas extremidades de saída e entrada
    // Três casos: (a) já ortogonal e longo o bastante → ignora
    //             (b) ortogonal, mas curto → estende o ponto de curva existente
    //             (c) não ortogonal → insere um conector de dois pontos
    const _eSide = isPeEdge ? 'bottom' : exitSide;
    const _nSide = isPeEdge ? 'top' : entrySide;
    const _STUB = 40;
    if (pts.length >= 3) {{
      // --- Extremidade de SAÍDA ---
      const _p0 = pts[0], _p1 = pts[1];
      const _eH = (_eSide === 'right' || _eSide === 'left');
      if (_eH) {{
        const _d = _eSide === 'right' ? 1 : -1;
        const _ortho = Math.abs(_p0.y - _p1.y) <= 1;
        if (_ortho) {{
          const _dist = (_p1.x - _p0.x) * _d;
          if (_dist < _STUB) {{
            const sx = _p0.x + _d * _STUB;
            pts[1] = {{x: sx, y: _p0.y}};
            if (pts.length > 2 && Math.abs(pts[2].x - _p1.x) <= 1) {{
              pts[2] = {{x: sx, y: pts[2].y}};
            }}
          }}
        }} else {{
          const sx = _p0.x + _d * _STUB;
          pts.splice(1, 0, {{x: sx, y: _p0.y}}, {{x: sx, y: _p1.y}});
        }}
      }} else {{
        const _d = _eSide === 'bottom' ? 1 : -1;
        const _ortho = Math.abs(_p0.x - _p1.x) <= 1;
        if (_ortho) {{
          const _dist = (_p1.y - _p0.y) * _d;
          if (_dist < _STUB) {{
            const sy = _p0.y + _d * _STUB;
            pts[1] = {{x: _p0.x, y: sy}};
            if (pts.length > 2 && Math.abs(pts[2].y - _p1.y) <= 1) {{
              pts[2] = {{x: pts[2].x, y: sy}};
            }}
          }}
        }} else {{
          const sy = _p0.y + _d * _STUB;
          pts.splice(1, 0, {{x: _p0.x, y: sy}}, {{x: _p1.x, y: sy}});
        }}
      }}
      // --- Extremidade de ENTRADA ---
      const _pN = pts[pts.length - 1], _pP = pts[pts.length - 2];
      const _nH = (_nSide === 'right' || _nSide === 'left');
      if (_nH) {{
        const _d = _nSide === 'left' ? -1 : 1;
        const _ortho = Math.abs(_pN.y - _pP.y) <= 1;
        if (_ortho) {{
          const _dist = (_pP.x - _pN.x) * _d;
          if (_dist < _STUB) {{
            const sx = _pN.x + _d * _STUB;
            const _idx = pts.length - 2;
            pts[_idx] = {{x: sx, y: _pN.y}};
            if (_idx > 0 && Math.abs(pts[_idx - 1].x - _pP.x) <= 1) {{
              pts[_idx - 1] = {{x: sx, y: pts[_idx - 1].y}};
            }}
          }}
        }} else {{
          const sx = _pN.x + _d * _STUB;
          pts.splice(pts.length - 1, 0, {{x: sx, y: _pP.y}}, {{x: sx, y: _pN.y}});
        }}
      }} else {{
        const _d = _nSide === 'top' ? -1 : 1;
        const _ortho = Math.abs(_pN.x - _pP.x) <= 1;
        if (_ortho) {{
          const _dist = (_pP.y - _pN.y) * _d;
          if (_dist < _STUB) {{
            const sy = _pN.y + _d * _STUB;
            const _idx = pts.length - 2;
            pts[_idx] = {{x: _pN.x, y: sy}};
            if (_idx > 0 && Math.abs(pts[_idx - 1].y - _pP.y) <= 1) {{
              pts[_idx - 1] = {{x: pts[_idx - 1].x, y: sy}};
            }}
          }}
        }} else {{
          const sy = _pN.y + _d * _STUB;
          pts.splice(pts.length - 1, 0, {{x: _pP.x, y: sy}}, {{x: _pN.x, y: sy}});
        }}
      }}
    }}

    // SEGURANÇA: divide os segmentos diagonais restantes em formas de L ortogonais
    for (let _i = 0; _i < pts.length - 1; _i++) {{
      const _a = pts[_i], _b = pts[_i + 1];
      if (Math.abs(_a.x - _b.x) > 1 && Math.abs(_a.y - _b.y) > 1) {{
        pts.splice(_i + 1, 0, {{x: _a.x, y: _b.y}});
      }}
    }}

    // SIMPLIFICAÇÃO: remove pontos intermediários duplicados e colineares
    for (let _i = pts.length - 2; _i >= 1; _i--) {{
      const _a = pts[_i - 1], _b = pts[_i], _c = pts[_i + 1];
      if (Math.abs(_a.x - _b.x) <= 1 && Math.abs(_a.y - _b.y) <= 1) {{
        pts.splice(_i, 1); continue;
      }}
      if ((Math.abs(_a.x - _b.x) <= 1 && Math.abs(_b.x - _c.x) <= 1) ||
          (Math.abs(_a.y - _b.y) <= 1 && Math.abs(_b.y - _c.y) <= 1)) {{
        pts.splice(_i, 1);
      }}
    }}

    _allEdgePaths.push({{ edge, pts, isPeEdge }});
  }});

  // SEPARAÇÃO DE SOBREPOSIÇÕES: afasta segmentos colineares sobrepostos
  // Separa somente segmentos mais próximos que OSEP; arestas pré-organizadas (a 16 px) não mudam
  const OSEP = 8;
  for (let pass = 0; pass < 4; pass++) {{
    for (let i = 0; i < _allEdgePaths.length; i++) {{
      for (let j = i + 1; j < _allEdgePaths.length; j++) {{
        const pA = _allEdgePaths[i].pts;
        const pB = _allEdgePaths[j].pts;
        const dir = (j % 2 === 0) ? 1 : -1;
        for (let si = 0; si < pA.length - 1; si++) {{
          for (let sj = 0; sj < pB.length - 1; sj++) {{
            const a1 = pA[si], a2 = pA[si + 1];
            const b1 = pB[sj], b2 = pB[sj + 1];
            const aV = Math.abs(a1.x - a2.x) < 2;
            const bV = Math.abs(b1.x - b2.x) < 2;
            const aH = Math.abs(a1.y - a2.y) < 2;
            const bH = Math.abs(b1.y - b2.y) < 2;

            if (aV && bV && Math.abs(a1.x - b1.x) < OSEP) {{
              const ov = Math.min(Math.max(a1.y, a2.y), Math.max(b1.y, b2.y))
                       - Math.max(Math.min(a1.y, a2.y), Math.min(b1.y, b2.y));
              if (ov > 10) {{
                let shift = OSEP * dir;
                if (b1.x + shift < 20) shift = Math.abs(shift);
                if (sj > 0) pB[sj] = {{ x: b1.x + shift, y: b1.y }};
                if (sj + 1 < pB.length - 1) pB[sj + 1] = {{ x: b2.x + shift, y: b2.y }};
              }}
            }}
            if (aH && bH && Math.abs(a1.y - b1.y) < OSEP) {{
              const ov = Math.min(Math.max(a1.x, a2.x), Math.max(b1.x, b2.x))
                       - Math.max(Math.min(a1.x, a2.x), Math.min(b1.x, b2.x));
              if (ov > 10) {{
                const shift = OSEP * dir;
                if (sj > 0) pB[sj] = {{ x: b1.x, y: b1.y + shift }};
                if (sj + 1 < pB.length - 1) pB[sj + 1] = {{ x: b2.x, y: b2.y + shift }};
              }}
            }}
          }}
        }}
      }}
    }}
  }}

  // ORTOGONALIZAÇÃO FINAL: corrige diagonais introduzidas pela separação de sobreposições
  _allEdgePaths.forEach(({{ pts }}) => {{
    for (let _i = 0; _i < pts.length - 1; _i++) {{
      const _a = pts[_i], _b = pts[_i + 1];
      if (Math.abs(_a.x - _b.x) > 1 && Math.abs(_a.y - _b.y) > 1) {{
        pts.splice(_i + 1, 0, {{x: _a.x, y: _b.y}});
      }}
    }}
    // Remove pontos colineares
    for (let _i = pts.length - 2; _i >= 1; _i--) {{
      const _a = pts[_i - 1], _b = pts[_i], _c = pts[_i + 1];
      if (Math.abs(_a.x - _b.x) <= 1 && Math.abs(_a.y - _b.y) <= 1) {{
        pts.splice(_i, 1); continue;
      }}
      if ((Math.abs(_a.x - _b.x) <= 1 && Math.abs(_b.x - _c.x) <= 1) ||
          (Math.abs(_a.y - _b.y) <= 1 && Math.abs(_b.y - _c.y) <= 1)) {{
        pts.splice(_i, 1);
      }}
    }}
  }});

  // ── ETAPA DE NOVO ROTEAMENTO: minimiza cruzamentos pelas margens externas ──
  // Em vez do caminho mais curto, redireciona as arestas que se cruzam AO REDOR das caixas
  const _gbLeft = groupBoxes.length > 0 ? Math.min(...groupBoxes.map(g => g.x)) : 0;
  const _gbRight = groupBoxes.length > 0 ? Math.max(...groupBoxes.map(g => g.x + g.w)) : 800;
  const _gbTop = groupBoxes.length > 0 ? Math.min(...groupBoxes.map(g => g.y)) : 0;
  const _gbBottom = groupBoxes.length > 0 ? Math.max(...groupBoxes.map(g => g.y + g.h)) : 600;
  const _RMARGIN = 50; // margem fora dos limites do grupo para arestas redirecionadas
  const _RM_SLOT = 14; // espaçamento entre arestas redirecionadas na mesma margem

  // Conta os cruzamentos H×V entre uma aresta e todas as outras
  function _cntCross(eIdx) {{
    let c = 0;
    const pA = _allEdgePaths[eIdx].pts;
    for (let j = 0; j < _allEdgePaths.length; j++) {{
      if (j === eIdx) continue;
      const pB = _allEdgePaths[j].pts;
      for (let si = 0; si < pA.length - 1; si++) {{
        for (let sj = 0; sj < pB.length - 1; sj++) {{
          if (findSegCrossing(pA[si].x, pA[si].y, pA[si+1].x, pA[si+1].y,
                              pB[sj].x, pB[sj].y, pB[sj+1].x, pB[sj+1].y)) c++;
        }}
      }}
    }}
    return c;
  }}

  // Gera uma rota pela margem: sp → segmento → margem → margem → segmento → ep
  function _mRoute(sp, ep, exitSide, entrySide, side, slotOff) {{
    const S = 40; // comprimento do segmento
    const so = slotOff || 0;
    // segmento de saída do nó de origem
    const s1 = exitSide === 'bottom' ? {{x: sp.x, y: sp.y + S}}
             : exitSide === 'top'    ? {{x: sp.x, y: sp.y - S}}
             : exitSide === 'right'  ? {{x: sp.x + S, y: sp.y}}
             :                         {{x: sp.x - S, y: sp.y}};
    // segmento de entrada no nó de destino
    const s2 = entrySide === 'top'    ? {{x: ep.x, y: ep.y - S}}
             : entrySide === 'bottom' ? {{x: ep.x, y: ep.y + S}}
             : entrySide === 'left'   ? {{x: ep.x - S, y: ep.y}}
             :                          {{x: ep.x + S, y: ep.y}};
    if (side === 'left') {{
      const mx = _gbLeft - _RMARGIN - so;
      return [sp, s1, {{x: mx, y: s1.y}}, {{x: mx, y: s2.y}}, s2, ep];
    }}
    if (side === 'right') {{
      const mx = _gbRight + _RMARGIN + so;
      return [sp, s1, {{x: mx, y: s1.y}}, {{x: mx, y: s2.y}}, s2, ep];
    }}
    if (side === 'top') {{
      const my = _gbTop - _RMARGIN - so;
      return [sp, s1, {{x: s1.x, y: my}}, {{x: s2.x, y: my}}, s2, ep];
    }}
    // inferior
    const my = _gbBottom + _RMARGIN + so;
    return [sp, s1, {{x: s1.x, y: my}}, {{x: s2.x, y: my}}, s2, ep];
  }}

  // Redireciona iterativamente, pelas margens, as arestas com cruzamentos
  const _marginUsed = {{ left: 0, right: 0, top: 0, bottom: 0 }};
  const _tried = new Set();
  for (let _ri = 0; _ri < 30; _ri++) {{
    // Localiza a aresta ainda não testada com mais cruzamentos
    let worstIdx = -1, worstCnt = 0;
    for (let i = 0; i < _allEdgePaths.length; i++) {{
      if (_allEdgePaths[i].isPeEdge || _tried.has(i)) continue;
      const cnt = _cntCross(i);
      if (cnt > worstCnt) {{ worstCnt = cnt; worstIdx = i; }}
    }}
    if (worstIdx < 0 || worstCnt === 0) break;

    const ei = _edgeSides[worstIdx];
    if (!ei) {{ _tried.add(worstIdx); continue; }}
    const origPts = _allEdgePaths[worstIdx].pts;
    const sp = origPts[0];
    const ep = origPts[origPts.length - 1];
    let bestPts = origPts, bestCnt = worstCnt, bestSide = null;

    // Calcula a largura do intervalo em cada margem para atribuir a profundidade adequada
    for (const side of ['left', 'right', 'top', 'bottom']) {{
      const alt = _mRoute(sp, ep, ei.exitSide, ei.entrySide, side, _marginUsed[side]);
      _allEdgePaths[worstIdx].pts = alt;
      const cnt = _cntCross(worstIdx);
      _allEdgePaths[worstIdx].pts = origPts;
      if (cnt < bestCnt) {{
        bestCnt = cnt; bestPts = alt; bestSide = side;
      }}
    }}

    if (bestSide && bestCnt < worstCnt) {{
      _allEdgePaths[worstIdx].pts = bestPts;
      _marginUsed[bestSide] += _RM_SLOT;
    }} else {{
      _tried.add(worstIdx); // marca como impossível de melhorar e tenta a próxima aresta
    }}
  }}

  // APÓS O NOVO ROTEAMENTO: ordena arestas na mesma margem pela largura (mais larga = mais externa)
  // Evita cruzamentos de segmentos verticais entre arestas no mesmo lado da margem
  const _marginEdges = {{ left: [], right: [], top: [], bottom: [] }};
  for (let i = 0; i < _allEdgePaths.length; i++) {{
    const pts = _allEdgePaths[i].pts;
    if (pts.length !== 6) continue; // somente arestas roteadas pela margem têm seis pontos
    // Detecta qual lado da margem esta aresta usa
    const p2 = pts[2], p3 = pts[3];
    if (p2.y === p3.y) {{
      // segmento horizontal na margem → superior ou inferior
      if (p2.y < _gbTop) {{ _marginEdges.top.push(i); }}
      else if (p2.y > _gbBottom) {{ _marginEdges.bottom.push(i); }}
    }} else if (p2.x === p3.x) {{
      // segmento vertical na margem → esquerda ou direita
      if (p2.x < _gbLeft) {{ _marginEdges.left.push(i); }}
      else if (p2.x > _gbRight) {{ _marginEdges.right.push(i); }}
    }}
  }}
  // Ordena cada grupo de margem: maior intervalo → posição mais externa
  for (const side of ['left', 'right', 'top', 'bottom']) {{
    const idxs = _marginEdges[side];
    if (idxs.length < 2) continue;
    const isHoriz = (side === 'top' || side === 'bottom');
    // Calcula o intervalo de cada aresta
    const spans = idxs.map(i => {{
      const pts = _allEdgePaths[i].pts;
      return isHoriz
        ? Math.abs(pts[2].x - pts[3].x)
        : Math.abs(pts[2].y - pts[3].y);
    }});
    // Ordena os índices pelo intervalo decrescente (mais largo primeiro → mais externo)
    const sorted = idxs.map((idx, j) => ({{ idx, span: spans[j] }}))
                       .sort((a, b) => b.span - a.span);
    // Reatribui as posições y/x das arestas ordenadas
    const baseMargin = isHoriz
      ? (side === 'top' ? _gbTop - _RMARGIN : _gbBottom + _RMARGIN)
      : (side === 'left' ? _gbLeft - _RMARGIN : _gbRight + _RMARGIN);
    const dir = (side === 'top' || side === 'left') ? -1 : 1;
    sorted.forEach((s, k) => {{
      const pts = _allEdgePaths[s.idx].pts;
      const newM = baseMargin + dir * k * _RM_SLOT;
      if (isHoriz) {{
        pts[2].y = newM; pts[3].y = newM;
      }} else {{
        pts[2].x = newM; pts[3].x = newM;
      }}
    }});
  }}

  // REDIRECIONADOR DE FAIXAS INFERIORES: abordagem organizada em forma de U
  // Redireciona arestas sobrepostas por faixas horizontais uniformes abaixo de todas as seções.
  // Desce verticalmente do nó quando possível (duas curvas); desloca somente quando bloqueado (quatro curvas).
  const OSEP2 = 14;
  const _bottomLaneBase = _gbBottom + _RMARGIN + 30;
  let _bottomSlot = 0;
  const _LANE_SPC = OSEP2; // espaçamento de 14 px entre faixas para um visual organizado
  const _COL_SPC = OSEP2; // distância mínima entre corredores verticais
  const _rerouted = new Set();
  const _usedCols = [];
  function _colUsed(cx) {{ for (const ux of _usedCols) {{ if (Math.abs(cx - ux) < _COL_SPC) return true; }} return false; }}
  // Verifica se a coluna vertical está livre de nós e caixas de seção não isentas
  function _isColClear(cx, yMin, yMax, skipId1, skipId2, skipGbs) {{
    for (const _nd of NODES) {{
      if (_nd.id === skipId1 || _nd.id === skipId2) continue;
      const _np = positions[_nd.id]; if (!_np) continue;
      const _nw = _nd.type === 'pe' ? PE_W : SVC_W;
      const _nh = (_nd.type === 'pe' ? PE_H : SVC_H) + 20;
      const _pad = 6;
      if (cx > _np.x - _pad && cx < _np.x + _nw + _pad &&
          yMin < _np.y + _nh + _pad && yMax > _np.y - _pad) {{
        return false;
      }}
    }}
    for (const _gb of groupBoxes) {{
      if (skipGbs && skipGbs.indexOf(_gb) >= 0) continue;
      if (cx > _gb.x - 4 && cx < _gb.x + _gb.w + 4 &&
          yMin < _gb.y + _gb.h + 4 && yMax > _gb.y - 4) {{
        return false;
      }}
    }}
    return true;
  }}
  // Verifica se a linha horizontal está livre de nós e caixas de seção não isentas
  function _isRowClear(cy, xMin, xMax, skipId1, skipId2, skipGbs) {{
    for (const _nd of NODES) {{
      if (_nd.id === skipId1 || _nd.id === skipId2) continue;
      const _np = positions[_nd.id]; if (!_np) continue;
      const _nw = _nd.type === 'pe' ? PE_W : SVC_W;
      const _nh = (_nd.type === 'pe' ? PE_H : SVC_H) + 20;
      const _pad = 6;
      if (cy > _np.y - _pad && cy < _np.y + _nh + _pad &&
          xMin < _np.x + _nw + _pad && xMax > _np.x - _pad) {{
        return false;
      }}
    }}
    for (const _gb of groupBoxes) {{
      if (skipGbs && skipGbs.indexOf(_gb) >= 0) continue;
      if (cy > _gb.y - 4 && cy < _gb.y + _gb.h + 4 &&
          xMin < _gb.x + _gb.w + 4 && xMax > _gb.x - 4) {{
        return false;
      }}
    }}
    return true;
  }}
  function _findGb(px, py) {{
    for (const _gb of groupBoxes) {{
      if (px >= _gb.x && px <= _gb.x + _gb.w && py >= _gb.y && py <= _gb.y + _gb.h) return _gb;
    }}
    return null;
  }}
  // Localiza a coluna livre mais próxima a partir do x preferencial, ignorando as seções de origem/destino
  function _findCol(prefX, yMin, yMax, skipId1, skipId2, skipGbs, preferDir) {{
    // Tenta primeiro a posição preferencial (vertical direta a partir do nó)
    if (!_colUsed(prefX) && _isColClear(prefX, yMin, yMax, skipId1, skipId2, skipGbs)) return prefX;
    // Pesquisa para fora em pequenos passos
    const _dirs = preferDir < 0 ? [-1, 1] : (preferDir > 0 ? [1, -1] : [-1, 1]);
    for (let _t = 1; _t <= 100; _t++) {{
      for (const _d of _dirs) {{
        const _cx = prefX + _d * _t * OSEP;
        if (_cx < 20) continue;
        if (_colUsed(_cx)) continue;
        if (_isColClear(_cx, yMin, yMax, skipId1, skipId2, skipGbs)) return _cx;
      }}
    }}
    return null;
  }}
  for (let _blPass = 0; _blPass < 20; _blPass++) {{
    let _worstEdge = -1, _worstCount = 0;
    for (let i = 0; i < _allEdgePaths.length; i++) {{
      if (_rerouted.has(i)) continue;
      let cnt = 0;
      const pB = _allEdgePaths[i].pts;
      for (let j = 0; j < _allEdgePaths.length; j++) {{
        if (j === i) continue;
        const pA = _allEdgePaths[j].pts;
        let maxOv = 0;
        for (let si = 0; si < pA.length - 1; si++) {{
          for (let sj = 0; sj < pB.length - 1; sj++) {{
            const a1 = pA[si], a2 = pA[si + 1], b1 = pB[sj], b2 = pB[sj + 1];
            if (Math.abs(a1.y - a2.y) < 2 && Math.abs(b1.y - b2.y) < 2 && Math.abs(a1.y - b1.y) < OSEP2) {{
              const ov = Math.min(Math.max(a1.x, a2.x), Math.max(b1.x, b2.x))
                       - Math.max(Math.min(a1.x, a2.x), Math.min(b1.x, b2.x));
              if (ov > maxOv) maxOv = ov;
            }}
            if (Math.abs(a1.x - a2.x) < 2 && Math.abs(b1.x - b2.x) < 2 && Math.abs(a1.x - b1.x) < OSEP2) {{
              const ov = Math.min(Math.max(a1.y, a2.y), Math.max(b1.y, b2.y))
                       - Math.max(Math.min(a1.y, a2.y), Math.min(b1.y, b2.y));
              if (ov > maxOv) maxOv = ov;
            }}
          }}
        }}
        if (maxOv > 20) cnt++;
      }}
      if (cnt > _worstCount) {{ _worstCount = cnt; _worstEdge = i; }}
    }}
    if (_worstEdge < 0) break;
    const pB = _allEdgePaths[_worstEdge].pts;
    const _fromId = _allEdgePaths[_worstEdge].edge.from;
    const _toId = _allEdgePaths[_worstEdge].edge.to;
    const start = pB[0];
    const end = pB[pB.length - 1];
    // As seções de origem/destino são isentas: linhas verticais podem atravessar a própria seção
    const srcGb = _findGb(start.x, start.y);
    const dstGb = _findGb(end.x, end.y);
    const skipGbs = [srcGb, dstGb].filter(g => g !== null);
    const _yMin = Math.min(start.y, end.y);
    const _yMax = Math.max(start.y, end.y);
    const _spanX = Math.abs(end.x - start.x);
    // Prefere primeiro o redirecionamento local por uma coluna para evitar desvios inferiores longos.
    const _localPrefX = (start.x + end.x) / 2;
    const _localX = _findCol(_localPrefX, _yMin, _yMax, _fromId, _toId, skipGbs);
    const _localLimit = Math.max(_spanX + 40, 120);
    if (_localX !== null &&
        Math.abs(_localX - start.x) <= _localLimit &&
        Math.abs(_localX - end.x) <= _localLimit &&
        _isRowClear(start.y, Math.min(start.x, _localX), Math.max(start.x, _localX), _fromId, _toId, skipGbs) &&
        _isRowClear(end.y, Math.min(end.x, _localX), Math.max(end.x, _localX), _fromId, _toId, skipGbs)) {{
      _usedCols.push(_localX);
      pB.length = 0;
      pB.push(start);
      if (Math.abs(_localX - start.x) > 2) pB.push({{ x: _localX, y: start.y }});
      if (Math.abs(end.y - start.y) > 2) pB.push({{ x: _localX, y: end.y }});
      if (Math.abs(_localX - end.x) > 2) pB.push({{ x: _localX, y: end.y }});
      pB.push(end);
      _rerouted.add(_worstEdge);
      continue;
    }}
    const laneY = _bottomLaneBase + _bottomSlot * _LANE_SPC;
    const _towardEnd = end.x >= start.x ? 1 : -1;
    const _exitX = _findCol(start.x, Math.min(start.y, laneY), Math.max(start.y, laneY), _fromId, _toId, skipGbs, _towardEnd);
    const _enterX = _findCol(end.x, Math.min(end.y, laneY), Math.max(end.y, laneY), _fromId, _toId, skipGbs, -_towardEnd);
    if (_exitX === null || _enterX === null) {{
      _rerouted.add(_worstEdge);
      continue;
    }}
    _usedCols.push(_exitX);
    _usedCols.push(_enterX);
    _bottomSlot++;
    pB.length = 0;
    pB.push(start);
    // Adiciona o segmento horizontal somente se a coluna de saída diferir do x do nó
    if (Math.abs(_exitX - start.x) > 2) pB.push({{ x: _exitX, y: start.y }});
    pB.push({{ x: _exitX, y: laneY }});
    pB.push({{ x: _enterX, y: laneY }});
    if (Math.abs(_enterX - end.x) > 2) pB.push({{ x: _enterX, y: end.y }});
    pB.push(end);
    _rerouted.add(_worstEdge);
  }}
  // SEPARAÇÃO DE SOBREPOSIÇÕES APÓS NOVO ROTEAMENTO: afasta os segmentos redirecionados
  for (let _rSep = 0; _rSep < 6; _rSep++) {{
    for (let i = 0; i < _allEdgePaths.length; i++) {{
      for (let j = i + 1; j < _allEdgePaths.length; j++) {{
        const pA = _allEdgePaths[i].pts;
        const pB = _allEdgePaths[j].pts;
        // Separa todos os pares de arestas para tratar sobreposições após o novo roteamento
        const dir = (j % 2 === 0) ? 1 : -1;
        for (let si = 0; si < pA.length - 1; si++) {{
          for (let sj = 0; sj < pB.length - 1; sj++) {{
            const a1 = pA[si], a2 = pA[si + 1];
            const b1 = pB[sj], b2 = pB[sj + 1];
            const aV = Math.abs(a1.x - a2.x) < 2;
            const bV = Math.abs(b1.x - b2.x) < 2;
            const aH = Math.abs(a1.y - a2.y) < 2;
            const bH = Math.abs(b1.y - b2.y) < 2;
            if (aV && bV && Math.abs(a1.x - b1.x) < OSEP2) {{
              const ov = Math.min(Math.max(a1.y, a2.y), Math.max(b1.y, b2.y))
                       - Math.max(Math.min(a1.y, a2.y), Math.min(b1.y, b2.y));
              if (ov > 10) {{
                let shift = OSEP2 * dir;
                if (b1.x + shift < 20) shift = Math.abs(shift);
                if (sj > 0) pB[sj] = {{ x: b1.x + shift, y: b1.y }};
                if (sj + 1 < pB.length - 1) pB[sj + 1] = {{ x: b2.x + shift, y: b2.y }};
              }}
            }}
            if (aH && bH && Math.abs(a1.y - b1.y) < OSEP2) {{
              const ov = Math.min(Math.max(a1.x, a2.x), Math.max(b1.x, b2.x))
                       - Math.max(Math.min(a1.x, a2.x), Math.min(b1.x, b2.x));
              if (ov > 10) {{
                const shift = OSEP2 * dir;
                if (sj > 0) pB[sj] = {{ x: b1.x, y: b1.y + shift }};
                if (sj + 1 < pB.length - 1) pB[sj + 1] = {{ x: b2.x, y: b2.y + shift }};
              }}
            }}
          }}
        }}
      }}
    }}
  }}
  // ORTOGONALIZAÇÃO APÓS NOVO ROTEAMENTO
  _allEdgePaths.forEach(({{ pts }}) => {{
    for (let _i = 0; _i < pts.length - 1; _i++) {{
      const _a = pts[_i], _b = pts[_i + 1];
      if (Math.abs(_a.x - _b.x) > 1 && Math.abs(_a.y - _b.y) > 1) {{
        pts.splice(_i + 1, 0, {{x: _a.x, y: _b.y}});
      }}
    }}
    for (let _i = pts.length - 2; _i >= 1; _i--) {{
      const _a = pts[_i - 1], _b = pts[_i], _c = pts[_i + 1];
      if (Math.abs(_a.x - _b.x) <= 1 && Math.abs(_a.y - _b.y) <= 1) {{
        pts.splice(_i, 1); continue;
      }}
      if ((Math.abs(_a.x - _b.x) <= 1 && Math.abs(_b.x - _c.x) <= 1) ||
          (Math.abs(_a.y - _b.y) <= 1 && Math.abs(_b.y - _c.y) <= 1)) {{
        pts.splice(_i, 1);
      }}
    }}
  }});

  // SEPARAÇÃO FINAL DE SOBREPOSIÇÕES: trata sobreposições recriadas pela ortogonalização
  for (let _fSep = 0; _fSep < 4; _fSep++) {{
    for (let i = 0; i < _allEdgePaths.length; i++) {{
      for (let j = i + 1; j < _allEdgePaths.length; j++) {{
        const pA = _allEdgePaths[i].pts;
        const pB = _allEdgePaths[j].pts;
        for (let si = 0; si < pA.length - 1; si++) {{
          for (let sj = 0; sj < pB.length - 1; sj++) {{
            const a1 = pA[si], a2 = pA[si + 1];
            const b1 = pB[sj], b2 = pB[sj + 1];
            const aH = Math.abs(a1.y - a2.y) < 2;
            const bH = Math.abs(b1.y - b2.y) < 2;
            const aV = Math.abs(a1.x - a2.x) < 2;
            const bV = Math.abs(b1.x - b2.x) < 2;
            if (aH && bH && Math.abs(a1.y - b1.y) < 6) {{
              const ov = Math.min(Math.max(a1.x, a2.x), Math.max(b1.x, b2.x))
                       - Math.max(Math.min(a1.x, a2.x), Math.min(b1.x, b2.x));
              if (ov > 20) {{
                const shift = 8 * ((j % 2 === 0) ? 1 : -1);
                if (sj > 0) pB[sj] = {{ x: b1.x, y: b1.y + shift }};
                if (sj + 1 < pB.length - 1) pB[sj + 1] = {{ x: b2.x, y: b2.y + shift }};
              }}
            }}
            if (aV && bV && Math.abs(a1.x - b1.x) < 6) {{
              const ov = Math.min(Math.max(a1.y, a2.y), Math.max(b1.y, b2.y))
                       - Math.max(Math.min(a1.y, a2.y), Math.min(b1.y, b2.y));
              if (ov > 20) {{
                let shift = 8 * ((j % 2 === 0) ? 1 : -1);
                if (b1.x + shift < 20) shift = Math.abs(shift);
                if (sj > 0) pB[sj] = {{ x: b1.x + shift, y: b1.y }};
                if (sj + 1 < pB.length - 1) pB[sj + 1] = {{ x: b2.x + shift, y: b2.y }};
              }}
            }}
          }}
        }}
      }}
    }}
  }}

  // DIVISOR FINAL DE DIAGONAIS: divide qualquer segmento não ortogonal em forma de L.
  // A etapa de separação acima pode introduzir diagonais quando move somente uma
  // extremidade. Alinha todos os segmentos aos eixos como última proteção.
  for (const _ep of _allEdgePaths) {{
    const pts = _ep.pts;
    for (let k = 0; k < pts.length - 1; k++) {{
      const q1 = pts[k], q2 = pts[k + 1];
      const dx = q2.x - q1.x;
      const dy = q2.y - q1.y;
      if (Math.abs(dx) > 1 && Math.abs(dy) > 1) {{
        // Insere uma curva em (q2.x, q1.y), preserva as extremidades e força a forma de L.
        // Heurística de direção: segue primeiro o eixo dominante.
        const elbow = Math.abs(dx) >= Math.abs(dy)
          ? {{ x: q2.x, y: q1.y }}
          : {{ x: q1.x, y: q2.y }};
        pts.splice(k + 1, 0, elbow);
        // Verifica novamente os segmentos recém-inseridos na próxima iteração
      }}
    }}
  }}

  // DETECÇÃO DE CRUZAMENTOS: localiza as arestas que se cruzam (para diferenciá-las por cor)
  const _crossNeighbors = {{}};
  for (let i = 0; i < _allEdgePaths.length; i++) {{
    for (let j = i + 1; j < _allEdgePaths.length; j++) {{
      const ptsA = _allEdgePaths[i].pts;
      const ptsB = _allEdgePaths[j].pts;
      let crossed = false;
      for (let si = 0; si < ptsA.length - 1 && !crossed; si++) {{
        for (let sj = 0; sj < ptsB.length - 1 && !crossed; sj++) {{
          if (findSegCrossing(
            ptsA[si].x, ptsA[si].y, ptsA[si + 1].x, ptsA[si + 1].y,
            ptsB[sj].x, ptsB[sj].y, ptsB[sj + 1].x, ptsB[sj + 1].y
          )) crossed = true;
        }}
      }}
      if (crossed) {{
        if (!_crossNeighbors[i]) _crossNeighbors[i] = new Set();
        if (!_crossNeighbors[j]) _crossNeighbors[j] = new Set();
        _crossNeighbors[i].add(j);
        _crossNeighbors[j].add(i);
      }}
    }}
  }}

  // Coloração gulosa do grafo: arestas que se cruzam recebem cores diferentes
  const _CROSS_COLORS = ['#0078D4', '#E3008C', '#00B7C3', '#FF8C00', '#107C10', '#881798'];
  const _edgeColor = {{}};
  const crossingEdges = Object.keys(_crossNeighbors).map(Number)
    .sort((a, b) => _crossNeighbors[b].size - _crossNeighbors[a].size);
  crossingEdges.forEach(eIdx => {{
    const neighborColors = new Set();
    _crossNeighbors[eIdx].forEach(n => {{
      if (_edgeColor[n] !== undefined) neighborColors.add(_edgeColor[n]);
    }});
    let colorIdx = 0;
    while (neighborColors.has(colorIdx)) colorIdx++;
    _edgeColor[eIdx] = colorIdx;
  }});

  // RENDERIZAÇÃO DAS ARESTAS: sem arcos de ponte, somente caminhos ortogonais com cores

  function renderEdge({{ edge, pts, isPeEdge, edgeIdx }}) {{
    let pathD;
    if (pts.length <= 2) {{
      pathD = `M ${{pts[0].x}} ${{pts[0].y}} L ${{pts[pts.length - 1].x}} ${{pts[pts.length - 1].y}}`;
    }} else {{
      pathD = buildOrthoPath(pts);
    }}

    // Define a cor da aresta: PE=roxo, cruzamento=colorido, normal=cinza
    let edgeStroke, edgeOpacity;
    if (isPeEdge) {{
      edgeStroke = '#5C2D91';
      edgeOpacity = '0.5';
    }} else if (_edgeColor[edgeIdx] !== undefined) {{
      edgeStroke = _CROSS_COLORS[_edgeColor[edgeIdx] % _CROSS_COLORS.length];
      edgeOpacity = '0.75';
    }} else {{
      edgeStroke = '#8a8886';
      edgeOpacity = '0.65';
    }}

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', pathD);
    path.setAttribute('fill', 'none');
    path.setAttribute('stroke', edgeStroke);
    path.setAttribute('stroke-width', isPeEdge ? '1' : '1.2');
    path.setAttribute('stroke-dasharray', edge.dash || '0');
    path.setAttribute('marker-end', `url(#${{markerFor(edge.type)}})`);
    path.setAttribute('opacity', edgeOpacity);
    path.classList.add('edge-path');
    path.setAttribute('data-from', edge.from);
    path.setAttribute('data-to', edge.to);
    root.appendChild(path);

    // Posicionamento de rótulos com detecção de colisões
    if (edge.label) {{
      const bw = edge.label.length * 5.5 + 10;
      const bh = 14;

      function labelHitsNode(lx, ly) {{
        return NODES.some(n => {{
          const p = positions[n.id];
          if (!p) return false;
          const nw = n.type === 'pe' ? PE_W : SVC_W;
          const nh = n.type === 'pe' ? PE_H : SVC_H;
          return lx + bw/2 > p.x && lx - bw/2 < p.x + nw
              && ly + bh/2 > p.y && ly - bh/2 < p.y + nh;
        }});
      }}

      const candidates = [];
      for (let s = 0; s < pts.length - 1; s++) {{
        const cx = (pts[s].x + pts[s + 1].x) / 2;
        const cy = (pts[s].y + pts[s + 1].y) / 2;
        const priority = Math.abs(s - (pts.length - 2) / 2);
        candidates.push({{ x: cx, y: cy, priority }});
      }}
      candidates.sort((a, b) => a.priority - b.priority);

      let chosen = candidates[0];
      for (const c of candidates) {{
        if (!labelHitsNode(c.x, c.y)) {{ chosen = c; break; }}
      }}

      if (labelHitsNode(chosen.x, chosen.y)) {{
        const offsets = [{{x:0,y:-20}},{{x:0,y:20}},{{x:-20,y:0}},{{x:20,y:0}}];
        for (const off of offsets) {{
          if (!labelHitsNode(chosen.x + off.x, chosen.y + off.y)) {{
            chosen = {{ x: chosen.x + off.x, y: chosen.y + off.y }};
            break;
          }}
        }}
      }}

      _edgeLabels.push({{ label: edge.label, x: chosen.x, y: chosen.y, from: edge.from, to: edge.to }});
    }}

    return {{ path, edge, pts }};
  }}

  // Renderiza todas as arestas
  _allEdgePaths.forEach((ep, edgeIdx) => renderEdge({{ ...ep, edgeIdx }}));

  // Reinsere os rótulos dos grupos sobre as arestas
  _groupLabelElements.forEach(el => root.appendChild(el));

  // ── Nós (renderizados POR ÚLTIMO, sobre as arestas e os cruzamentos) ──
  NODES.forEach(node => {{
    const pos = positions[node.id];
    if (!pos) return;
    const isPe = node.type === 'pe';
    const nw = isPe ? PE_W : SVC_W;
    const nh = isPe ? PE_H : SVC_H;
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('class', 'node');
    g.setAttribute('data-id', node.id);
    g.setAttribute('transform', `translate(${{pos.x}},${{pos.y}})`);

    // Fundo do cartão: toda a área é clicável
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('class', 'node-bg');
    rect.setAttribute('width', nw); rect.setAttribute('height', nh);
    rect.setAttribute('rx', '8'); rect.setAttribute('fill', 'white');
    rect.setAttribute('stroke', '#c8c6c4'); rect.setAttribute('stroke-width', '1.2');
    rect.setAttribute('filter', 'url(#shadow)');
    g.appendChild(rect);

    // Barra de destaque colorida na parte superior
    const accent = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    accent.setAttribute('width', nw); accent.setAttribute('height', '3');
    accent.setAttribute('rx', '8'); accent.setAttribute('fill', node.color);
    accent.setAttribute('opacity', '0.7');
    g.appendChild(accent);

    // Ícone: prefere o ícone oficial do Azure (URI de dados) e usa SVG como alternativa
    const iconSize = isPe ? 28 : 36;
    const iconX = (nw - iconSize) / 2;
    const iconY = isPe ? 12 : 14;
    if (node.icon_data_uri) {{
      // Ícone oficial do Azure (imagem Base64)
      const iconImg = document.createElementNS('http://www.w3.org/2000/svg', 'image');
      iconImg.setAttribute('x', iconX); iconImg.setAttribute('y', iconY);
      iconImg.setAttribute('width', iconSize); iconImg.setAttribute('height', iconSize);
      iconImg.setAttribute('role', 'img'); iconImg.setAttribute('aria-label', node.name);
      iconImg.setAttributeNS('http://www.w3.org/1999/xlink', 'href', node.icon_data_uri);
      g.appendChild(iconImg);
    }} else {{
      // Alternativa: ícone de texto SVG integrado
      const iconG = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      iconG.setAttribute('x', iconX); iconG.setAttribute('y', iconY);
      iconG.setAttribute('width', iconSize); iconG.setAttribute('height', iconSize);
      iconG.setAttribute('viewBox', '0 0 48 48');
      iconG.innerHTML = node.icon_svg;
      g.appendChild(iconG);
    }}

    // Nome: espaço extra abaixo do ícone (base do ícone ~50, base do nome em 74 → 24 px)
    const name = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    name.setAttribute('x', nw/2); name.setAttribute('y', isPe ? 64 : 74);
    name.setAttribute('text-anchor', 'middle');
    name.setAttribute('font-size', isPe ? '10' : '11');
    name.setAttribute('font-weight', '600'); name.setAttribute('fill', '#323130');
    name.setAttribute('font-family', 'Segoe UI, sans-serif');
    const maxC = isPe ? 14 : 20;
    name.textContent = node.name.length > maxC ? node.name.substring(0, maxC-1) + '..' : node.name;
    g.appendChild(name);

    // Rótulo da SKU
    if (!isPe && node.sku) {{
      const sku = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      sku.setAttribute('x', nw/2); sku.setAttribute('y', 90);
      sku.setAttribute('text-anchor', 'middle');
      sku.setAttribute('font-size', '10'); sku.setAttribute('fill', '#a19f9d');
      sku.setAttribute('font-family', 'Segoe UI, sans-serif');
      sku.textContent = node.sku;
      g.appendChild(sku);
    }}

    if (isPe && node.details.length > 0) {{
      const det = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      det.setAttribute('x', nw/2); det.setAttribute('y', 76);
      det.setAttribute('text-anchor', 'middle');
      det.setAttribute('font-size', '9'); det.setAttribute('fill', '#a19f9d');
      det.setAttribute('font-family', 'Segoe UI, sans-serif');
      det.textContent = node.details[0];
      g.appendChild(det);
    }}

    // Rótulo do tipo de serviço abaixo (não é a categoria; mostra o tipo real)
    if (!isPe) {{
      const TYPE_LABELS = {{
        'ai_foundry': 'AI Foundry', 'openai': 'Azure OpenAI', 'search': 'AI Search', 'ai_search': 'AI Search',
        'storage': 'Storage', 'adls': 'ADLS Gen2', 'keyvault': 'Key Vault', 'kv': 'Key Vault',
        'fabric': 'Fabric', 'databricks': 'Databricks', 'adf': 'Data Factory', 'data_factory': 'Data Factory',
        'sql_server': 'SQL Server', 'sql_database': 'SQL Database', 'cosmos_db': 'Cosmos DB',
        'vm': 'Virtual Machine', 'aks': 'AKS', 'app_service': 'App Service',
        'function_app': 'Function App', 'synapse': 'Synapse', 'vnet': 'VNet',
        'nsg': 'NSG', 'bastion': 'Bastion', 'pe': 'Private Endpoint',
        'log_analytics': 'Log Analytics', 'app_insights': 'App Insights',
        'monitor': 'Monitor', 'acr': 'Container Registry', 'container_registry': 'Container Registry',
        'document_intelligence': 'Doc Intelligence', 'form_recognizer': 'Doc Intelligence',
        'cdn': 'CDN', 'event_hub': 'Event Hub', 'redis': 'Redis Cache',
        'devops': 'Azure DevOps', 'app_gateway': 'App Gateway',
        'iot_hub': 'IoT Hub', 'stream_analytics': 'Stream Analytics',
        'vpn_gateway': 'VPN Gateway', 'front_door': 'Front Door',
        'ai_hub': 'AI Hub', 'firewall': 'Firewall',
      }};
      const typeLabel = TYPE_LABELS[node.type] || node.type;
      const cat = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      cat.setAttribute('x', nw/2); cat.setAttribute('y', nh + 14);
      cat.setAttribute('text-anchor', 'middle');
      cat.setAttribute('font-size', '10'); cat.setAttribute('fill', node.color);
      cat.setAttribute('font-weight', '600');
      cat.setAttribute('font-family', 'Segoe UI, sans-serif');
      cat.textContent = typeLabel;
      g.appendChild(cat);
    }}

    // Selo de privado no cartão
    if (node.private && !isPe) {{
      const badge = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      const br = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      br.setAttribute('x', nw - 8); br.setAttribute('y', '4');
      br.setAttribute('width', '6'); br.setAttribute('height', '6');
      br.setAttribute('rx', '3'); br.setAttribute('fill', '#5C2D91');
      br.setAttribute('opacity', '0.6');
      badge.appendChild(br);
      g.appendChild(badge);
    }}

    // ── Eventos: separação entre arrastar e clicar ──
    g.addEventListener('mousedown', e => {{
      if (e.button !== 0) return;
      dragging = node.id;
      _didDrag = false;
      _dragStartX = e.clientX; _dragStartY = e.clientY;
      const svgPt = getSVGPoint(e);
      dragOffX = svgPt.x - pos.x; dragOffY = svgPt.y - pos.y;
      e.stopPropagation(); e.preventDefault();
    }});
    g.addEventListener('mousemove', e => {{
      if (dragging === node.id) {{
        const dx = Math.abs(e.clientX - _dragStartX);
        const dy = Math.abs(e.clientY - _dragStartY);
        if (dx > 3 || dy > 3) _didDrag = true;
      }}
    }});
    g.addEventListener('mouseup', e => {{
      if (!_didDrag && dragging === node.id) {{
        selectNode(node.id);
      }}
    }});
    g.addEventListener('mouseenter', e => {{
      const tt = document.getElementById('tooltip');
      const dets = node.details.map(d => `<div class="tooltip-detail">› ${{d}}</div>`).join('');
      tt.style.display = 'block';
      tt.innerHTML = `<strong>${{node.name}}</strong>${{node.sku ? `<div class="tooltip-detail">SKU: ${{node.sku}}</div>` : ''}}${{dets}}`;
    }});
    g.addEventListener('mousemove', e => {{
      const tt = document.getElementById('tooltip');
      tt.style.left = (e.clientX+12)+'px'; tt.style.top = (e.clientY-8)+'px';
    }});
    g.addEventListener('mouseleave', () => {{ document.getElementById('tooltip').style.display = 'none'; }});

    root.appendChild(g);
  }});

  // ── Rótulos das arestas (renderizados APÓS os nós, sempre visíveis acima) ──
  _edgeLabels.forEach(el => {{
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.classList.add('edge-label');
    g.setAttribute('data-from', el.from);
    g.setAttribute('data-to', el.to);
    const r = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    r.classList.add('edge-label-bg');
    const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    const bw = el.label.length * 6 + 10;
    r.setAttribute('x', el.x-bw/2); r.setAttribute('y', el.y-7);
    r.setAttribute('width', bw); r.setAttribute('height', 14);
    r.setAttribute('rx', '3'); r.setAttribute('fill', 'white');
    r.setAttribute('stroke', '#d2d0ce'); r.setAttribute('stroke-width', '0.5');
    r.setAttribute('opacity', '0.95');
    t.setAttribute('x', el.x); t.setAttribute('y', el.y+3);
    t.setAttribute('text-anchor', 'middle'); t.setAttribute('font-size', '9');
    t.setAttribute('fill', '#605e5c'); t.setAttribute('font-family', 'Segoe UI, sans-serif');
    t.textContent = el.label;
    g.appendChild(r); g.appendChild(t);
    root.appendChild(g);
  }});

  // Reaplica a escala do texto e o estado da seleção após reconstruir o DOM
  if (typeof _textScale !== 'undefined' && _textScale !== 1) applyTextScale();
  if (_selectedNodeId) applySelectionHighlight();

}}

function getSVGPoint(e) {{
  const svg = document.getElementById('canvas');
  const pt = svg.createSVGPoint();
  pt.x = e.clientX; pt.y = e.clientY;
  return pt.matrixTransform(document.getElementById('diagram-root').getScreenCTM().inverse());
}}

document.getElementById('canvas').addEventListener('mousemove', e => {{
  if (dragging) {{
    const p = getSVGPoint(e);
    positions[dragging].x = p.x - dragOffX;
    positions[dragging].y = p.y - dragOffY;
    renderDiagram();
  }} else if (draggingGroup !== null) {{
    const p = getSVGPoint(e);
    const dx = p.x - dragOffX;
    const dy = p.y - dragOffY;
    dragOffX = p.x; dragOffY = p.y;
    // Move todos os nós do grupo
    groupDragNodes.forEach(nid => {{
      if (positions[nid]) {{
        positions[nid].x += dx;
        positions[nid].y += dy;
      }}
    }});
    // Também move a própria caixa de grupo
    const gb = groupBoxes[draggingGroup];
    if (gb) {{ gb.x += dx; gb.y += dy; }}
    renderDiagram();
  }}
}});
document.addEventListener('mouseup', () => {{ dragging = null; draggingGroup = null; groupDragNodes = []; }});

// ── Movimento e zoom ──
function applyTransform() {{
  document.getElementById('diagram-root').setAttribute('transform',
    `translate(${{viewTransform.x}},${{viewTransform.y}}) scale(${{viewTransform.scale}})`);
  document.getElementById('zoom-level').textContent = Math.round(viewTransform.scale * 100) + '%';
}}
function fitToScreen() {{
  const svg = document.getElementById('canvas');
  const root = document.getElementById('diagram-root');
  root.setAttribute('transform', '');
  const bbox = root.getBBox();
  if (!bbox.width || !bbox.height) return;
  const w = svg.clientWidth, h = svg.clientHeight;
  const s = Math.min((w-60)/bbox.width, (h-60)/bbox.height, 1.5);
  if (s <= 0) return;
  viewTransform.scale = s;
  viewTransform.x = (w - bbox.width*s)/2 - bbox.x*s;
  viewTransform.y = (h - bbox.height*s)/2 - bbox.y*s;
  applyTransform();
}}
function zoomIn() {{ viewTransform.scale *= 1.25; applyTransform(); }}
function zoomOut() {{ viewTransform.scale *= 0.8; applyTransform(); }}

// ── Controles de tamanho do texto ──
let _textScale = 1.4;  // por padrão, 40% maior que os tamanhos brutos dos atributos
function applyTextScale() {{
  document.querySelectorAll('#canvas text').forEach(t => {{
    let orig = t.getAttribute('data-orig-fs');
    if (!orig) {{
      orig = t.getAttribute('font-size');
      if (!orig) {{
        const cs = window.getComputedStyle(t).fontSize;
        orig = cs ? parseFloat(cs).toString() : '11';
      }}
      t.setAttribute('data-orig-fs', orig);
    }}
    t.setAttribute('font-size', (parseFloat(orig) * _textScale).toFixed(2));
  }});
}}
function textBigger() {{ _textScale = Math.min(2.5, _textScale * 1.15); applyTextScale(); }}
function textSmaller() {{ _textScale = Math.max(0.5, _textScale / 1.15); applyTextScale(); }}

function downloadPNG() {{
  const svg = document.getElementById('canvas');
  const bbox = svg.getBBox();
  const pad = 40;
  const w = Math.ceil(bbox.width + bbox.x + pad * 2);
  const h = Math.ceil(bbox.height + bbox.y + pad * 2);

  const clone = svg.cloneNode(true);
  clone.setAttribute('width', w);
  clone.setAttribute('height', h);
  clone.setAttribute('viewBox', `${{-pad}} ${{-pad}} ${{w}} ${{h}}`);
  clone.querySelector('#viewport')?.removeAttribute('transform');

  // Incorpora todos os estilos calculados
  const allEls = clone.querySelectorAll('*');
  const origEls = svg.querySelectorAll('*');
  allEls.forEach((el, i) => {{
    if (origEls[i]) {{
      const cs = window.getComputedStyle(origEls[i]);
      ['fill','stroke','stroke-width','font-size','font-family','font-weight',
       'text-anchor','opacity','fill-opacity','stroke-opacity','stroke-dasharray'].forEach(p => {{
        const v = cs.getPropertyValue(p);
        if (v) el.style.setProperty(p, v);
      }});
    }}
  }});

  const serializer = new XMLSerializer();
  const svgStr = serializer.serializeToString(clone);
  const svgBlob = new Blob([svgStr], {{type: 'image/svg+xml;charset=utf-8'}});
  const url = URL.createObjectURL(svgBlob);

  const img = new Image();
  img.onload = () => {{
    const canvas = document.createElement('canvas');
    const scale = 2;
    canvas.width = w * scale;
    canvas.height = h * scale;
    const ctx = canvas.getContext('2d');
    ctx.scale(scale, scale);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, w, h);
    ctx.drawImage(img, 0, 0, w, h);
    URL.revokeObjectURL(url);

    canvas.toBlob(blob => {{
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = (document.title || 'azure-architecture') + '.png';
      a.click();
      URL.revokeObjectURL(a.href);
    }}, 'image/png');
  }};
  img.src = url;
}}

document.getElementById('canvas').addEventListener('wheel', e => {{
  e.preventDefault();
  const f = e.deltaY < 0 ? 1.1 : 0.9;
  const rect = document.getElementById('canvas').getBoundingClientRect();
  const mx = e.clientX - rect.left, my = e.clientY - rect.top;
  const os = viewTransform.scale, ns = os * f;
  viewTransform.x = mx - (mx - viewTransform.x) * (ns/os);
  viewTransform.y = my - (my - viewTransform.y) * (ns/os);
  viewTransform.scale = ns;
  applyTransform();
}}, {{ passive: false }});

document.getElementById('canvas').addEventListener('mousedown', e => {{
  if (e.target.closest('.node')) return;
  isPanning = true;
  panSX = e.clientX; panSY = e.clientY;
  panSTx = viewTransform.x; panSTy = viewTransform.y;
  document.getElementById('canvas').style.cursor = 'grabbing';
  e.preventDefault();
}});
document.addEventListener('mousemove', e => {{
  if (isPanning) {{
    viewTransform.x = panSTx + (e.clientX - panSX);
    viewTransform.y = panSTy + (e.clientY - panSY);
    applyTransform();
  }}
}});
document.addEventListener('mouseup', () => {{
  if (isPanning) {{ isPanning = false; document.getElementById('canvas').style.cursor = ''; }}
}});

// ── Barra lateral ──
function buildSidebar() {{
  const list = document.getElementById('service-list');
  const byCat = {{}};
  NODES.forEach(n => {{ if (!byCat[n.category]) byCat[n.category] = []; byCat[n.category].push(n); }});
  Object.entries(byCat).forEach(([cat, nodes]) => {{
    const cd = document.createElement('div');
    cd.className = 'cat-label'; cd.textContent = categoryLabel(cat);
    list.appendChild(cd);
    nodes.forEach(node => {{
      const card = document.createElement('div');
      card.className = 'service-card'; card.id = 'card-' + node.id;
      card.innerHTML = `
        <div class="service-card-header">
          <div class="sc-icon">${{node.icon_data_uri ? `<img src="${{node.icon_data_uri}}" alt="" width="28" height="28" style="object-fit:contain;">` : `<svg viewBox="0 0 48 48" aria-hidden="true">${{node.icon_svg}}</svg>`}}</div>
          <div>
            <div class="service-name">${{node.name}}</div>
            <div class="service-sku">${{node.sku || node.type}}</div>
          </div>
          ${{node.private ? '<span class="private-badge">Privado</span>' : ''}}
        </div>
        ${{node.details.length > 0 ? `<div class="service-card-body">${{node.details.map(d => `<div class="service-detail">${{d}}</div>`).join('')}}</div>` : ''}}
      `;
      card.addEventListener('click', () => {{
        selectNode(node.id);
      }});
      list.appendChild(card);
    }});
  }});
}}

// ── Alternância do destaque da VNet ──
let _vnetHighlighted = false;
function toggleVNetHighlight() {{
  _vnetHighlighted = !_vnetHighlighted;
  const vr = document.getElementById('vnet-rect');
  if (!vr) return;
  if (_vnetHighlighted) {{
    vr.setAttribute('stroke-width', '4');
    vr.setAttribute('stroke', '#5C2D91');
    vr.setAttribute('fill', '#f0eaf8');
  }} else {{
    vr.setAttribute('stroke-width', '2');
    vr.setAttribute('stroke', '#5C2D91');
    vr.setAttribute('fill', '#f8f7ff');
  }}
  // Também alterna o cartão da barra lateral
  const card = document.getElementById('card-vnet-boundary');
  if (card) card.classList.toggle('selected', _vnetHighlighted);
}}

renderDiagram();
buildSidebar();

// ── Cartão da VNet na barra lateral (adicionado dinamicamente se houver limite de VNet) ──
if (VNET_INFO || NODES.some(n => n.private && n.type !== 'pe') || NODES.some(n => n.type === 'pe')) {{
  const list = document.getElementById('service-list');
  // Insere na parte superior
  const catLabel = document.createElement('div');
  catLabel.className = 'cat-label'; catLabel.textContent = 'REDE';
  const card = document.createElement('div');
  card.className = 'service-card'; card.id = 'card-vnet-boundary';
  const vnetIcon = '<rect x="6" y="6" width="36" height="36" rx="4" fill="none" stroke="#5C2D91" stroke-width="3"/><circle cx="16" cy="18" r="3" fill="#5C2D91"/><circle cx="32" cy="18" r="3" fill="#5C2D91"/><circle cx="24" cy="32" r="3" fill="#5C2D91"/>';
  const vnetDetails = VNET_INFO ? VNET_INFO.split('|').map(s => s.trim()) : [];
  card.innerHTML = `
    <div class="service-card-header">
      <div class="sc-icon"><svg viewBox="0 0 48 48" aria-hidden="true">${{vnetIcon}}</svg></div>
      <div>
        <div class="service-name">Virtual Network</div>
        <div class="service-sku">vnet</div>
      </div>
      <span class="private-badge">Privado</span>
    </div>
    ${{vnetDetails.length > 0 ? `<div class="service-card-body">${{vnetDetails.map(d => `<div class="service-detail">${{d}}</div>`).join('')}}</div>` : ''}}
  `;
  card.addEventListener('click', () => {{ toggleVNetHighlight(); }});
  list.insertBefore(card, list.firstChild);
  list.insertBefore(catLabel, list.firstChild);
}}
setTimeout(fitToScreen, 100);
</script>
</body>
</html>"""
    return html

def generate_diagram(services, connections, title="Arquitetura do Azure", vnet_info="", hierarchy=None):
    """Gera um diagrama interativo de arquitetura do Azure como uma string HTML.

    Argumentos:
        services: lista de dicionários com as chaves id, name, type, sku, private, details etc.
        connections: lista de dicionários com as chaves from, to, label e type.
        title: cadeia de texto com o título do diagrama.
        vnet_info: cadeia de texto com informações de CIDR da VNet.
        hierarchy: lista opcional da hierarquia de assinatura/RG.

    Retorna:
        Cadeia HTML que contém o diagrama interativo.
    """
    return generate_html(services, connections, title, vnet_info=vnet_info, hierarchy=hierarchy)
