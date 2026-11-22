import unittest
from benchmark import predict,evaluate
class KNNTests(unittest.TestCase):
    def test_nearest(self):self.assertEqual(predict([(0,0,"A","1"),(10,10,"B","1")],(1,1),1),"A")
    def test_vote_tie(self):self.assertEqual(predict([(0,0,"B","1"),(0,0,"A","1")],(0,0),2),"A")
    def test_distance_tie(self):self.assertEqual(predict([(0,0,"B","1"),(0,0,"A","1")],(0,0),1),"B")
    def test_invalid_k(self):
        for k in [0,2,1.5]:
            with self.assertRaises(ValueError):predict([(0,0,"A","1")],(0,0),k)
    def test_excludes_test_fold(self):
        r,c=evaluate([(0,0,"A","1"),(0,0,"B","2")],(1,))
        self.assertTrue(all(x["correct"]==0 for x in r));self.assertEqual(sum(x["count"] for x in c),2)
    def test_known_separation(self):
        rows=[(0,0,"A","1"),(0,1,"A","2"),(10,10,"B","1"),(10,11,"B","2")]
        r,_=evaluate(rows,(1,));self.assertTrue(all(x["accuracy"]==1 for x in r))
    def test_invalid_folds(self):
        with self.assertRaises(ValueError):evaluate([(0,0,"A","1")])
if __name__=="__main__":unittest.main()
