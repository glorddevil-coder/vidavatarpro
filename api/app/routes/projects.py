from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
)

router = APIRouter(prefix="/api/projects", tags=["projects"])

# Mock database - replace with Supabase
projects_db = {}

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(user_id: str = Query(...)):
    """List all projects for a user."""
    user_projects = [p for p in projects_db.values() if p.get("user_id") == user_id]
    return user_projects

@router.post("/", response_model=ProjectResponse)
async def create_project(user_id: str, project: ProjectCreate):
    """Create a new project."""
    project_id = f"proj_{len(projects_db)}"
    new_project = {
        "id": project_id,
        "user_id": user_id,
        **project.dict(),
        "status": "draft",
        "created_at": "2024-01-01T00:00:00Z",
        "last_synced": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
    }
    projects_db[project_id] = new_project
    return new_project

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Get a specific project."""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects_db[project_id]

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, updates: ProjectUpdate):
    """Update a project."""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects_db[project_id]
    update_data = updates.dict(exclude_unset=True)
    project.update(update_data)
    return project

@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """Delete a project."""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    del projects_db[project_id]
    return {"deleted": True}
