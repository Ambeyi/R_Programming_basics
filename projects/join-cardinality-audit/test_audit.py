import unittest
from audit import audit

def rows(*keys): return [{'id': k} for k in keys]

class JoinTests(unittest.TestCase):
    def test_duplicate_expansion(self):
        r=audit(rows('a','a','b'),rows('a','a','a'),['id'])
        self.assertEqual(r['projected_left_join_rows'],7)
        self.assertEqual(r['many_to_many_keys'],1)
    def test_missing_never_matches(self):
        r=audit(rows('',None,' '),rows('',None,' '),['id'])
        self.assertEqual(r['matching_keys'],0)
        self.assertEqual(r['projected_left_join_rows'],3)
    def test_exact_strings(self):
        r=audit(rows('01','A',' a'),rows('1','a','a '),['id'])
        self.assertEqual(r['matched_left_rows'],0)
    def test_composite_keys(self):
        left=[{'id':'a','version':'1'},{'id':'a','version':'2'}]
        r=audit(left,[left[0]],['id','version'])
        self.assertEqual(r['matched_left_rows'],1)
    def test_empty_left(self):
        r=audit([],rows('a'),['id'])
        self.assertIsNone(r['expansion_factor'])
        self.assertEqual(r['unmatched_right_rows'],1)
    def test_empty_right(self):
        self.assertEqual(audit(rows('a','b'),[],['id'])['projected_left_join_rows'],2)
    def test_invalid_keys(self):
        for keys in ([],['id','id'],['absent']):
            with self.assertRaises(ValueError): audit(rows('a'),[],keys)
    def test_unmatched_duplicates(self):
        r=audit(rows('a'),rows('a','z','z'),['id'])
        self.assertEqual(r['right_duplicate_keys'],1)
        self.assertEqual(r['matched_key_relationship'],'one_to_one')

if __name__ == '__main__': unittest.main()
