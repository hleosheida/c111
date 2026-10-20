"""Generate deterministic fictional adults and run a masked-interest benchmark."""
from pathlib import Path
import random,json,statistics
from matching import INTERESTS,eligible,recommend
ROOT=Path(__file__).resolve().parent
rng=random.Random(42)
profiles=[]
for i in range(360):
 age=rng.randint(21,55)
 profiles.append({'id':i+1,'name':f'Demo member {i+1:03}','age':age,'city':['Stockholm','Gothenburg','Malmö'][i%3], 'min_age':max(18,age-8),'max_age':age+8,'interests':sorted(rng.sample(INTERESTS,rng.randint(3,6))), 'bio':'Fictional profile for a portfolio demonstration.'})
(ROOT/'data').mkdir(exist_ok=True)
(ROOT/'outputs').mkdir(exist_ok=True)
(ROOT/'data/profiles.json').write_text(json.dumps(profiles,indent=2))
model_scores=[]; random_scores=[]; counts=[]
for user in profiles:
 # One interest is hidden from the query. Relevance is overlap with the FULL
 # original interest set, not a real person's response or dating outcome.
 query={**user,'interests':user['interests'][:-1]}
 pool=[p for p in profiles if eligible(user,p)]
 counts.append(len(pool))
 def gain(p): return len(set(user['interests']) & set(p['interests']))
 def dcg(items): return sum((2**gain(p)-1)/__import__('math').log2(i+2) for i,p in enumerate(items))
 ideal=dcg(sorted(pool,key=gain,reverse=True)[:6])
 if not ideal: continue
 model_scores.append(dcg(recommend(query,profiles))/ideal)
 random_scores.append(dcg(rng.sample(pool,min(6,len(pool))))/ideal)
metrics={'seed':42,'profiles':len(profiles),'evaluated_queries':len(model_scores),'k':6,'masked_interest_ndcg_at_6':statistics.mean(model_scores),'random_baseline_ndcg_at_6':statistics.mean(random_scores),'mean_eligible_candidates':statistics.mean(counts),'limitation':'Synthetic interest-recovery benchmark only. Does not measure attraction, safety, fairness or real dating outcomes.'}
(ROOT/'outputs/metrics.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
