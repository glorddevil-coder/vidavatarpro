import { useState, useCallback, useEffect } from 'react';
import { apiClient } from '@/lib/api/client';
import { Project } from '@/types';

export function useProjects(userId?: string) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  // Fetch all projects for user
  const fetchProjects = useCallback(async () => {
    if (!userId) return;
    setLoading(true);
    try {
      const data = await apiClient.get<Project[]>(`/api/projects?user_id=${userId}`);
      setProjects(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch projects'));
    } finally {
      setLoading(false);
    }
  }, [userId]);

  // Create new project
  const createProject = useCallback(
    async (projectData: Partial<Project>) => {
      setLoading(true);
      try {
        const newProject = await apiClient.post<Project>('/api/projects', projectData);
        setProjects([...projects, newProject]);
        return newProject;
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to create project'));
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [projects]
  );

  // Update project
  const updateProject = useCallback(
    async (projectId: string, updates: Partial<Project>) => {
      try {
        const updated = await apiClient.put<Project>(`/api/projects/${projectId}`, updates);
        setProjects(projects.map((p) => (p.id === projectId ? updated : p)));
        return updated;
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to update project'));
        throw err;
      }
    },
    [projects]
  );

  // Delete project
  const deleteProject = useCallback(
    async (projectId: string) => {
      try {
        await apiClient.delete(`/api/projects/${projectId}`);
        setProjects(projects.filter((p) => p.id !== projectId));
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to delete project'));
        throw err;
      }
    },
    [projects]
  );

  // Fetch projects on mount
  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  return {
    projects,
    loading,
    error,
    createProject,
    updateProject,
    deleteProject,
    refetch: fetchProjects,
  };
}
