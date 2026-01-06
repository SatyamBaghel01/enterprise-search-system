import json
import os
from datetime import datetime, timedelta
import random
from faker import Faker

fake = Faker()

def ensure_dir(directory):
    """Ensure directory exists"""
    os.makedirs(directory, exist_ok=True)

def generate_confluence_data():
    """Generate dummy Confluence pages"""
    print("Generating Confluence data...")
    ensure_dir("data/confluence")
    
    spaces = ["Engineering", "Product", "Marketing", "HR"]
    page_types = ["Requirements", "Design", "Tutorial", "Meeting Notes", "Architecture"]
    
    documents = []
    
    for i in range(30):
        doc = {
            "id": f"CONF-{i+1000}",
            "title": f"{random.choice(page_types)}: {fake.catch_phrase()}",
            "content": f"""
            {fake.catch_phrase()}
            
            Overview:
            {fake.paragraph(nb_sentences=5)}
            
            Details:
            {fake.paragraph(nb_sentences=8)}
            
            Implementation:
            {fake.paragraph(nb_sentences=6)}
            
            Key Points:
            - {fake.sentence()}
            - {fake.sentence()}
            - {fake.sentence()}
            
            Next Steps:
            {fake.paragraph(nb_sentences=4)}
            """,
            "author": fake.name(),
            "space": random.choice(spaces),
            "type": "page",
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 180))).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
            "url": f"https://confluence.example.com/pages/{i+1000}",
            "tags": random.sample(["documentation", "api", "security", "performance", "testing", "deployment"], k=random.randint(1, 3))
        }
        
        documents.append(doc)
        
        # Save individual files
        with open(f"data/confluence/CONF-{i+1000}.json", 'w') as f:
            json.dump(doc, f, indent=2)
    
    print(f"Generated {len(documents)} Confluence documents")

def generate_jira_data():
    """Generate dummy Jira issues"""
    print("Generating Jira data...")
    ensure_dir("data/jira")
    
    issue_types = ["Bug", "Task", "Story", "Epic"]
    priorities = ["High", "Medium", "Low", "Critical"]
    statuses = ["Open", "In Progress", "In Review", "Done"]
    
    for i in range(40):
        doc = {
            "id": f"PROJ-{i+100}",
            "title": f"[{random.choice(issue_types)}] {fake.sentence(nb_words=6)}",
            "description": fake.paragraph(nb_sentences=5),
            "status": random.choice(statuses),
            "priority": random.choice(priorities),
            "issue_type": random.choice(issue_types),
            "reporter": fake.name(),
            "assignee": fake.name() if random.random() > 0.3 else "Unassigned",
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=random.randint(0, 15))).isoformat(),
            "url": f"https://jira.example.com/browse/PROJ-{i+100}",
            "labels": random.sample(["backend", "frontend", "database", "api", "ui", "performance"], k=random.randint(1, 3)),
            "comments": "\n".join([f"{fake.name()}: {fake.sentence()}" for _ in range(random.randint(0, 3))])
        }
        
        with open(f"data/jira/PROJ-{i+100}.json", 'w') as f:
            json.dump(doc, f, indent=2)
    
    print(f"Generated 40 Jira issues")

def generate_slack_data():
    """Generate dummy Slack messages"""
    print("Generating Slack data...")
    ensure_dir("data/slack")
    
    channels = ["general", "engineering", "product", "random", "support"]
    
    for i in range(50):
        doc = {
            "id": f"SLACK-{i+5000}",
            "channel": random.choice(channels),
            "user": fake.name(),
            "text": fake.paragraph(nb_sentences=random.randint(1, 4)),
            "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 720))).isoformat(),
            "thread_ts": f"thread-{random.randint(1000, 9999)}" if random.random() > 0.7 else None,
            "permalink": f"https://slack.example.com/archives/C123/{i+5000}"
        }
        
        with open(f"data/slack/SLACK-{i+5000}.json", 'w') as f:
            json.dump(doc, f, indent=2)
    
    print(f"Generated 50 Slack messages")

def generate_document_data():
    """Generate dummy text documents"""
    print("Generating documents...")
    ensure_dir("data/documents")
    
    doc_types = [
        "API Documentation",
        "Technical Specification",
        "User Guide",
        "System Architecture",
        "Security Policy",
        "Deployment Guide"
    ]
    
    for i in range(30):
        doc_type = random.choice(doc_types)
        content = f"""
        {doc_type}
        
        {fake.catch_phrase()}
        
        Introduction:
        {fake.paragraph(nb_sentences=8)}
        
        Main Content:
        {fake.paragraph(nb_sentences=12)}
        
        Section 1: {fake.sentence()}
        {fake.paragraph(nb_sentences=6)}
        
        Section 2: {fake.sentence()}
        {fake.paragraph(nb_sentences=6)}
        
        Section 3: {fake.sentence()}
        {fake.paragraph(nb_sentences=6)}
        
        Conclusion:
        {fake.paragraph(nb_sentences=5)}
        
        References:
        - {fake.sentence()}
        - {fake.sentence()}
        - {fake.sentence()}
        """
        
        filename = f"{doc_type.replace(' ', '_').lower()}_{i+1}.txt"
        with open(f"data/documents/{filename}", 'w') as f:
            f.write(content)
    
    print(f"Generated 30 documents")

if __name__ == "__main__":
    print("🎲 Generating dummy enterprise data...")
    print("=" * 50)
    
    generate_confluence_data()
    generate_jira_data()
    generate_slack_data()
    generate_document_data()
    
    print("=" * 50)
    print("✅ Dummy data generation complete!")
    print("\nData locations:")
    print("  - data/confluence/")
    print("  - data/jira/")
    print("  - data/slack/")
    print("  - data/documents/")