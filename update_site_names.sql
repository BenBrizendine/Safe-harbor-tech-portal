-- Add sites table if it doesn't exist
CREATE TABLE IF NOT EXISTS sites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id TEXT UNIQUE NOT NULL,
    site_name TEXT NOT NULL,
    platform TEXT NOT NULL, -- 'unifi' or 'meraki'
    organization TEXT,
    gateway_mac TEXT,
    device_count INTEGER DEFAULT 0,
    client_count INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert UniFi site (The Preserve at Spring Creek)
INSERT OR REPLACE INTO sites (
    site_id, site_name, platform, organization, 
    gateway_mac, device_count, client_count, last_updated
) VALUES (
    '6955d7ba43f1f93b98b1388b',
    'The Preserve at Spring Creek',
    'unifi',
    'Safe Harbor Solutions',
    '6c:63:f8:68:28:2d',
    70,
    676,
    datetime('now')
);

-- Insert Meraki sites (Frontier Management org)
INSERT OR REPLACE INTO sites (site_id, site_name, platform, organization) VALUES
    ('meraki-frontier-shs', 'Safe Harbor Solutions', 'meraki', 'Frontier Management'),
    ('meraki-frontier-portland', 'Frontier Management - Portland', 'meraki', 'Frontier Management'),
    ('meraki-frontier-dallas', 'Frontier Dallas Office', 'meraki', 'Frontier Management'),
    ('meraki-frontier-colo', 'SHS Colo', 'meraki', 'Frontier Management'),
    ('meraki-frontier-sache', 'Sache International', 'meraki', 'Frontier Management');

-- Insert Meraki sites (Welltower - CIS)
INSERT OR REPLACE INTO sites (site_id, site_name, platform, organization) VALUES
    ('meraki-wt-cis-boise', 'ID Boise - Overland Court', 'meraki', 'Welltower - CIS'),
    ('meraki-wt-cis-bremerton', 'WA Bremerton - Bay Pointe MC', 'meraki', 'Welltower - CIS'),
    ('meraki-wt-cis-havasu', 'AZ Lake Havasu - Lake View Terrace', 'meraki', 'Welltower - CIS'),
    ('meraki-wt-cis-happyvalley', 'OR Happy Valley - Monterey Court', 'meraki', 'Welltower - CIS'),
    ('meraki-wt-cis-hattiesburg', 'MS Hattiesburg - Crescent Landing', 'meraki', 'Welltower - CIS'),
    ('meraki-wt-cis-ogden', 'UT Ogden - The Auberge', 'meraki', 'Welltower - CIS'),
    ('meraki-wt-cis-test', 'CIS TEST', 'meraki', 'Welltower - CIS');

-- Insert Meraki sites (Welltower - QSL)
INSERT OR REPLACE INTO sites (site_id, site_name, platform, organization) VALUES
    ('meraki-wt-qsl-carrollton', 'GA Carrollton - Laurel Glen', 'meraki', 'Welltower - QSL');

-- Insert Meraki sites (Embassy - OH7)
INSERT OR REPLACE INTO sites (site_id, site_name, platform, organization) VALUES
    ('meraki-emb-euclid', 'Euclid', 'meraki', 'Embassy - OH7'),
    ('meraki-emb-newark', 'Newark', 'meraki', 'Embassy - OH7'),
    ('meraki-emb-lyndhurst', 'Lyndhurst', 'meraki', 'Embassy - OH7'),
    ('meraki-emb-painesville', 'Painesville', 'meraki', 'Embassy - OH7');
