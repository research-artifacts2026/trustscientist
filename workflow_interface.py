"""Backend-neutral directory ownership contract. No task-specific logic.

Manual integration names every dependency and effect. Managed integration owns
one input and one output directory, recording every current input and the whole
output directory, including subsequently created children. Writes outside those
directories remain the application's obligation. No inference of scientific needs.
"""
from pathlib import Path
import json


class WorkflowInterface:
    def __init__(self,engine,managed):
        self.engine=engine;self.managed=managed

    def register(self,root,policy,bindings,context,action,outputs,checkpoint):
        root=Path(root)
        if self.managed:
            bindings=sorted(p.relative_to(root).as_posix() for p in (root/'evidence').iterdir() if p.is_file())
            outputs=['products']
            if checkpoint.get('resume_stage')!='analyze':raise ValueError('restart stage required')
        self.engine.record(policy,bindings,context,action,outputs,checkpoint)

    def revalidate(self):
        # Both backends expose this same method; TrustScientist's default is CBR.
        return self.engine.revalidate()

    def register_owned_directories(self,root,policy,context,action,checkpoint):
        if not self.managed:raise ValueError('managed interface required')
        return self.register(root,policy,[],context,action,[],checkpoint)
