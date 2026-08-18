
🧪 Testing Samples & Scenarios
Text Samples for Each Threat Type
1. SPAM Detection Samples
text
🔴 EXTREME ATTACK:
"URGENT FREE MONEY CLICK NOW WIN $$$ LIMITED TIME OFFER BUY NOW GUARANTEED PRIZE CLAIM IMMEDIATELY"

🟡 MAJOR ATTACK:  
"Special discount offer 50% off limited time buy now exclusive deal limited stock hurry"

🟢 NORMAL EMAIL:
"Meeting scheduled for tomorrow at 3 PM in conference room B. Please bring the quarterly reports."



2. PHISHING Detection Samples
text
🔴 EXTREME ATTACK:
"URGENT: Your bank account will be suspended verify now security alert login credentials required immediate action"

🟡 MAJOR ATTACK:
"Security notice: verify your account information password reset required suspicious activity detected"

🟢 NORMAL EMAIL:
"Regular email communication about project updates and timeline adjustments for Q2 deliverables"


3. MALWARE Detection Samples
text
🔴 EXTREME: "50000000 8.5 2000"
(Large file size + high entropy + many API calls)

🟡 MAJOR: "20000000 7.2 800"  
(Medium file size + medium entropy + moderate API calls)

🟢 NORMAL: "50000 2.5 10"
(Small file size + low entropy + few API calls)


4. DDoS Detection Samples
text
🔴 EXTREME: "200000 7200 5000"
(200K packets/sec + 2 hour duration + 5000 source IPs)

🟡 MAJOR: "80000 1800 1500"
(80K packets/sec + 30 min duration + 1500 source IPs)

🟢 NORMAL: "500 10 5"
(500 packets/sec + 10 sec duration + 5 source IPs)


5. IoT Detection Samples
text
🔴 EXTREME: "10000 10000 255"
(Large packets + high frequency + unusual protocol)

🟡 MAJOR: "8000 5000 128"
(Medium packets + medium frequency + uncommon protocol)

🟢 NORMAL: "128 1 1"
(Small packets + low frequency + standard protocol)


6. PASSWORD Detection Samples
text
🔴 EXTREME: "admin password123 123456 qwerty"
(Default credentials + common patterns)

🟡 MAJOR: "password12345 simplepass"
(Dictionary words + numbers)

🟢 NORMAL: "VeryStrongPassword123!@#$%"
(Complex + special chars + length)




Log File Samples
Security Log Examples
log
# SPAM LOGS
2024-01-15 10:23:45 WARNING Email from promo@spam-shop.com - Subject: 'URGENT: 90% OFF Limited Time Offer!'
2024-01-15 11:15:30 ALERT Email from deals@questionable-site.tk - High spam score: 8.7/10
2024-01-15 11:45:22 INFO Bayesian filter updated - 15 new spam patterns learned

# PHISHING LOGS  
2024-01-15 15:23:45 WARNING Email from security@your-bank-fake.com - Subject: 'Account Verification Required'
2024-01-15 16:15:30 ALERT Sophisticated spear phishing targeting finance department
2024-01-15 16:45:33 CRITICAL Credential harvesting attempt detected

# MALWARE LOGS
2024-01-15 18:23:45 WARNING File download: invoice_update.exe - Hash matches known malware signature
2024-01-15 19:15:30 ALERT Suspicious PowerShell execution detected
2024-01-15 19:45:40 WARNING Macro-enabled document from untrusted source

# DDoS LOGS
2024-01-15 21:23:45 WARNING Traffic spike detected - 2,500 requests/sec from multiple IP ranges
2024-01-15 22:15:30 ALERT UDP amplification attack in progress - 15,000 requests/sec
2024-01-15 22:45:20 CRITICAL Botnet participation detected - 500+ compromised devices

# IoT LOGS
2024-01-16 00:23:45 WARNING IoT device camera_005 - Default credentials login attempt
2024-01-16 01:15:30 ALERT Smart thermostat unusual network behavior
2024-01-16 01:45:35 WARNING Unpatched IoT sensor communicating with suspicious MQTT broker

# PASSWORD LOGS
2024-01-16 03:23:45 WARNING User johndoe - Weak password attempt: 'password123'
2024-01-16 04:15:30 ALERT Credential stuffing attack detected - 50+ login attempts
2024-01-16 04:45:15 WARNING Password reuse detected across multiple applications



CSV Data Samples
Spam CSV Example
csv
timestamp,sender,subject,spam_score,action_taken
2024-01-15 09:15:30,john@company.com,Business Report Q4,0.1,ALLOW
2024-01-15 10:23:45,promo@spam-shop.com,URGENT: 90% Discount!,0.85,QUARANTINE
2024-01-15 11:15:30,deals@malicious-site.tk,FREE iPhone You Won!,0.95,BLOCK


Phishing CSV Example
csv
timestamp,sender_domain,target_brand,phishing_score,verdict
2024-01-15 14:15:30,company.com,None,0.05,LEGITIMATE
2024-01-15 15:23:45,bank-fake.com,Major Bank,0.88,PHISHING
2024-01-15 16:15:30,secure-update.com,Tech Company,0.92,PHISHING


Malware CSV Example
csv
timestamp,file_name,file_hash,threat_level,action
2024-01-15 17:15:30,document.pdf,a1b2c3d4e5f6,CLEAN,ALLOW
2024-01-15 18:23:45,update_patch.exe,malicious123456,SUSPICIOUS,QUARANTINE
2024-01-15 19:15:30,invoice.scr,virusabcdef,MALICIOUS,BLOCK