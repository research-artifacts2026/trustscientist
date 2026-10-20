"""Independent, single-writer selective replay with a durable recovery journal.

No TrustScientist imports. Same supplied predicates, dependencies, output paths,
and restart metadata; no claimed speed disadvantage. Local filesystem effects.
"""
from pathlib import Path
import hashlib, json, os, shutil, uuid


def sha(p):
    p=Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None


def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix('.tmp')
    with tmp.open('w') as f:
        json.dump(obj,f,sort_keys=True);f.flush();os.fsync(f.fileno())
    os.replace(tmp,p)


class GenericReplay:
    def __init__(self,root,policies):
        self.root=Path(root).resolve();self.home=self.root/'.generic';self.home.mkdir(exist_ok=True)
        self.policies=policies;self.path=self.home/'state.json'

    def path_for(self,p):
        x=(self.root/p).resolve()
        if not x.is_relative_to(self.root) or x==self.root:raise ValueError('out of workspace')
        return x

    def load(self):
        return json.loads(self.path.read_text()) if self.path.exists() else {'nodes':[],'pending':None,'events':[]}

    def record(self,policy,bindings,context,old_action,outputs=(),checkpoint_before=None):
        s=self.load()
        if s['pending']:raise RuntimeError('unfinished recovery')
        deps=sorted(set(bindings));out=sorted(set(outputs))
        for p in deps+out:self.path_for(p)
        versions={p:sha(self.path_for(p)) for p in deps}
        if any(v is None for v in versions.values()):raise ValueError('missing dependency')
        if self.policies[policy](self.root,deps,context)!=old_action:raise ValueError('action not reproducible')
        s['nodes'].append(dict(policy=policy,deps=deps,versions=versions,context=context,
                               action=old_action,outputs=out,checkpoint=checkpoint_before or {}))
        write(self.path,s)

    def finish(self,s):
        pending=s['pending']
        if not pending:return
        for relative in pending['outputs']:
            src=self.path_for(relative);dst=self.home/'quarantine'/pending['id']/relative
            dst.parent.mkdir(parents=True,exist_ok=True)
            if src.exists():
                if dst.exists():raise RuntimeError('quarantine collision')
                os.rename(src,dst)
        write(self.root/'checkpoint.json',pending['checkpoint'])
        s['events'].append(pending);s['nodes']=s['nodes'][:pending['index']];s['pending']=None
        write(self.path,s)

    def revalidate(self):
        s=self.load();self.finish(s)
        result={'rollback_index':None,'replayed':[],'blocked':False}
        for i,node in enumerate(s['nodes']):
            current={p:sha(self.path_for(p)) for p in node['deps']}
            if current==node['versions']:continue
            try:action=self.policies[node['policy']](self.root,node['deps'],node['context'])
            except Exception as e:
                result.update(blocked=True,error=repr(e));return result
            result['replayed'].append({'index':i,'old':node['action'],'new':action})
            if action!=node['action']:
                outputs=sorted({p for n in s['nodes'][i:] for p in n['outputs']})
                for a in outputs:
                    for b in outputs:
                        if a!=b and Path(a) in Path(b).parents:raise ValueError('overlapping outputs')
                    if any(Path(a)==Path(p) or Path(a) in Path(p).parents for n in s['nodes'] for p in n['deps']):raise ValueError('output contains dependency')
                s['pending']={'id':uuid.uuid4().hex,'index':i,'outputs':outputs,'checkpoint':node['checkpoint']}
                write(self.path,s);self.finish(s);result['rollback_index']=i;return result
            node['versions']=current
        write(self.path,s);return result
