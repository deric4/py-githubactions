from pydantic import BaseSettings, FilePath, Json, Field

class GithubCtx(BaseSettings):
    payload: Json
    event: Json
    event_path: FilePath
    workflow: str
    job: str
    run_id: str
    run_number: str
    actor: str
    repository: str
    repository_owner: str
    event_name: str
    sha: str #Field(...,min_length=40, max_length=40)
    ref: str
    head_ref: str
    base_ref: str
    workspace: str = None
    action: str

    class Config:
        env_prefix = 'GITHUB_'
    

context = GithubCtx()
