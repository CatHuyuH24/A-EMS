"""
Database migration management utilities.
"""

import os
import logging
from typing import List, Optional
from pathlib import Path
import importlib.util
from datetime import datetime

logger = logging.getLogger(__name__)


class MigrationManager:
    """Manages database migrations for microservices."""
    
    def __init__(self, migrations_dir: str):
        self.migrations_dir = Path(migrations_dir)
        self.migrations_dir.mkdir(parents=True, exist_ok=True)
        self.sql_dir = self.migrations_dir / "sql"
        self.sql_dir.mkdir(exist_ok=True)
    
    def create_migration(self, name: str, description: str = "") -> str:
        """Create a new migration file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        migration_name = f"{timestamp}_{name}.sql"
        migration_path = self.sql_dir / migration_name
        
        # Create migration template
        template = f"""-- Migration: {name}
-- Description: {description}
-- Created: {datetime.now().isoformat()}
-- 
-- Up Migration
-- 

-- Add your database changes here


-- 
-- Down Migration (Rollback)
-- 

-- Add rollback commands here (commented out)
-- These should reverse the changes made above
"""
        
        with open(migration_path, "w") as f:
            f.write(template)
        
        logger.info(f"Created migration: {migration_path}")
        return str(migration_path)
    
    def get_migrations(self) -> List[str]:
        """Get list of migration files in chronological order."""
        migrations = []
        for file in self.sql_dir.glob("*.sql"):
            migrations.append(str(file))
        return sorted(migrations)
    
    def apply_migration(self, migration_file: str) -> bool:
        """Apply a single migration."""
        try:
            from ..base import engine
            
            with open(migration_file, "r") as f:
                sql_content = f.read()
            
            # Extract up migration (before "Down Migration" comment)
            up_sql = sql_content.split("-- Down Migration")[0]
            
            with engine.connect() as connection:
                # Execute migration in transaction
                trans = connection.begin()
                try:
                    connection.execute(up_sql)
                    trans.commit()
                    logger.info(f"Applied migration: {migration_file}")
                    return True
                except Exception as e:
                    trans.rollback()
                    logger.error(f"Failed to apply migration {migration_file}: {e}")
                    raise
                    
        except Exception as e:
            logger.error(f"Migration error: {e}")
            return False
    
    def rollback_migration(self, migration_file: str) -> bool:
        """Rollback a single migration."""
        try:
            from ..base import engine
            
            with open(migration_file, "r") as f:
                sql_content = f.read()
            
            # Extract down migration (after "Down Migration" comment)
            parts = sql_content.split("-- Down Migration")
            if len(parts) < 2:
                logger.warning(f"No rollback commands found in {migration_file}")
                return False
            
            down_sql = parts[1].strip()
            if not down_sql or down_sql.startswith("--"):
                logger.warning(f"No executable rollback commands in {migration_file}")
                return False
            
            with engine.connect() as connection:
                trans = connection.begin()
                try:
                    connection.execute(down_sql)
                    trans.commit()
                    logger.info(f"Rolled back migration: {migration_file}")
                    return True
                except Exception as e:
                    trans.rollback()
                    logger.error(f"Failed to rollback migration {migration_file}: {e}")
                    raise
                    
        except Exception as e:
            logger.error(f"Rollback error: {e}")
            return False
    
    def migrate_all(self) -> bool:
        """Apply all pending migrations."""
        migrations = self.get_migrations()
        success = True
        
        for migration in migrations:
            if not self.apply_migration(migration):
                success = False
                break
        
        return success


def create_service_migration_manager(service_name: str) -> MigrationManager:
    """Create migration manager for a specific service."""
    migrations_dir = f"backend/services/{service_name}/migrations"
    return MigrationManager(migrations_dir)