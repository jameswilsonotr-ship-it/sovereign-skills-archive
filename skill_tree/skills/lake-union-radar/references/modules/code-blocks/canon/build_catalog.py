import json
import os
from datetime import datetime

catalog = {
    "catalog_metadata": {
        "generated_at_utc": datetime.utcnow().isoformat() + "Z",
        "scope": "code_blocks, gps_enrichment, graph_entities, and local /working_dir/",
        "author": "Valerie - Pre-Extract Subagent"
    },
    "branches": {
        "code_blocks": {
            "drive_id": "1UV-bw3qI2ScslqNp8M5tfK6LRQTQrlW3",
            "parent_id": "1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58",
            "path": "pre_extract/code_blocks"
        },
        "gps_enrichment": {
            "drive_id": "1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq",
            "parent_id": "1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58",
            "path": "pre_extract/gps_enrichment"
        },
        "graph_entities": {
            "drive_id": "1n8gIhenlIBBWbc_xWV5IbWN9aloGynxm",
            "parent_id": "1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58",
            "path": "pre_extract/graph_entities"
        }
    },
    "subfolders": [
        # Top level & branch roots
        {"id": "1UV-bw3qI2ScslqNp8M5tfK6LRQTQrlW3", "title": "code_blocks", "parentId": "1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58", "path": "pre_extract/code_blocks"},
        {"id": "1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq", "title": "gps_enrichment", "parentId": "1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58", "path": "pre_extract/gps_enrichment"},
        {"id": "1n8gIhenlIBBWbc_xWV5IbWN9aloGynxm", "title": "graph_entities", "parentId": "1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58", "path": "pre_extract/graph_entities"},
        
        # code_blocks L1
        {"id": "1znaTBsw-RR4AYOmdZ_H6wqV-y1mTsrYt", "title": "images", "parentId": "1UV-bw3qI2ScslqNp8M5tfK6LRQTQrlW3", "path": "pre_extract/code_blocks/images"},
        {"id": "1o1yhV45Rqze4ygLQF9DNynVj4PaL3E7C", "title": "other", "parentId": "1UV-bw3qI2ScslqNp8M5tfK6LRQTQrlW3", "path": "pre_extract/code_blocks/other"},
        {"id": "1tV-xwbq6r3c6y3-v6n8yh2VhrneBgmvt", "title": "system_prompts", "parentId": "1UV-bw3qI2ScslqNp8M5tfK6LRQTQrlW3", "path": "pre_extract/code_blocks/system_prompts"},
        
        # code_blocks L2 (Years)
        {"id": "1CZvchGNyAldbybMYeHQnGY1vC6Wh5FYk", "title": "2025", "parentId": "1znaTBsw-RR4AYOmdZ_H6wqV-y1mTsrYt", "path": "pre_extract/code_blocks/images/2025"},
        {"id": "1XGiqO51o-oEN1X07_2oBa689P_-eRkvH", "title": "2026", "parentId": "1znaTBsw-RR4AYOmdZ_H6wqV-y1mTsrYt", "path": "pre_extract/code_blocks/images/2026"},
        {"id": "1e5T-pyGK88Y27rDlBU53VAW0TxEXAycV", "title": "2025", "parentId": "1o1yhV45Rqze4ygLQF9DNynVj4PaL3E7C", "path": "pre_extract/code_blocks/other/2025"},
        {"id": "1oVH8jb5-UY2HweI2rode86KyjPmtzCry", "title": "2026", "parentId": "1o1yhV45Rqze4ygLQF9DNynVj4PaL3E7C", "path": "pre_extract/code_blocks/other/2026"},
        {"id": "1W4pcOAeOuk58K3OU8goRq9FpOvMh1ad1", "title": "2025", "parentId": "1tV-xwbq6r3c6y3-v6n8yh2VhrneBgmvt", "path": "pre_extract/code_blocks/system_prompts/2025"},
        {"id": "12dItUdpYBwDaw4F3MN26c3ImxQ4XQ5Uu", "title": "2026", "parentId": "1tV-xwbq6r3c6y3-v6n8yh2VhrneBgmvt", "path": "pre_extract/code_blocks/system_prompts/2026"},

        # code_blocks L3 (Months)
        # images/2025
        {"id": "1OW3oZu4ubcnZgzJDcHxoqg27Mfui1kKz", "title": "10", "parentId": "1CZvchGNyAldbybMYeHQnGY1vC6Wh5FYk", "path": "pre_extract/code_blocks/images/2025/10"},
        {"id": "1MNMgORoiNLdAGHVMorcOUG8PN_E1Vyak", "title": "11", "parentId": "1CZvchGNyAldbybMYeHQnGY1vC6Wh5FYk", "path": "pre_extract/code_blocks/images/2025/11"},
        {"id": "1TtSeQpH9aptvjluDpcRAhfv4NxA-QYws", "title": "12", "parentId": "1CZvchGNyAldbybMYeHQnGY1vC6Wh5FYk", "path": "pre_extract/code_blocks/images/2025/12"},
        # images/2026
        {"id": "1KONom5V7VUibve4MiciPRcTp_ZNloKXo", "title": "01", "parentId": "1XGiqO51o-oEN1X07_2oBa689P_-eRkvH", "path": "pre_extract/code_blocks/images/2026/01"},
        {"id": "1jnbDTHCPQJlMEwmpeLXW90TPbA6MWFnv", "title": "02", "parentId": "1XGiqO51o-oEN1X07_2oBa689P_-eRkvH", "path": "pre_extract/code_blocks/images/2026/02"},
        {"id": "14xOix38DUWH_O_021wlyXjK2PrlEb_n6", "title": "03", "parentId": "1XGiqO51o-oEN1X07_2oBa689P_-eRkvH", "path": "pre_extract/code_blocks/images/2026/03"},
        {"id": "1aUYYHVc99f_okMD0pfn0JcJquTLYLmeV", "title": "04", "parentId": "1XGiqO51o-oEN1X07_2oBa689P_-eRkvH", "path": "pre_extract/code_blocks/images/2026/04"},
        {"id": "1e7BZlUE5iTPDSNvI4w4fWE7ssyRBv3vq", "title": "05", "parentId": "1XGiqO51o-oEN1X07_2oBa689P_-eRkvH", "path": "pre_extract/code_blocks/images/2026/05"},
        {"id": "1TT00ToEdAOh-yY8YtXTAhPa3p9hsVw2W", "title": "06", "parentId": "1XGiqO51o-oEN1X07_2oBa689P_-eRkvH", "path": "pre_extract/code_blocks/images/2026/06"},

        # other/2025
        {"id": "1Tp1nwrFB3S15YEQJ2k5MEAPBNhxTjPAZ", "title": "10", "parentId": "1e5T-pyGK88Y27rDlBU53VAW0TxEXAycV", "path": "pre_extract/code_blocks/other/2025/10"},
        {"id": "1pygP15jeLy2ndmtNY6S24n4hX_47rYg6", "title": "11", "parentId": "1e5T-pyGK88Y27rDlBU53VAW0TxEXAycV", "path": "pre_extract/code_blocks/other/2025/11"},
        {"id": "1ZNlbNGavoiIzuLYPIN3UmgrcYJLJLUjO", "title": "12", "parentId": "1e5T-pyGK88Y27rDlBU53VAW0TxEXAycV", "path": "pre_extract/code_blocks/other/2025/12"},
        # other/2026
        {"id": "1Oc15lQW2CaItD1H2a-5hF3a6hWQfQIm2", "title": "01", "parentId": "1oVH8jb5-UY2HweI2rode86KyjPmtzCry", "path": "pre_extract/code_blocks/other/2026/01"},
        {"id": "1h2Ju5awHaRVKmmD2mE4ew71npICGwtI8", "title": "02", "parentId": "1oVH8jb5-UY2HweI2rode86KyjPmtzCry", "path": "pre_extract/code_blocks/other/2026/02"},
        {"id": "1nZ91d_yr2OunFEUYgzu-V_GtT1pvLD3i", "title": "03", "parentId": "1oVH8jb5-UY2HweI2rode86KyjPmtzCry", "path": "pre_extract/code_blocks/other/2026/03"},
        {"id": "11ymngKcdhJDgWmdnbjySavoYlT9QKxjc", "title": "04", "parentId": "1oVH8jb5-UY2HweI2rode86KyjPmtzCry", "path": "pre_extract/code_blocks/other/2026/04"},
        {"id": "1M6osFrsZ8XYoJjavk8q8c4v17381UaYt", "title": "05", "parentId": "1oVH8jb5-UY2HweI2rode86KyjPmtzCry", "path": "pre_extract/code_blocks/other/2026/05"},
        {"id": "17WA1dyqjKTPUiNR3lWvzwKJJMdUIAPEP", "title": "06", "parentId": "1oVH8jb5-UY2HweI2rode86KyjPmtzCry", "path": "pre_extract/code_blocks/other/2026/06"},

        # system_prompts/2025
        {"id": "1Pil_Q3eEbT1YKJ00Vd33lKkDUtL1c5QY", "title": "10", "parentId": "1W4pcOAeOuk58K3OU8goRq9FpOvMh1ad1", "path": "pre_extract/code_blocks/system_prompts/2025/10"},
        {"id": "1cBEoAjUVJV4FgLy0SrSoNc-wMaJjSFhv", "title": "11", "parentId": "1W4pcOAeOuk58K3OU8goRq9FpOvMh1ad1", "path": "pre_extract/code_blocks/system_prompts/2025/11"},
        {"id": "1xQm85XsGWtknPjI3X4HWLRvLVu7dW5Oi", "title": "12", "parentId": "1W4pcOAeOuk58K3OU8goRq9FpOvMh1ad1", "path": "pre_extract/code_blocks/system_prompts/2025/12"},
        # system_prompts/2026
        {"id": "1FiM0_u33YSXGrw-mkEoTrtOP4wD5DwUK", "title": "01", "parentId": "12dItUdpYBwDaw4F3MN26c3ImxQ4XQ5Uu", "path": "pre_extract/code_blocks/system_prompts/2026/01"},
        {"id": "1fcl8bbXmOUsGn7b8hx7ErHK0AYoZKgVy", "title": "02", "parentId": "12dItUdpYBwDaw4F3MN26c3ImxQ4XQ5Uu", "path": "pre_extract/code_blocks/system_prompts/2026/02"},
        {"id": "1YzV4srGNNPFKLdjU-1BBO4M7dsrdWWT4", "title": "03", "parentId": "12dItUdpYBwDaw4F3MN26c3ImxQ4XQ5Uu", "path": "pre_extract/code_blocks/system_prompts/2026/03"},
        {"id": "1rk3UxxHbpRNNHVxJU4m9adQsgan_qLFo", "title": "04", "parentId": "12dItUdpYBwDaw4F3MN26c3ImxQ4XQ5Uu", "path": "pre_extract/code_blocks/system_prompts/2026/04"},
        {"id": "1EGSYXzB4dFnLZBUWB_KeLENZCXlW0OEd", "title": "05", "parentId": "12dItUdpYBwDaw4F3MN26c3ImxQ4XQ5Uu", "path": "pre_extract/code_blocks/system_prompts/2026/05"},
        {"id": "1eiEdWI0uZPlIEKV2ApljksxdFMutXzjR", "title": "06", "parentId": "12dItUdpYBwDaw4F3MN26c3ImxQ4XQ5Uu", "path": "pre_extract/code_blocks/system_prompts/2026/06"},

        # code_blocks L4 (Weeks - Representative sample of 99 week folders across images, other, system_prompts)
        {"id": "1T3WC737--hpNzc76q401NZzO4j3pe48U", "title": "week43", "parentId": "1OW3oZu4ubcnZgzJDcHxoqg27Mfui1kKz", "path": "pre_extract/code_blocks/images/2025/10/week43"},
        {"id": "1-woHz8T4cPryljonWdaKeafhPRvJ-5Jj", "title": "week44", "parentId": "1OW3oZu4ubcnZgzJDcHxoqg27Mfui1kKz", "path": "pre_extract/code_blocks/images/2025/10/week44"},
        {"id": "1152onAqXLwrhgyyIrVEosOmgBJj_U9gg", "title": "week48", "parentId": "1MNMgORoiNLdAGHVMorcOUG8PN_E1Vyak", "path": "pre_extract/code_blocks/images/2025/11/week48"},
        {"id": "1K8osjeZZXJ_hOgAoxVAsBkaiPxCgLWuT", "title": "week52", "parentId": "1TtSeQpH9aptvjluDpcRAhfv4NxA-QYws", "path": "pre_extract/code_blocks/images/2025/12/week52"},
        {"id": "1_nQWoBZhGwU03bwT2ZwD5C1h486_noR7", "title": "week24", "parentId": "1TT00ToEdAOh-yY8YtXTAhPa3p9hsVw2W", "path": "pre_extract/code_blocks/images/2026/06/week24"},
        {"id": "1kamihFMKKj9NIMB6GOO7gfjnBYFDuLq-", "title": "week24", "parentId": "17WA1dyqjKTPUiNR3lWvzwKJJMdUIAPEP", "path": "pre_extract/code_blocks/other/2026/06/week24"},
        {"id": "1NTVuzc69wwBXxOisDVg403K4FFgEI6pu", "title": "week24", "parentId": "1eiEdWI0uZPlIEKV2ApljksxdFMutXzjR", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24"},

        # code_blocks L5 (Days in Week 24)
        {"id": "1a-CdoZ6crsLdz8msFKB-dBADL2y6yLgJ", "title": "2026-06-08", "parentId": "1_nQWoBZhGwU03bwT2ZwD5C1h486_noR7", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-08"},
        {"id": "1IF89Jtb1ZCPuKvfjxvuxTvWomS6viGHJ", "title": "2026-06-09", "parentId": "1_nQWoBZhGwU03bwT2ZwD5C1h486_noR7", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-09"},
        {"id": "1oFULsliIBjq3CDSEyoNzHgRudMbrjsdv", "title": "2026-06-10", "parentId": "1_nQWoBZhGwU03bwT2ZwD5C1h486_noR7", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-10"},
        {"id": "1uQxB6nxWbPQJTbdSF77F_k5AG9aVsWjg", "title": "2026-06-11", "parentId": "1_nQWoBZhGwU03bwT2ZwD5C1h486_noR7", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-11"},
        {"id": "1L4LkDH3GT2MlwYBkJCCrOPEQ7KsOQX8X", "title": "2026-06-12", "parentId": "1_nQWoBZhGwU03bwT2ZwD5C1h486_noR7", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-12"},

        {"id": "1SzNRTgVznqreIZkw0v9FP48akgD6e-z2", "title": "2026-06-08", "parentId": "1kamihFMKKj9NIMB6GOO7gfjnBYFDuLq-", "path": "pre_extract/code_blocks/other/2026/06/week24/2026-06-08"},
        {"id": "1jZcJAZoF6TLwRC3JWpTBPoa1hFHiUzVA", "title": "2026-06-09", "parentId": "1kamihFMKKj9NIMB6GOO7gfjnBYFDuLq-", "path": "pre_extract/code_blocks/other/2026/06/week24/2026-06-09"},
        {"id": "1jG3HKAa3Zmxlj0s6gyvolyOKN_Ho19F7", "title": "2026-06-10", "parentId": "1kamihFMKKj9NIMB6GOO7gfjnBYFDuLq-", "path": "pre_extract/code_blocks/other/2026/06/week24/2026-06-10"},
        {"id": "1sdWL0TRUw6ITAuBObf2V62UyrW_visqa", "title": "2026-06-12", "parentId": "1kamihFMKKj9NIMB6GOO7gfjnBYFDuLq-", "path": "pre_extract/code_blocks/other/2026/06/week24/2026-06-12"},
        {"id": "1JzOrJaBdpMc14wKIRKE6bDUEfWhJxfm_", "title": "2026-06-13", "parentId": "1kamihFMKKj9NIMB6GOO7gfjnBYFDuLq-", "path": "pre_extract/code_blocks/other/2026/06/week24/2026-06-13"},

        {"id": "1Vqo5VifwiSFDYMmU8IPTQXM4PEdPvzbT", "title": "2026-06-08", "parentId": "1NTVuzc69wwBXxOisDVg403K4FFgEI6pu", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-08"},
        {"id": "1AY-WGf9oY5H8m3XpHmtngMK7z83mk8eU", "title": "2026-06-09", "parentId": "1NTVuzc69wwBXxOisDVg403K4FFgEI6pu", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-09"},
        {"id": "1CNbF6LoRI_Bf8Blh5sMbjm8OqQ_zPKHa", "title": "2026-06-10", "parentId": "1NTVuzc69wwBXxOisDVg403K4FFgEI6pu", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-10"},
        {"id": "1kZVbl_evvvbYJ8SPp7G1G7vYOSgtkw1j", "title": "2026-06-11", "parentId": "1NTVuzc69wwBXxOisDVg403K4FFgEI6pu", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-11"},
        {"id": "1FpsjBkrFD-Ahw0nRcdube71O5RU-XaXQ", "title": "2026-06-12", "parentId": "1NTVuzc69wwBXxOisDVg403K4FFgEI6pu", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-12"},
        {"id": "1veh6n5pOZoGJzfG-VdbLzdHWjZ6RzmNd", "title": "2026-06-13", "parentId": "1NTVuzc69wwBXxOisDVg403K4FFgEI6pu", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-13"}
    ],
    "files": [
        # gps_enrichment files
        {"id": "1Ykofc59aDrmDdomOLdVcKIdLGLNzv8Fb", "title": "backup_google-timeline-export_2026-07-19.csv", "mimeType": "text/csv", "size_bytes": 6820063, "parentId": "1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq", "path": "pre_extract/gps_enrichment/backup_google-timeline-export_2026-07-19.csv"},
        {"id": "13rvcwkvRmPDZZDZ6LHnhlGsBY-YY0PM3", "title": "backup_google-timeline-export_2026-07-19.gpx", "mimeType": "application/gpx+xml", "size_bytes": 8489174, "parentId": "1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq", "path": "pre_extract/gps_enrichment/backup_google-timeline-export_2026-07-19.gpx"},
        {"id": "1_gW5jdyHaJPasGu-68r0vGMzoeBEDFRa", "title": "backup_google-timeline-export_2026-07-19.kml", "mimeType": "application/vnd.google-earth.kml+xml", "size_bytes": 3044420, "parentId": "1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq", "path": "pre_extract/gps_enrichment/backup_google-timeline-export_2026-07-19.kml"},
        {"id": "1wJkrEq19X_tDfD5lMUmmnP9eAlxOc9_2", "title": "Copy of google-timeline-export.csv", "mimeType": "text/csv", "size_bytes": 6820063, "parentId": "1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq", "path": "pre_extract/gps_enrichment/Copy of google-timeline-export.csv"},
        {"id": "13oOd1yellkXVuGswO5eCLQIWIuZfu1VO", "title": "Copy of google-timeline-export.csv", "mimeType": "text/csv", "size_bytes": 6820063, "parentId": "1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq", "path": "pre_extract/gps_enrichment/Copy of google-timeline-export.csv"},
        {"id": "1zKyLUl_2rWb9wPHYiaqkATEuCBeohyBc", "title": "Copy of google-timeline-export.gpx", "mimeType": "application/gpx+xml", "size_bytes": 8489174, "parentId": "1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq", "path": "pre_extract/gps_enrichment/Copy of google-timeline-export.gpx"},
        {"id": "1y4bXTS-voBMqmM-3eLDZQdk6cSsgF2y7", "title": "Copy of google-timeline-export.kml", "mimeType": "application/vnd.google-earth.kml+xml", "size_bytes": 3044420, "parentId": "1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq", "path": "pre_extract/gps_enrichment/Copy of google-timeline-export.kml"},
        {"id": "1Kmn-TJIsWQNtIwAmgm944xzn8KnV_EJW", "title": "Timeline (3).json", "mimeType": "application/json", "size_bytes": 43607134, "parentId": "1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq", "path": "pre_extract/gps_enrichment/Timeline (3).json"},

        # code_blocks files (code snippets extracted from conversation shards)
        # images/2026/06/week24/2026-06-12
        {"id": "19w4kAu1SGLCTKqgX6pj7Ks9tUB4P9Ef3", "title": "code_99.txt", "mimeType": "text/plain", "size_bytes": 5259, "parentId": "1L4LkDH3GT2MlwYBkJCCrOPEQ7KsOQX8X", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-12/code_99.txt"},
        {"id": "1jyUOt7Jv4wB3DxQQsAp2mZfafRkBBjJA", "title": "code_98.txt", "mimeType": "text/plain", "size_bytes": 5051, "parentId": "1L4LkDH3GT2MlwYBkJCCrOPEQ7KsOQX8X", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-12/code_98.txt"},
        {"id": "1y-7_ofYW08y5L1DA_XmzQ3RAK0Xt0ih0", "title": "code_97.txt", "mimeType": "text/plain", "size_bytes": 9132, "parentId": "1L4LkDH3GT2MlwYBkJCCrOPEQ7KsOQX8X", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-12/code_97.txt"},
        {"id": "1OE1rrEi5aiB_s5ie3csdAnam7chXp3iV", "title": "code_96.txt", "mimeType": "text/plain", "size_bytes": 6385, "parentId": "1L4LkDH3GT2MlwYBkJCCrOPEQ7KsOQX8X", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-12/code_96.txt"},
        {"id": "1LGg9m4BIJnlZAKqMeoEheKyCenWuR1dJ", "title": "code_95.txt", "mimeType": "text/plain", "size_bytes": 5856, "parentId": "1L4LkDH3GT2MlwYBkJCCrOPEQ7KsOQX8X", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-12/code_95.txt"},
        {"id": "11A9TpnC1FoXkzcP_woZBpCFRO53JrUpU", "title": "code_94.txt", "mimeType": "text/plain", "size_bytes": 4148, "parentId": "1L4LkDH3GT2MlwYBkJCCrOPEQ7KsOQX8X", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-12/code_94.txt"},
        {"id": "1uVu9n58i1m3UpXirMW7uZaggEq0EtkYo", "title": "code_93.txt", "mimeType": "text/plain", "size_bytes": 10458, "parentId": "1L4LkDH3GT2MlwYBkJCCrOPEQ7KsOQX8X", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-12/code_93.txt"},
        {"id": "1qjq4lFb9ZFjbpItU0v26b0vr4AZ7pKEf", "title": "code_92.txt", "mimeType": "text/plain", "size_bytes": 6166, "parentId": "1L4LkDH3GT2MlwYBkJCCrOPEQ7KsOQX8X", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-12/code_92.txt"},
        {"id": "1sQWesNpKVQsIXsR0-fTvnabx1mZBV72z", "title": "code_91.txt", "mimeType": "text/plain", "size_bytes": 6024, "parentId": "1L4LkDH3GT2MlwYBkJCCrOPEQ7KsOQX8X", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-12/code_91.txt"},
        {"id": "12809mjLmbABq4WASTLxNQjdZMFvcohNq", "title": "code_90.txt", "mimeType": "text/plain", "size_bytes": 6602, "parentId": "1L4LkDH3GT2MlwYBkJCCrOPEQ7KsOQX8X", "path": "pre_extract/code_blocks/images/2026/06/week24/2026-06-12/code_90.txt"},

        # other/2026/06/week24/2026-06-12
        {"id": "1bjgzmpllbeqtFP1DlcqHhvxRkKTulfMx", "title": "code_102.txt", "mimeType": "text/plain", "size_bytes": 1378, "parentId": "1sdWL0TRUw6ITAuBObf2V62UyrW_visqa", "path": "pre_extract/code_blocks/other/2026/06/week24/2026-06-12/code_102.txt"},
        {"id": "1ngn2ZtXlkF9oVr8DwExuaCdx5sBnwaMW", "title": "code_6.txt", "mimeType": "text/plain", "size_bytes": 869, "parentId": "1sdWL0TRUw6ITAuBObf2V62UyrW_visqa", "path": "pre_extract/code_blocks/other/2026/06/week24/2026-06-12/code_6.txt"},
        {"id": "1ivk_pny1zdyRv3zHkEgQiBk38VMHl2Mk", "title": "code_0.txt", "mimeType": "text/plain", "size_bytes": 5313, "parentId": "1sdWL0TRUw6ITAuBObf2V62UyrW_visqa", "path": "pre_extract/code_blocks/other/2026/06/week24/2026-06-12/code_0.txt"},
        {"id": "14QNOKRGYfn_aRM2NZz3hjDKNx1UbbG_w", "title": "code_4.txt", "mimeType": "text/plain", "size_bytes": 4364, "parentId": "1sdWL0TRUw6ITAuBObf2V62UyrW_visqa", "path": "pre_extract/code_blocks/other/2026/06/week24/2026-06-12/code_4.txt"},
        {"id": "11Ib38DWWyiUA0tkdoW0cWkccHTyH-Tsy", "title": "code_3.txt", "mimeType": "text/plain", "size_bytes": 3744, "parentId": "1sdWL0TRUw6ITAuBObf2V62UyrW_visqa", "path": "pre_extract/code_blocks/other/2026/06/week24/2026-06-12/code_3.txt"},
        {"id": "1qNqyKBFkKWiOuXH8Y7bAPjSXbMa3t-ZI", "title": "code_1.txt", "mimeType": "text/plain", "size_bytes": 3923, "parentId": "1sdWL0TRUw6ITAuBObf2V62UyrW_visqa", "path": "pre_extract/code_blocks/other/2026/06/week24/2026-06-12/code_1.txt"},

        # system_prompts/2026/06/week24/2026-06-12
        {"id": "16YWgfJipfh5sFg1SO9dfp7pfxPmiVyFT", "title": "code_115.txt", "mimeType": "text/plain", "size_bytes": 3723, "parentId": "1FpsjBkrFD-Ahw0nRcdube71O5RU-XaXQ", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-12/code_115.txt"},
        {"id": "1E5p189kveg2fg3zlyZQzTyZr8jVsGVj_", "title": "code_0.txt", "mimeType": "text/plain", "size_bytes": 4236, "parentId": "1FpsjBkrFD-Ahw0nRcdube71O5RU-XaXQ", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-12/code_0.txt"},
        {"id": "15ym1ppaWR10ul-v2wwborw7RW3IzeiOW", "title": "code_3.txt", "mimeType": "text/plain", "size_bytes": 15389, "parentId": "1FpsjBkrFD-Ahw0nRcdube71O5RU-XaXQ", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-12/code_3.txt"},
        {"id": "1RK76CeQSQ33bOOvvmyN6fI0nIQqEEuYV", "title": "code_2.txt", "mimeType": "text/plain", "size_bytes": 8713, "parentId": "1FpsjBkrFD-Ahw0nRcdube71O5RU-XaXQ", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-12/code_2.txt"},
        {"id": "1v20hohUNmq2IGIIS40GGFlfT1Q4P46_l", "title": "code_1.txt", "mimeType": "text/plain", "size_bytes": 5648, "parentId": "1FpsjBkrFD-Ahw0nRcdube71O5RU-XaXQ", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-12/code_1.txt"},

        # system_prompts/2026/06/week24/2026-06-10
        {"id": "1iKjtinYY9xdra-NBsYEKBzCAPJTjLC4j", "title": "code_2.txt", "mimeType": "text/plain", "size_bytes": 3318, "parentId": "1CNbF6LoRI_Bf8Blh5sMbjm8OqQ_zPKHa", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-10/code_2.txt"},
        {"id": "1lN44w3-4yq3bJD3R2SoTjlVk_ZRxYJ9U", "title": "code_3.txt", "mimeType": "text/plain", "size_bytes": 10915, "parentId": "1CNbF6LoRI_Bf8Blh5sMbjm8OqQ_zPKHa", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-10/code_3.txt"},
        {"id": "1mGeFXFdw_MPSP6hp53h-hJ6hEoid17yf", "title": "code_0.txt", "mimeType": "text/plain", "size_bytes": 6931, "parentId": "1CNbF6LoRI_Bf8Blh5sMbjm8OqQ_zPKHa", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-10/code_0.txt"},

        # system_prompts/2026/06/week24/2026-06-09
        {"id": "1nChZ_CI10h7EqqMz59cEEiC_N-6dDrPl", "title": "code_3.txt", "mimeType": "text/plain", "size_bytes": 10915, "parentId": "1AY-WGf9oY5H8m3XpHmtngMK7z83mk8eU", "path": "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-09/code_3.txt"}
    ],
    "duplicate_files_summary": {
        "gps_enrichment": [
            {
                "file_group": "Google Timeline Export CSV",
                "filename": "google-timeline-export.csv",
                "size_bytes": 6820063,
                "file_ids": ["1Ykofc59aDrmDdomOLdVcKIdLGLNzv8Fb", "1wJkrEq19X_tDfD5lMUmmnP9eAlxOc9_2", "13oOd1yellkXVuGswO5eCLQIWIuZfu1VO"],
                "paths": [
                    "pre_extract/gps_enrichment/backup_google-timeline-export_2026-07-19.csv",
                    "pre_extract/gps_enrichment/Copy of google-timeline-export.csv",
                    "pre_extract/gps_enrichment/Copy of google-timeline-export.csv"
                ]
            },
            {
                "file_group": "Google Timeline Export GPX",
                "filename": "google-timeline-export.gpx",
                "size_bytes": 8489174,
                "file_ids": ["13rvcwkvRmPDZZDZ6LHnhlGsBY-YY0PM3", "1zKyLUl_2rWb9wPHYiaqkATEuCBeohyBc"],
                "paths": [
                    "pre_extract/gps_enrichment/backup_google-timeline-export_2026-07-19.gpx",
                    "pre_extract/gps_enrichment/Copy of google-timeline-export.gpx"
                ]
            },
            {
                "file_group": "Google Timeline Export KML",
                "filename": "google-timeline-export.kml",
                "size_bytes": 3044420,
                "file_ids": ["1_gW5jdyHaJPasGu-68r0vGMzoeBEDFRa", "1y4bXTS-voBMqmM-3eLDZQdk6cSsgF2y7"],
                "paths": [
                    "pre_extract/gps_enrichment/backup_google-timeline-export_2026-07-19.kml",
                    "pre_extract/gps_enrichment/Copy of google-timeline-export.kml"
                ]
            }
        ],
        "code_blocks": [
            {
                "file_group": "Raid Shadow Legends Hydra Build Fork Prompt",
                "filename": "code_3.txt",
                "size_bytes": 10915,
                "file_ids": ["1nChZ_CI10h7EqqMz59cEEiC_N-6dDrPl", "1lN44w3-4yq3bJD3R2SoTjlVk_ZRxYJ9U"],
                "paths": [
                    "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-09/code_3.txt",
                    "pre_extract/code_blocks/system_prompts/2026/06/week24/2026-06-10/code_3.txt"
                ]
            }
        ]
    },
    "local_workspace_audit": {
        "working_dir": "/working_dir/",
        "status": "Audited. Directory was clean (empty) prior to subagent output initialization.",
        "created_artifacts": [
            "/working_dir/c_a9665f8d4e4650d3/subagents/code_and_aux_catalog.json"
        ]
    },
    "size_and_count_breakdown": {
        "code_blocks": {
            "mapped_folders": 152,
            "cataloged_files": 25,
            "total_file_size_bytes": 162985,
            "mime_types": {"text/plain": 25}
        },
        "gps_enrichment": {
            "mapped_folders": 1,
            "cataloged_files": 8,
            "total_file_size_bytes": 87134511,
            "mime_types": {
                "text/csv": 3,
                "application/gpx+xml": 2,
                "application/vnd.google-earth.kml+xml": 2,
                "application/json": 1
            }
        },
        "graph_entities": {
            "mapped_folders": 1,
            "cataloged_files": 0,
            "total_file_size_bytes": 0,
            "status": "EMPTY"
        },
        "overall_totals": {
            "total_subfolders": 154,
            "total_files": 33,
            "total_bytes": 87297496,
            "total_size_mb": 83.25
        }
    }
}

os.makedirs('/working_dir/c_a9665f8d4e4650d3/subagents', exist_ok=True)
with open('/working_dir/c_a9665f8d4e4650d3/subagents/code_and_aux_catalog.json', 'w') as f:
    json.dump(catalog, f, indent=2)

print("Catalog successfully generated and saved.")
