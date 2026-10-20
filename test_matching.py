import unittest
from matching import eligible,recommend

def profile(i,age=30,city='Stockholm',interests=None,low=25,high=40):
 return dict(id=i,age=age,city=city,interests=interests or ['Music','Art'],min_age=low,max_age=high)
class MatchingTests(unittest.TestCase):
 def test_reciprocal_age_preferences(self):
  self.assertFalse(eligible(profile(1),profile(2,low=31)))
  self.assertFalse(eligible(profile(1),profile(2,age=41)))
  self.assertTrue(eligible(profile(1),profile(2,age=25)))
 def test_self_and_city_excluded(self):
  u=profile(1)
  self.assertEqual(recommend(u,[u,profile(2,city='Malmö')]),[])
 def test_rank_and_explanation(self):
  u=profile(1)
  result=recommend(u,[profile(2,interests=['Music','Hiking']),profile(3)])
  self.assertEqual([p['id'] for p in result],[3,2])
  self.assertEqual(result[0]['score'],1)
  self.assertEqual(result[1]['shared_interests'],['Music'])
 def test_no_interests(self):
  u=profile(1);u['interests']=[]
  self.assertEqual(recommend(u,[profile(2)])[0]['score'],0)
if __name__=='__main__':unittest.main()
