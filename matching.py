"""Explainable matching for fictional adult profiles. Standard library only."""
import math
INTERESTS = ['Art', 'Books', 'Cooking', 'Cycling', 'Dancing', 'Film', 'Gaming', 'Hiking', 'Music', 'Photography', 'Travel', 'Yoga']
def eligible(user, other):
    return (user['id'] != other['id'] and user['city'] == other['city']
            and user['min_age'] <= other['age'] <= user['max_age']
            and other['min_age'] <= user['age'] <= other['max_age'])
def recommend(user, profiles, limit=6):
    ranked=[]
    for p in profiles:
        if not eligible(user,p): continue
        shared=sorted(set(user['interests']) & set(p['interests']))
        score=len(shared)/math.sqrt(len(user['interests'])*len(p['interests'])) if user['interests'] and p['interests'] else 0
        ranked.append({**p,'score':round(score,4),'shared_interests':shared})
    return sorted(ranked,key=lambda p:(-p['score'],p['id']))[:limit]
