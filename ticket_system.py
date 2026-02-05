#!/usr/bin/env python3
"""
Service Ticket System - SQLite backend for Safe Harbor tech tickets
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict

DB_PATH = os.path.expanduser("~/.openclaw/workspace/projects/tech-portal/tickets.db")

def init_database():
    """Create database schema"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            client TEXT NOT NULL,
            site TEXT,
            priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'critical')) DEFAULT 'medium',
            status TEXT CHECK(status IN ('open', 'in-progress', 'waiting', 'resolved', 'closed')) DEFAULT 'open',
            assigned_to TEXT,
            created_by TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            network_type TEXT CHECK(network_type IN ('unifi', 'meraki', 'both', 'other')),
            device_info TEXT,
            notes TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ticket_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            user TEXT NOT NULL,
            update_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES tickets(id)
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_tickets_assigned ON tickets(assigned_to)
    """)
    
    conn.commit()
    conn.close()
    print("✓ Database initialized")


def create_ticket(title: str, client: str, created_by: str, **kwargs) -> int:
    """Create a new ticket"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    fields = ['title', 'client', 'created_by']
    values = [title, client, created_by]
    
    optional_fields = ['description', 'site', 'priority', 'status', 'assigned_to', 
                      'network_type', 'device_info', 'notes']
    
    for field in optional_fields:
        if field in kwargs:
            fields.append(field)
            values.append(kwargs[field])
    
    placeholders = ', '.join(['?'] * len(values))
    field_names = ', '.join(fields)
    
    cursor.execute(f"""
        INSERT INTO tickets ({field_names})
        VALUES ({placeholders})
    """, values)
    
    ticket_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return ticket_id


def update_ticket(ticket_id: int, user: str, update_text: str = None, **kwargs):
    """Update ticket and log the change"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Update ticket fields
    if kwargs:
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        set_clause += ", updated_at = CURRENT_TIMESTAMP"
        values = list(kwargs.values()) + [ticket_id]
        
        cursor.execute(f"""
            UPDATE tickets
            SET {set_clause}
            WHERE id = ?
        """, values)
    
    # Log the update
    if update_text:
        cursor.execute("""
            INSERT INTO ticket_updates (ticket_id, user, update_text)
            VALUES (?, ?, ?)
        """, (ticket_id, user, update_text))
    
    conn.commit()
    conn.close()


def get_tickets(status: str = None, assigned_to: str = None, limit: int = 100) -> List[Dict]:
    """Get tickets with optional filters"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT * FROM tickets WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    if assigned_to:
        query += " AND assigned_to = ?"
        params.append(assigned_to)
    
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    tickets = []
    for row in rows:
        ticket = dict(zip(columns, row))
        
        # Get updates
        cursor.execute("""
            SELECT user, update_text, created_at
            FROM ticket_updates
            WHERE ticket_id = ?
            ORDER BY created_at DESC
        """, (ticket['id'],))
        
        ticket['updates'] = cursor.fetchall()
        tickets.append(ticket)
    
    conn.close()
    return tickets


def get_ticket_stats() -> Dict:
    """Get ticket statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'open'")
    open_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'in-progress'")
    in_progress = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE priority = 'critical' AND status NOT IN ('resolved', 'closed')")
    critical = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status IN ('resolved', 'closed') AND DATE(resolved_at) = DATE('now')")
    resolved_today = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'open': open_count,
        'in_progress': in_progress,
        'critical': critical,
        'resolved_today': resolved_today
    }


def close_ticket(ticket_id: int, user: str, resolution_notes: str):
    """Close a ticket"""
    update_ticket(
        ticket_id,
        user,
        update_text=f"Ticket closed: {resolution_notes}",
        status='closed',
        resolved_at=datetime.now().isoformat()
    )


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Tech Portal Ticket System")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Init
    parser_init = subparsers.add_parser('init', help='Initialize database')
    
    # Create
    parser_create = subparsers.add_parser('create', help='Create new ticket')
    parser_create.add_argument('--title', required=True, help='Ticket title')
    parser_create.add_argument('--client', required=True, help='Client name')
    parser_create.add_argument('--site', help='Site location')
    parser_create.add_argument('--priority', choices=['low', 'medium', 'high', 'critical'], default='medium')
    parser_create.add_argument('--assigned', help='Assign to technician')
    parser_create.add_argument('--network', choices=['unifi', 'meraki', 'both', 'other'], help='Network type')
    parser_create.add_argument('--description', help='Ticket description')
    parser_create.add_argument('--created-by', required=True, help='Your name')
    
    # List
    parser_list = subparsers.add_parser('list', help='List tickets')
    parser_list.add_argument('--status', choices=['open', 'in-progress', 'waiting', 'resolved', 'closed'])
    parser_list.add_argument('--assigned', help='Filter by assigned tech')
    
    # Update
    parser_update = subparsers.add_parser('update', help='Update ticket')
    parser_update.add_argument('id', type=int, help='Ticket ID')
    parser_update.add_argument('--status', choices=['open', 'in-progress', 'waiting', 'resolved', 'closed'])
    parser_update.add_argument('--assigned', help='Reassign ticket')
    parser_update.add_argument('--note', help='Add update note')
    parser_update.add_argument('--user', required=True, help='Your name')
    
    # Stats
    parser_stats = subparsers.add_parser('stats', help='Show ticket statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'init':
        init_database()
    
    elif args.command == 'create':
        ticket_id = create_ticket(
            title=args.title,
            client=args.client,
            created_by=args.created_by,
            site=args.site,
            priority=args.priority,
            assigned_to=args.assigned,
            network_type=args.network,
            description=args.description
        )
        print(f"✓ Ticket #{ticket_id} created")
    
    elif args.command == 'list':
        tickets = get_tickets(status=args.status, assigned_to=args.assigned)
        
        if not tickets:
            print("No tickets found")
            return
        
        print(f"\n{'ID':<5} {'Title':<40} {'Client':<20} {'Status':<12} {'Priority':<10} {'Assigned':<15}")
        print("-" * 105)
        
        for t in tickets:
            print(f"{t['id']:<5} {t['title'][:40]:<40} {t['client'][:20]:<20} {t['status']:<12} {t['priority']:<10} {t['assigned_to'] or 'Unassigned':<15}")
    
    elif args.command == 'update':
        kwargs = {}
        if args.status:
            kwargs['status'] = args.status
        if args.assigned:
            kwargs['assigned_to'] = args.assigned
        
        update_ticket(args.id, args.user, args.note, **kwargs)
        print(f"✓ Ticket #{args.id} updated")
    
    elif args.command == 'stats':
        stats = get_ticket_stats()
        print("\n📊 Ticket Statistics")
        print(f"  Open: {stats['open']}")
        print(f"  In Progress: {stats['in_progress']}")
        print(f"  Critical: {stats['critical']}")
        print(f"  Resolved Today: {stats['resolved_today']}")


if __name__ == "__main__":
    main()
