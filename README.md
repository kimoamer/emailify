# 📢 Emailify - ERPNext Custom App

## 📘 Overview

**Emailify** is a custom ERPNext app that extends the default notification system by:

- 🔗 Integrating Email Templates for enhanced email notifications  
- ✅ Maintaining compatibility with existing ERPNext notifications  
- ⚙️ Seamlessly integrating with core ERPNext functionality  

---

## ✨ Key Features

### 📧 Email Template Integration

- Link notifications to existing **Email Templates**  
- Ensure consistent and branded communication  
- Update email content centrally  

### 🖥️ Enhanced User Interface

- Dynamic field visibility based on selected channel  
- Preview templates with actual document data  
- Intuitive and clean configuration UI  

### ⚙️ Technical Advantages

- Backward compatible with ERPNext's existing Notification system  
- Built-in validation ensures proper configuration  
- Logs actions and errors for easier troubleshooting  

---

## 🛠️ Installation

### ✅ Prerequisites

- ERPNext v15+  
- Bench CLI installed and configured  
- Git installed  

### 📦 Installation Steps

1. Navigate to your `apps` directory:
   ```bash
   cd /path/to/bench
   ```

2. Clone the app repository:
   ```bash
   bench get-app https://github.com/kimoamer/emailify.git
   ```

3. Install the app on your site:
   ```bash
   bench --site [your-site-name] install-app emailify
   ```

4. Restart your bench:
   ```bash
   bench restart
   ```

5. Verify the installation:
   ```bash
   bench --site [your-site-name] list-apps
   ```

---

## 🚀 Usage Guide

### 🔔 Creating Template-Based Notifications

1. **Open the Notification Doctype**  
   Go to: `Setup > Notifications > Notification`

2. **Configure the Notification**  
   - Create or edit a notification  
   - Set **Channel** to "Email"  
   - Choose an **Email Template** from the dropdown  
   - Configure remaining options as needed  

3. **Field Behavior**  
   - `Subject` and `Message` fields are hidden when a template is selected  
   - All default ERPNext fields are retained  

### 👁️ Template Preview

1. While editing a notification with a selected template, click **"Preview Template"**

2. Preview allows you to:
   - See rendered content with sample document data  
   - Validate subject and body formatting  
   - Confirm variable substitutions  

### ⚙️ Advanced Configuration

#### 🧩 Template Context Variables

```jinja
{{ name }}       # Document ID
{{ owner }}      # Document owner
{{ creation }}   # Creation timestamp
```

---

## 🧩 Customization

### 🔧 Extending Functionality

1. Override core methods in:
   ```
   notifications_manager/overrides/notification.py
   ```

2. Add new channels by:
   - Creating channel-specific handlers  
   - Extending the `send()` method accordingly  

---

## 👨‍💻 Development

### 📋 Requirements

- Python 3.7+  
- Node.js 14+  
- ERPNext v15+  
- Redis  

### 🧪 Contribution Workflow



**Contribute**:
- Fork the repository  
- Create a feature branch: `git checkout -b feature/your-feature`  
- Commit changes: `git commit -m "Add feature"`  
- Push branch: `git push origin feature/your-feature`  
- Open a Pull Request  

### 🧪 Testing Matrix

| Test Case             | Verification Method         |
|-----------------------|-----------------------------|
| Email with template   | Check Email Queue           |
| System notification   | Validate via UI alert       |
| SMS notification      | Confirm SMS delivery        |
| Template preview      | UI preview validation       |
| Condition logic       | Unit test coverage          |

---

## 📜 License

**MIT License**  
Copyright (c) [Year] [Innomate LLC]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

(License)[license.txt]