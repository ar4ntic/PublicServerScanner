-- Development Seed Data
-- WARNING: This is for development only, do NOT use in production

-- Insert a test user (password: Test1234!)
-- Password hash generated with bcrypt (cost 10)
INSERT INTO users (id, email, password_hash, first_name, last_name, is_active) VALUES
('123e4567-e89b-12d3-a456-426614174000', 'admin@example.com', '$2a$10$6JCA.2wcm/HQTd/nVM.RaOlHM07/6MxMMiv5XBeca70vBzj4M/01e', 'Admin', 'User', true),
('123e4567-e89b-12d3-a456-426614174001', 'user@example.com', '$2a$10$6JCA.2wcm/HQTd/nVM.RaOlHM07/6MxMMiv5XBeca70vBzj4M/01e', 'Test', 'User', true);

-- Insert a test organization
INSERT INTO organizations (id, name, owner_id) VALUES
('223e4567-e89b-12d3-a456-426614174000', 'Test Organization', '123e4567-e89b-12d3-a456-426614174000');

-- Insert organization members
INSERT INTO organization_members (organization_id, user_id, role) VALUES
('223e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000', 'owner'),
('223e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174001', 'member');

-- Insert test targets
INSERT INTO targets (id, organization_id, name, hostname, description, tags, created_by) VALUES
('323e4567-e89b-12d3-a456-426614174000', '223e4567-e89b-12d3-a456-426614174000', 'Example Website', 'example.com', 'Test target for development', ARRAY['web', 'public'], '123e4567-e89b-12d3-a456-426614174000'),
('323e4567-e89b-12d3-a456-426614174001', '223e4567-e89b-12d3-a456-426614174000', 'Test API', 'api.example.com', 'API endpoint for testing', ARRAY['api', 'production'], '123e4567-e89b-12d3-a456-426614174000');

-- Insert test scans (both target-based and quick scans)
INSERT INTO scan_jobs (id, target_id, url, organization_id, initiated_by, status, progress, checks, started_at, completed_at) VALUES
-- Target-based scan
('423e4567-e89b-12d3-a456-426614174000',
 '323e4567-e89b-12d3-a456-426614174000',
 NULL,
 '223e4567-e89b-12d3-a456-426614174000',
 '123e4567-e89b-12d3-a456-426614174000',
 'completed',
 100,
 ARRAY['ping', 'portscan', 'headers', 'ssl', 'dns', 'bruteforce'],
 CURRENT_TIMESTAMP - INTERVAL '1 hour',
 CURRENT_TIMESTAMP - INTERVAL '30 minutes'),
-- Quick scan without saved target
('423e4567-e89b-12d3-a456-426614174001',
 NULL,
 'https://google.com',
 '223e4567-e89b-12d3-a456-426614174000',
 '123e4567-e89b-12d3-a456-426614174000',
 'completed',
 100,
 ARRAY['ping', 'headers', 'ssl'],
 CURRENT_TIMESTAMP - INTERVAL '2 hours',
 CURRENT_TIMESTAMP - INTERVAL '1 hour 30 minutes');

-- Insert test scan results
INSERT INTO scan_results (scan_id, check_type, status, data, findings, severity) VALUES
-- Results for target-based scan
('423e4567-e89b-12d3-a456-426614174000', 'ping', 'success', '{"response_time": "23ms", "packet_loss": 0}', 0, 'info'),
('423e4567-e89b-12d3-a456-426614174000', 'portscan', 'success', '{"open_ports": [80, 443], "total_ports_scanned": 65535}', 2, 'info'),
('423e4567-e89b-12d3-a456-426614174000', 'headers', 'success', '{"missing_headers": ["X-Frame-Options", "Content-Security-Policy"]}', 2, 'medium'),
('423e4567-e89b-12d3-a456-426614174000', 'ssl', 'success', '{"valid": true, "expires_in_days": 89, "issuer": "Let''s Encrypt"}', 0, 'info'),
('423e4567-e89b-12d3-a456-426614174000', 'dns', 'success', '{"records": {"A": ["93.184.216.34"], "MX": ["mail.example.com"]}}', 0, 'info'),
-- Results for quick scan
('423e4567-e89b-12d3-a456-426614174001', 'ping', 'success', '{"response_time": "15ms", "packet_loss": 0}', 0, 'info'),
('423e4567-e89b-12d3-a456-426614174001', 'headers', 'success', '{"missing_headers": ["X-Frame-Options"]}', 1, 'low'),
('423e4567-e89b-12d3-a456-426614174001', 'ssl', 'success', '{"valid": true, "expires_in_days": 45, "issuer": "Google Trust Services"}', 0, 'info');

-- Development note
SELECT 'Development seed data loaded successfully!' AS message,
       'Default credentials: admin@example.com / Test1234!' AS note;
