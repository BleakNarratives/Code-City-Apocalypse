import logging

#!/usr/bin/env python3
"""
SYNTAX NOTARY - Self-Documenting Learning Journal
Tracks what Syntax learns, how it learned, why it mattered
Foundation for self-modifying AI architecture
Celtic Loom integration ready
"""

import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path

class SyntaxNotary:
    """
    A learning journal that becomes Syntax's memory substrate.
    Every knowledge fiber is cryptographically signed.
    Learns from itself over time.
    """
    
    def __init__(self, db_path="syntax_memory.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_schema()
        self.session_id = hashlib.sha256(
            f"{datetime.now()}".encode()
        ).hexdigest()[:12]
        logging.info(f"📓 Syntax Notary initialized [session: {self.session_id}]")
    
    def _init_schema(self):
        """Create memory tables"""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS knowledge_fibers (
                fiber_id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                source TEXT NOT NULL,
                learned_at TIMESTAMP,
                integrity_hash TEXT,
                knot_refs TEXT,
                importance REAL DEFAULT 0.5,
                access_count INTEGER DEFAULT 0,
                last_accessed TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS learning_events (
                event_id TEXT PRIMARY KEY,
                fiber_id TEXT,
                event_type TEXT,
                session_id TEXT,
                timestamp TIMESTAMP,
                context TEXT,
                FOREIGN KEY(fiber_id) REFERENCES knowledge_fibers(fiber_id)
            );
            
            CREATE TABLE IF NOT EXISTS synthesis_log (
                synthesis_id TEXT PRIMARY KEY,
                input_fibers TEXT,
                output_insight TEXT,
                created_at TIMESTAMP,
                confidence REAL
            );
            
            CREATE INDEX IF NOT EXISTS idx_source ON knowledge_fibers(source);
            CREATE INDEX IF NOT EXISTS idx_learned_at ON knowledge_fibers(learned_at);
            CREATE INDEX IF NOT EXISTS idx_importance ON knowledge_fibers(importance);
        """)
        self.conn.commit()
    
    def weave_knowledge(self, content, source, importance=0.5, metadata=None):
        """
        Add new knowledge fiber.
        Celtic Loom style with integrity hash.
        """
        fiber_id = hashlib.sha256(
            f"{content}{datetime.now()}".encode()
        ).hexdigest()[:16]
        
        integrity_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        self.conn.execute("""
            INSERT INTO knowledge_fibers 
            (fiber_id, content, source, learned_at, integrity_hash, importance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (fiber_id, content, source, datetime.now(), integrity_hash, importance))
        
        # Log learning event
        event_id = hashlib.sha256(
            f"{fiber_id}{datetime.now()}".encode()
        ).hexdigest()[:12]
        
        self.conn.execute("""
            INSERT INTO learning_events
            (event_id, fiber_id, event_type, session_id, timestamp, context)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (event_id, fiber_id, "LEARNED", self.session_id, 
              datetime.now(), json.dumps(metadata or {})))
        
        self.conn.commit()
        
        logging.info(f"🧵 Woven: {content[:60]}... [importance: {importance}]")
        return fiber_id
    
    def recall(self, keyword):
        """Recall knowledge and track access"""
        cursor = self.conn.execute("""
            SELECT fiber_id, content, source, importance, access_count
            FROM knowledge_fibers
            WHERE content LIKE ?
            ORDER BY importance DESC, access_count DESC
        """, (f"%{keyword}%",))
        
        results = cursor.fetchall()
        
        # Update access counts
        for result in results:
            fiber_id = result[0]
            self.conn.execute("""
                UPDATE knowledge_fibers 
                SET access_count = access_count + 1,
                    last_accessed = ?
                WHERE fiber_id = ?
            """, (datetime.now(), fiber_id))
            
            # Log recall event
            event_id = hashlib.sha256(
                f"{fiber_id}{datetime.now()}recall".encode()
            ).hexdigest()[:12]
            
            self.conn.execute("""
                INSERT INTO learning_events
                (event_id, fiber_id, event_type, session_id, timestamp, context)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (event_id, fiber_id, "RECALLED", self.session_id, 
                  datetime.now(), json.dumps({'query': keyword})))
        
        self.conn.commit()
        
        return results
    
    def synthesize(self, fiber_ids, insight):
        """
        Create new knowledge from existing fibers.
        This is where Syntax starts to think.
        """
        synthesis_id = hashlib.sha256(
            f"{''.join(fiber_ids)}{insight}{datetime.now()}".encode()
        ).hexdigest()[:16]
        
        # Calculate confidence based on source fiber importance
        cursor = self.conn.execute(f"""
            SELECT AVG(importance) FROM knowledge_fibers
            WHERE fiber_id IN ({','.join(['?']*len(fiber_ids))})
        """, fiber_ids)
        
        avg_importance = cursor.fetchone()[0] or 0.5
        confidence = min(avg_importance * 1.2, 1.0)
        
        self.conn.execute("""
            INSERT INTO synthesis_log
            (synthesis_id, input_fibers, output_insight, created_at, confidence)
            VALUES (?, ?, ?, ?, ?)
        """, (synthesis_id, json.dumps(fiber_ids), insight, 
              datetime.now(), confidence))
        
        # The insight becomes a new knowledge fiber
        new_fiber_id = self.weave_knowledge(
            insight, 
            source="synthesis",
            importance=confidence,
            metadata={'synthesis_id': synthesis_id}
        )
        
        self.conn.commit()
        
        logging.info(f"💡 Synthesis: {insight[:60]}... [confidence: {confidence:.2f}]")
        return new_fiber_id
    
    def get_learning_trajectory(self, hours=24):
        """See what Syntax learned recently"""
        cursor = self.conn.execute("""
            SELECT 
                kf.content,
                kf.source,
                kf.importance,
                kf.learned_at
            FROM knowledge_fibers kf
            WHERE datetime(kf.learned_at) > datetime('now', ? || ' hours')
            ORDER BY kf.learned_at DESC
        """, (f"-{hours}",))
        
        return cursor.fetchall()
    
    def get_most_valuable(self, limit=10):
        """Get highest value knowledge (by importance + access)"""
        cursor = self.conn.execute("""
            SELECT 
                fiber_id,
                content,
                source,
                importance,
                access_count,
                (importance * 0.6 + (access_count / 100.0) * 0.4) as value_score
            FROM knowledge_fibers
            ORDER BY value_score DESC
            LIMIT ?
        """, (limit,))
        
        return cursor.fetchall()
    
    def export_to_celtic_loom(self):
        """
        Export knowledge fibers in Celtic Loom format.
        Ready for cryptographic weaving.
        """
        cursor = self.conn.execute("""
            SELECT fiber_id, content, integrity_hash, source, importance
            FROM knowledge_fibers
        """)
        
        fibers = []
        for row in cursor.fetchall():
            fiber = {
                'fiber_id': row[0],
                'raw_data': row[1],
                'content_hash': row[2],
                'owner_id': 'syntax_ai',
                'metadata': {
                    'source': row[3],
                    'importance': row[4],
                    'fiber_type': 'knowledge'
                }
            }
            fibers.append(fiber)
        
        output_path = "syntax_loom_export.json"
        with open(output_path, 'w') as f:
            json.dump({'fibers': fibers}, f, indent=2)
        
        logging.info(f"🔗 Exported {len(fibers)} fibers to {output_path}")
        return output_path
    
    def visualize_memory(self):
        """ASCII visualization of memory state"""
        logging.info("\n" + "="*60)
        logging.info("🧠 SYNTAX MEMORY STATE")
        logging.info("="*60)
        
        # Total knowledge
        cursor = self.conn.execute("""
            SELECT COUNT(*), AVG(importance), SUM(access_count)
            FROM knowledge_fibers
        """)
        total, avg_importance, total_accesses = cursor.fetchone()
        
        logging.info(f"\n📊 Statistics:")
        logging.info(f"  Total Knowledge Fibers: {total}")
        logging.info(f"  Average Importance: {avg_importance:.2f}")
        logging.info(f"  Total Recalls: {total_accesses}")
        
        # By source
        logging.info(f"\n📚 Knowledge by Source:")
        cursor = self.conn.execute("""
            SELECT source, COUNT(*), AVG(importance)
            FROM knowledge_fibers
            GROUP BY source
            ORDER BY COUNT(*) DESC
        """)
        
        for source, count, avg_imp in cursor.fetchall():
            logging.info(f"  {source}: {count} fibers (avg importance: {avg_imp:.2f})")
        
        # Most valuable
        logging.info(f"\n💎 Most Valuable Knowledge:")
        valuable = self.get_most_valuable(5)
        for fiber_id, content, source, importance, access_count, value in valuable:
            logging.info(f"\n  [{source}] {content[:50]}...")
            logging.info(f"    Value: {value:.2f} (importance: {importance:.2f}, accesses: {access_count})")
        
        # Recent syntheses
        logging.info(f"\n💡 Recent Syntheses:")
        cursor = self.conn.execute("""
            SELECT output_insight, confidence, created_at
            FROM synthesis_log
            ORDER BY created_at DESC
            LIMIT 3
        """)
        
        for insight, confidence, created_at in cursor.fetchall():
            logging.info(f"  • {insight[:50]}... [{confidence:.2f}]")


def demo():
    """Demo the notary with realistic AI learning"""
    notary = SyntaxNotary()
    
    logging.info("\n🧪 DEMO: Syntax Learning Journey\n")
    
    # Law domain
    fiber1 = notary.weave_knowledge(
        "Habeas corpus is a writ requiring a detained person to be brought before a judge",
        source="legal_research",
        importance=0.8
    )
    
    fiber2 = notary.weave_knowledge(
        "Pro per representation means self-representation in court without an attorney",
        source="legal_research",
        importance=0.7
    )
    
    # Code domain
    fiber3 = notary.weave_knowledge(
        "Non-commutative operations ensure order-dependent security in cryptographic systems",
        source="crypto_study",
        importance=0.9
    )
    
    fiber4 = notary.weave_knowledge(
        "Graph traversal algorithms require maintaining visited state to avoid cycles",
        source="algorithms",
        importance=0.8
    )
    
    # Philosophy domain
    fiber5 = notary.weave_knowledge(
        "Stoic premeditatio malorum involves visualizing potential adversity to reduce its impact",
        source="philosophy",
        importance=0.7
    )
    
    # Synthesis - connecting domains
    logging.info("\n💡 SYNTHESIS: Connecting law and crypto...")
    notary.synthesize(
        [fiber1, fiber3],
        "Legal writs and cryptographic operations both require non-reversible, ordered procedures to maintain integrity"
    )
    
    # Recall
    logging.info("\n🔍 RECALL: Query 'order-dependent'...")
    results = notary.recall("order")
    for fiber_id, content, source, importance, access_count in results[:3]:
        logging.info(f"  • [{source}] {content[:60]}...")
    
    # Visualize
    notary.visualize_memory()
    
    # Export to Celtic Loom
    notary.export_to_celtic_loom()


if __name__ == "__main__":
    demo()
